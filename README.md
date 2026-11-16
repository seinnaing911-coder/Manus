# Myanmar Auto Video Dubbing

Streamlit app: upload one video; extract audio; use Gemini 3.8 Flash to transcribe Chinese/English speech and translate it into Burmese; generate Burmese speech with Microsoft Edge Thiha Neural; fit video segments to the generated speech without changing speech speed.

## Streamlit secrets

Keep your existing password and API key in Streamlit Secrets:

APP_PASSWORD = "your-existing-password"
GEMINI_API_KEY = "your-gemini-api-key"

Do not share your API key publicly. This build keeps the password login and the Thiha Neural voice.
