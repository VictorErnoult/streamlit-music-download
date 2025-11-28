# Music Download

A lightweight Streamlit app for downloading audio from YouTube playlists.

## Features

- Download all audio tracks from a public YouTube playlist
- User-specified download folder
- MP3 format output
- Progress tracking per track
- Error reporting (skips failed tracks and continues)

## Requirements

- Python 3.8+
- ffmpeg (required for audio conversion)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure ffmpeg is installed on your system

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

Then:
1. Enter a YouTube playlist URL
2. Select or enter a download folder
3. Click download and wait for completion

## License

MIT

