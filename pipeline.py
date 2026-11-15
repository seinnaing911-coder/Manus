#!/usr/bin/env python3
"""Render an MP4 with its original speech replaced by Burmese TTS audio.

The video stream is kept intact. Each TTS segment is placed at its original
subtitle timestamp on a silent timeline, so pauses and non-speech video are
preserved instead of being removed by concatenating clips.
"""
from __future__ import annotations

import argparse
import asyncio
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

import edge_tts
import pysrt
from pydub import AudioSegment

VOICE = "my-MM-ThihaNeural"


def run(command: list[str]) -> None:
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr[-3000:] or "FFmpeg command failed")


def subtitle_seconds(item: pysrt.SubRipItem) -> tuple[float, float]:
    start = item.start.hours * 3600 + item.start.minutes * 60 + item.start.seconds + item.start.milliseconds / 1000
    end = item.end.hours * 3600 + item.end.minutes * 60 + item.end.seconds + item.end.milliseconds / 1000
    return start, end


def video_duration(video: Path) -> float:
    result = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
        text=True,
    ).strip()
    return float(result)


async def generate_audio(subtitles: pysrt.SubRipFile, audio_dir: Path) -> None:
    for index, subtitle in enumerate(subtitles):
        text = subtitle.text.replace("\n", " ").strip()
        if text:
            await edge_tts.Communicate(text, VOICE).save(str(audio_dir / f"audio_{index}.mp3"))


def fit_audio(audio: AudioSegment, target_ms: int) -> AudioSegment:
    if target_ms <= 0:
        return AudioSegment.empty()
    if len(audio) > target_ms:
        return audio[:target_ms]
    return audio + AudioSegment.silent(duration=target_ms - len(audio), frame_rate=audio.frame_rate)


def build_dubbed_track(subtitles: pysrt.SubRipFile, audio_dir: Path, duration: float, output_wav: Path) -> None:
    sample_rate = 24000
    track = AudioSegment.silent(duration=math.ceil(duration * 1000) + 250, frame_rate=sample_rate).set_channels(1)
    for index, subtitle in enumerate(subtitles):
        source = audio_dir / f"audio_{index}.mp3"
        if not source.exists():
            continue
        start, end = subtitle_seconds(subtitle)
        if end <= start or start >= duration:
            continue
        target_ms = max(1, min(int((end - start) * 1000), int(duration * 1000 - start * 1000)))
        clip = fit_audio(AudioSegment.from_file(source), target_ms).set_frame_rate(sample_rate).set_channels(1)
        track = track.overlay(clip, position=max(0, int(start * 1000)))
    track.export(output_wav, format="wav")


def process(video: Path, srt: Path, output: Path) -> None:
    if not video.exists():
        raise FileNotFoundError(f"Video not found: {video}")
    if not srt.exists():
        raise FileNotFoundError(f"Subtitle not found: {srt}")

    subtitles = pysrt.open(str(srt), encoding="utf-8")
    if not subtitles:
        raise ValueError("The SRT file does not contain any subtitle lines")

    work_dir = Path(tempfile.mkdtemp(prefix="dubwave-"))
    audio_dir = work_dir / "tts"
    audio_dir.mkdir(parents=True, exist_ok=True)
    track_path = work_dir / "burmese_track.wav"
    try:
        asyncio.run(generate_audio(subtitles, audio_dir))
        build_dubbed_track(subtitles, audio_dir, video_duration(video), track_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        run([
            "ffmpeg", "-y", "-i", str(video), "-i", str(track_path),
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
            "-b:a", "128k", "-shortest", "-movflags", "+faststart", str(output),
        ])
        if not output.exists() or output.stat().st_size == 0:
            raise RuntimeError("FFmpeg did not create the final output")
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Replace an MP4's original audio with Burmese TTS")
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--srt", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    process(args.video, args.srt, args.output)
    print(f"Created {args.output}")


if __name__ == "__main__":
    main()
