# Myanmar Auto Video Dubbing

Streamlit app: one video upload, timestamped speech recognition, Burmese translation and TTS, plus manual blur and subtitle styling.

## Included
- One MP4 / MOV / MKV / WEBM upload.
- Grok Voice batch transcription with Groq Whisper and local faster-whisper fallbacks.
- Grok translation first, Manus AI JSON-compatible translation fallback, then Gemini/OpenRouter fallback.
- Grok TTS first, with Burmese Edge TTS voices (Nilar and Thiha) as fallback.
- Original audio is removed from the final video; only generated Burmese voice is mixed.
- Preview and manually drawn rectangular blur regions. Save multiple regions with individual start/end times and blur strength.
- Subtitle font size, color, and vertical position settings.
- MP4, MP3 and SRT exports.
- Speech segments are fitted into their time slots to reduce overlap.

## Deploy
Upload `app.py`, `requirements.txt`, `packages.txt`, and `.streamlit/config.toml` to the connected GitHub repository.

Set these in Streamlit Cloud > App > Settings > Secrets:
```toml
XAI_API_KEY = "your-xai-key"
MANUS_API_URL = "https://your-manus-api-host"
MANUS_API_KEY = "your-manus-key"
MANUS_MODEL = "your-manus-model-id"
GEMINI_API_KEY = "your-gemini-key"
GROQ_API_KEY = "your-groq-key"
OPENROUTER_API_KEY = "your-openrouter-key"
APP_PASSWORD = "your-private-password"
```
Keep API keys private. Do not commit real keys to GitHub.

## Provider order

The app uses Grok as the primary provider. Grok Voice STT transcribes the uploaded audio, Grok translates the timestamped segments into concise spoken Burmese, and Grok TTS generates the replacement voice. If any Grok step fails, the app falls back to Manus AI where configured, then the existing Groq, Gemini, OpenRouter, local Whisper, or Edge TTS providers. `MANUS_API_URL` must expose the OpenAI-compatible `/v1/chat/completions` endpoint.

## Notes
- The uploaded video must contain an audio track with speech for transcription.
- Blur areas are rectangles drawn on the selected preview frame. Their time range controls when the blur appears.
- Speech recognition timestamps may not be perfect. Very long Burmese lines can be shortened by fitting them into the available slot.
- Streamlit Cloud CPU, memory, execution time, network access and provider quotas can limit large-video processing.
