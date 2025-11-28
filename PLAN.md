# Music Download App

Create a new Streamlit application for downloading audio from YouTube playlists.

## Implementation Plan

### 1. Repository Setup
- Create new directory `music-download` in the workspace
- Initialize git repository with SSH remote
- Set up basic project structure

### 2. Core Dependencies
- `streamlit` - Web UI framework
- `yt-dlp` - YouTube downloader (recommended for reliability and playlist support)
- `ffmpeg` - Required by yt-dlp for audio conversion to MP3 (system dependency)

### 3. Main Application (`app.py`)
- Streamlit UI with:
  - URL input field for YouTube playlist
  - Folder picker/input for user-specified download location
  - Download button to trigger batch download
  - Progress indicators (per track and overall)
  - Error reporting section (display failed tracks, continue with others)
- Backend logic:
  - Validate playlist URL
  - Extract playlist information (track count, titles)
  - Download each track as audio (MP3 format)
  - Save to user-specified folder
  - Error handling: Report errors for failed tracks, skip and continue with remaining tracks
  - Display summary of successful vs failed downloads

### 4. Supporting Files
- `requirements.txt` - Python dependencies
- `README.md` - Setup and usage instructions
- `.gitignore` - Exclude downloads folder and Python cache

### 5. Features
- Playlist URL validation
- Progress tracking per track
- Download status display
- Error logging for failed downloads
- Organized file naming (track number + title)

## Technical Details

- Use `yt-dlp` library for YouTube downloading (chosen over pytube for better reliability and playlist support)
- Audio format: MP3 (user preference)
- Download location: User-specified folder via Streamlit file/folder picker
- Error handling: Report errors for each failed track, skip failed tracks and continue with remaining downloads
- UI: Simple, clean interface with progress bars, status messages, and error reporting section
- Note: Requires ffmpeg to be installed on the system for MP3 conversion

## Implementation Todos

- [ ] setup-repo: Create new repository directory, initialize git, and set up SSH remote
- [ ] setup-dependencies: Create requirements.txt with streamlit, yt-dlp, and other necessary packages
- [ ] create-app: Build main Streamlit app (app.py) with URL input, download functionality, and progress tracking
- [ ] add-supporting-files: Create README.md with setup instructions and .gitignore file

