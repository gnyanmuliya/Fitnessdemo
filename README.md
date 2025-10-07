# FriskaAi - Smart Fitness Advisor (Streamlit)

This repository contains `c1.py`, a Streamlit application that creates personalized fitness plans using an AI backend.

## Quick start (local)

1. Create and activate a Python environment (recommended).
2. Install dependencies:

```
python -m pip install -r requirements.txt
```

3. Run the app:

```
streamlit run "c1.py"
```

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to https://share.streamlit.io and create a new app from your GitHub repo.
3. In the app settings, open "Secrets" and add the following keys:

- API_KEY: your AI service API key
- ENDPOINT_URL: the full endpoint URL for the chat completions (e.g., your Azure or other provider endpoint)

4. Deploy and open the app.

Notes:
- The app will warn if the secrets are missing and some features (AI generation) will be disabled.
- Make sure the `archive/exercisedb_v1_sample` folder is included in the repo if you want local exercise GIFs to show.

## Troubleshooting

- If images or GIFs don't display on Streamlit sharing, confirm that the files are present in the repository and the paths are correct.
- If AI responses return errors, check your endpoint URL and API key, and review provider docs for the correct request format.

## Security

Do NOT commit secret API keys into the repository. Use Streamlit secrets or environment variables.
