# Myanmar Auto Video Dubbing — No Blur Version

This version removes the manual blur tool and its preview-canvas dependency. It keeps the single-video dubbing workflow, a simple video preview, Burmese voice selection, subtitle appearance controls, and MP4 / MP3 / SRT downloads.

## Features
- Upload one MP4 / MOV / MKV / WEBM video (up to 500 MB configured).
- Groq Whisper transcription with timestamps; local faster-whisper fallback.
- Burmese translation using Gemini with OpenRouter fallback.
- Burmese Edge TTS voices: Nilar (`my-MM-NilarNeural`) and Thiha (`my-MM-ThihaNeural`).
- Original audio is not included in the final MP4; only generated Burmese TTS is used.
- Optional burned-in Burmese subtitles with size, color, and position controls.
- Download MP4, MP3, and SRT.
- No blur features, no drawable canvas, and no `image_to_url` compatibility patch.

## Deploy
Replace `app.py`, `requirements.txt`, `packages.txt`, and `.streamlit/config.toml` in the GitHub repository connected to Streamlit Community Cloud. Keep your existing Streamlit Secrets unchanged.

Required Secrets: `GROQ_API_KEY` and at least one of `GEMINI_API_KEY` or `OPENROUTER_API_KEY`. `APP_PASSWORD` is optional.
