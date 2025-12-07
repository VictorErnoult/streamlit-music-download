# Music Download App

Create a new Streamlit application for downloading audio from YouTube playlists.

## Implementation Plan

### 1. Repository Setup
- Work in current directory (`streamlit-music-download`)
- Set up basic project structure

### 2. Core Dependencies
- `streamlit` - Web UI framework
- `yt-dlp` - YouTube downloader (recommended for reliability and playlist support)
- `ffmpeg` - Required by yt-dlp for audio conversion to MP3 (system dependency)

### 3. Main Application (`app.py`)
- Streamlit UI with:
  - URL input field for YouTube playlist
  - Download button to trigger batch download
  - Simple progress indicator ("Downloading track X of Y...")
  - Error reporting section (display failed tracks, continue with others)
- Backend logic:
  - Validate playlist URL
  - Extract playlist information (track count, titles)
  - Download each track as audio (MP3 format)
  - Save to `downloads/[playlist-name]/` folder (create subfolder per playlist)
  - File naming: `Song Title.mp3` (sanitize special characters for filesystem compatibility)
  - Error handling: Report errors for failed tracks, skip and continue with remaining tracks
  - Display summary of successful vs failed downloads

### 4. Supporting Files
- `requirements.txt` - Python dependencies
- `packages.txt` - System dependencies (ffmpeg) for Streamlit Cloud deployment
- `README.md` - Setup and usage instructions
- `.gitignore` - Exclude downloads folder and Python cache

### 5. Features
- Playlist URL validation
- Simple progress tracking ("Downloading track X of Y...")
- Download status display
- Error reporting for failed downloads (continue with remaining tracks)
- File naming: `Song Title.mp3` (special characters sanitized for filesystem compatibility)

## Technical Details

- Use `yt-dlp` library for YouTube downloading (chosen over pytube for better reliability and playlist support)
- Audio format: MP3 (user preference)
- Download location: `downloads/[playlist-name]/` folder (auto-created subfolder per playlist)
- File naming: `Song Title.mp3` format with special characters sanitized (replace invalid filesystem characters like `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|` with underscores or remove them)
- Error handling: Report errors for each failed track, skip failed tracks and continue with remaining downloads
- UI: Simple, clean interface with status messages and error reporting section
- Progress: Simple text-based progress ("Downloading track X of Y...")
- Note: Requires ffmpeg to be installed on the system for MP3 conversion
- Deployment: `packages.txt` file included for Streamlit Cloud deployment (automatically installs ffmpeg)

## Implementation Todos

- [ ] setup-dependencies: Create requirements.txt with streamlit, yt-dlp, and other necessary packages
- [ ] create-app: Build main Streamlit app (app.py) with URL input, download functionality, and simple progress tracking
- [ ] add-supporting-files: Create README.md with setup instructions and .gitignore file

