# Myanmar Auto Video Dubbing

Streamlit app: one video upload, timestamped speech recognition, Burmese translation and TTS, plus manual blur and subtitle styling.

## Included
- One MP4 / MOV / MKV / WEBM upload.
- Groq Whisper transcription with local faster-whisper fallback.
- Gemini translation with OpenRouter fallback.
- Burmese Edge TTS voices: Nilar and Thiha.
- Original audio is removed from the final video; only generated Burmese voice is mixed.
- Preview and manually drawn rectangular blur regions. Save multiple regions with individual start/end times and blur strength.
- Subtitle font size, color, and vertical position settings.
- MP4, MP3 and SRT exports.
- Speech segments are fitted into their time slots to reduce overlap.

## Deploy
Upload `app.py`, `requirements.txt`, `packages.txt`, and `.streamlit/config.toml` to the connected GitHub repository.

Set these in Streamlit Cloud > App > Settings > Secrets:
```toml
GROQ_API_KEY = "your-groq-key"
GEMINI_API_KEY = "your-gemini-key"
OPENROUTER_API_KEY = "your-openrouter-key"
APP_PASSWORD = "your-private-password"
```
Keep API keys private. Do not commit real keys to GitHub.

## Notes
- The uploaded video must contain an audio track with speech for transcription.
- Blur areas are rectangles drawn on the selected preview frame. Their time range controls when the blur appears.
- Speech recognition timestamps may not be perfect. Very long Burmese lines can be shortened by fitting them into the available slot.
- Streamlit Cloud CPU, memory, execution time, network access and provider quotas can limit large-video processing.
