# Myanmar Auto Video Dubbing

A single-video Streamlit app that transcribes the original speech, translates each timestamped speech segment into Burmese, generates Burmese TTS, and exports a dubbed video.

## What this version does
- Upload one MP4 / MOV / MKV / WEBM video.
- Uses Groq Whisper to detect speech with timestamps (local faster-whisper is a fallback).
- Translates speech segments into concise spoken Burmese using Gemini, with OpenRouter fallback.
- Generates Burmese speech with Edge TTS voices Nilar (`my-MM-NilarNeural`) or Thiha (`my-MM-ThihaNeural`).
- Removes the original audio track from the final MP4. Original dialogue, music, and ambient sound are not carried into the output.
- Keeps the original video duration and places Burmese speech using detected timestamps.
- Downloads MP4, MP3, and SRT.

## Deploy
1. Upload `app.py`, `requirements.txt`, `packages.txt`, and `.streamlit/config.toml` to the GitHub repository connected to Streamlit Community Cloud.
2. In Streamlit App Settings > Secrets, configure:

```toml
GROQ_API_KEY = "your-groq-key"
GEMINI_API_KEY = "your-gemini-key"
OPENROUTER_API_KEY = "your-openrouter-key"
APP_PASSWORD = "your-private-password"
```

At minimum, Groq plus one translation provider (Gemini or OpenRouter) is required. Keep keys private; never commit them to GitHub or paste them into chat.

## Notes and limitations
- The original audio is extracted temporarily for speech recognition only; it is not included in the final MP4.
- Speech timestamps come from automatic speech recognition and may not be perfectly exact. If a Burmese translation is longer than the available gap, the app speeds that segment up by up to 1.5x; dense dialogue can still overlap slightly.
- Music and ambient sounds are removed too, because the final video uses only the generated Burmese voice track.
- Edge TTS requires network access. Provider quotas, model availability, and Streamlit Cloud CPU/time limits can affect processing.
- A 500 MB upload limit does not guarantee every large video can be processed within Streamlit Cloud resource limits.
