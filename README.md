# Myanmar Auto Video Dubbing — Manual Blur compatibility fix

This package keeps the single-video Burmese dubbing workflow and manually drawn blur regions. It includes a compatibility adapter for `streamlit-drawable-canvas==0.9.3` on recent Streamlit versions where `image_to_url` moved and began expecting a layout object with a `.width` attribute.

## Deploy

Replace `app.py`, `requirements.txt`, and `packages.txt` in the connected GitHub repository. Keep the existing Streamlit Secrets unchanged. Keep `.streamlit/config.toml` in the repository.

## Secrets

`GROQ_API_KEY`, at least one of `GEMINI_API_KEY` or `OPENROUTER_API_KEY`, and optionally `APP_PASSWORD` are read from Streamlit Secrets.

## Note

The compatibility fix is code-checked for Python syntax. Actual rendering must still be verified in the deployed Streamlit Cloud environment.
