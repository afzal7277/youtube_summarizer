# YouTube Summarizer

Automated workflow to summarize new YouTube videos from a specified channel and send the summary via email.

## Features

- Detects new uploads from a target YouTube channel
- Downloads audio using `yt-dlp`
- Transcribes audio using OpenAI Whisper API
- Summarizes transcript with GPT-4
- Sends summary via email

## Requirements

- Python 3.7+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [openai](https://pypi.org/project/openai/)
- [google-api-python-client](https://pypi.org/project/google-api-python-client/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Setup

1. **Create and activate a virtual environment (recommended):**
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```

2. **Install dependencies:**
    - If you have a `requirements.txt` file:
        ```sh
        pip install -r requirements.txt
        ```
    - Or install manually:
        ```sh
        pip install yt-dlp openai google-api-python-client python-dotenv
        ```

3. **Create a `.env` file in the project directory with the following variables:**
    ```
    YOUTUBE_API_KEY=your_youtube_api_key
    OPENAI_API_KEY=your_openai_api_key
    CHANNEL_ID=target_channel_id
    EMAIL_FROM=your_email@gmail.com
    EMAIL_TO=recipient_email@gmail.com
    EMAIL_PASSWORD=your_email_app_password
    ```

4. Make sure you have enabled the YouTube Data API v3 and have the necessary API keys.

5. For Gmail, generate an [App Password](https://support.google.com/accounts/answer/185833) for email sending.

## Usage

Run the summarizer:

```sh
python youtube_summarizer.py
```

- The script checks for new videos, downloads and transcribes the latest one, summarizes it, and sends the summary via email.
- The last processed video ID is stored in `last_video_id.txt` to avoid duplicate processing.

## Logging

Logs are saved to `youtube_summarizer.log`.

## Notes

- The script uses OpenAI's Whisper API for transcription and GPT-4 for summarization.
- You can modify the prompt in `summarize_text` for different summary styles.

## License

MIT License