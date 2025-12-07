import streamlit as st
import yt_dlp
import os
import re
import shutil
import zipfile
import io
import tempfile
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Ginette la Cassette",
    page_icon="📼",
    layout="centered"
)


def get_ffmpeg_path():
    """Detect ffmpeg installation path for local and cloud deployments."""
    # Check common locations first (absolute paths)
    possible_paths = [
        '/usr/bin/ffmpeg',  # Streamlit Cloud / Linux
        '/usr/local/bin/ffmpeg',  # macOS / Linux alternative
    ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path
    
    # Fallback: try to find it in PATH (this returns full path)
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        return ffmpeg_path
    
    return None


def get_cookies_path():
    """Get cookies file path from Streamlit secrets if available."""
    try:
        if 'youtube' in st.secrets and 'cookies' in st.secrets.youtube:
            # Create a temporary file for cookies
            cookies_content = st.secrets.youtube.cookies
            temp_cookies = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
            temp_cookies.write(cookies_content)
            temp_cookies.close()
            # Debug: confirm cookies loaded
            st.session_state.cookies_loaded = True
            return temp_cookies.name
    except Exception as e:
        # Debug: show error if cookies fail to load
        st.session_state.cookies_error = str(e)
        pass
    return None


st.markdown("### 📼 Ginette la Cassette te souhaite un Joyeux Noël 🎅 🎶")
st.markdown(
    """
1) Colle l’URL d’une playlist YouTube **publique** (ou non répertoriée)  
   - Ouvre la page de la playlist sur YouTube  
   - Clique sur **Partager** puis **Copier le lien**  
2) Clique sur **Trouver les morceaux**, attends la fin du chargement, puis télécharge les fichiers
    """
)

# Add global CSS for blue buttons (no client JS needed)
st.markdown("""
<style>
    /* Make all buttons blue by default */
    .stButton > button,
    .stForm button[type="submit"],
    .stDownloadButton > button {
        background-color: #0066cc !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button:hover,
    .stForm button[type="submit"]:hover,
    .stDownloadButton > button:hover {
        background-color: #0052a3 !important;
        opacity: 0.9;
    }
    /* Make primary buttons (like "Trouver les morceaux") blue */
    button[kind="primary"] {
        background-color: #0066cc !important;
        color: white !important;
        border: none !important;
    }
    button[kind="primary"]:hover {
        background-color: #0052a3 !important;
        opacity: 0.9;
    }
    /* Streamlit text input (normal + focus) */
    .stTextInput input:focus {
        border-color: #0066cc !important;
        box-shadow: 0 0 0 1px #0066cc !important;
    }
    .stTextInput input {
        border-color: #0066cc !important;
        box-shadow: 0 0 0 1px #0066cc !important;
    }
    /* Catch-all for baseweb input wrappers (prevents red outline) */
    [data-baseweb="input"] > div:focus-within,
    [data-baseweb="input"] input:focus {
        border-color: #0066cc !important;
        box-shadow: 0 0 0 1px #0066cc !important;
    }
</style>
""", unsafe_allow_html=True)

# Check for ffmpeg availability (silently, only show error if not found)
ffmpeg_path = get_ffmpeg_path()
if not ffmpeg_path:
    st.error("⚠️ **ffmpeg introuvable !** Veuillez installer ffmpeg pour utiliser cette application. La conversion MP3 nécessite ffmpeg.")
    st.info("**Installation :**\n- macOS : `brew install ffmpeg`\n- Linux : `sudo apt-get install ffmpeg`\n- Windows : Télécharger depuis [ffmpeg.org](https://ffmpeg.org/download.html)")

# Initialize session state
if 'downloading' not in st.session_state:
    st.session_state.downloading = False
if 'download_results' not in st.session_state:
    st.session_state.download_results = {'success': [], 'failed': []}
if 'downloaded_files' not in st.session_state:
    st.session_state.downloaded_files = set()
if 'cookies_loaded' not in st.session_state:
    st.session_state.cookies_loaded = False
if 'cookies_error' not in st.session_state:
    st.session_state.cookies_error = None

# Debug: Show cookies status
if st.session_state.cookies_loaded:
    st.success("✅ Cookies YouTube chargés depuis les secrets")
elif st.session_state.cookies_error:
    st.error(f"❌ Erreur de chargement des cookies : {st.session_state.cookies_error}")
else:
    # Try to load cookies to check status
    test_cookies = get_cookies_path()
    if test_cookies:
        os.unlink(test_cookies)  # Clean up test file
    if not st.session_state.cookies_loaded:
        st.warning("⚠️ Pas de cookies configurés - certaines playlists peuvent être bloquées (403)")


def sanitize_filename(filename):
    """Remove or replace invalid filesystem characters."""
    # Remove invalid characters: / \ : * ? " < > |
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    # Replace multiple underscores with single underscore
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized


def create_zip_file(output_dir, playlist_name, track_titles):
    """Create a ZIP file containing only the MP3 files from the current playlist.
    
    Args:
        output_dir: Directory containing the MP3 files
        playlist_name: Name of the playlist
        track_titles: List of track titles that belong to this playlist
    """
    zip_buffer = io.BytesIO()
    sanitized_playlist_name = sanitize_filename(playlist_name)
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Only include files that match the track titles from this playlist
        for track_title in track_titles:
            sanitized_title = sanitize_filename(track_title)
            file_path = Path(output_dir) / f"{sanitized_title}.mp3"
            
            if file_path.exists():
                # Add file to zip with just the filename (no path)
                zip_file.write(file_path, arcname=file_path.name)
    
    zip_buffer.seek(0)
    return zip_buffer, sanitized_playlist_name


def get_playlist_info(url):
    """Extract playlist information without downloading."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # Don't download, just get info
        # Use Android client profile + explicit UA to reduce 403 issues on YouTube
        'extractor_args': {'youtube': {'player_client': ['android', 'web', 'ios']}},
        'http_headers': {'User-Agent': 'Mozilla/5.0'},
        # Additional options to bypass restrictions
        'geo_bypass': True,
        'geo_bypass_country': 'US',
    }
    
    # Add cookies if available
    cookies_path = get_cookies_path()
    if cookies_path:
        ydl_opts['cookiefile'] = cookies_path
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        st.error(f"Erreur lors de la récupération des informations de la playlist : {str(e)}")
        return None
    finally:
        # Clean up temp cookies file if created
        if cookies_path and os.path.exists(cookies_path):
            try:
                os.unlink(cookies_path)
            except:
                pass


def download_playlist(url, output_dir, playlist_info=None):
    """Download all tracks from a YouTube playlist.
    
    Args:
        url: YouTube playlist URL
        output_dir: Directory to save downloaded files
        playlist_info: Optional pre-fetched playlist info to avoid duplicate fetching
    """
    results = {'success': [], 'failed': []}
    
    try:
        # Use provided info or fetch it if not available
        if playlist_info is None:
            ydl_info_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'extractor_args': {'youtube': {'player_client': ['android']}},
                'http_headers': {'User-Agent': 'Mozilla/5.0'},
            }
            
            with yt_dlp.YoutubeDL(ydl_info_opts) as ydl:
                playlist_info = ydl.extract_info(url, download=False)
        
        if 'entries' not in playlist_info:
            st.error("Aucune entrée trouvée dans la playlist. Assure-toi que l'URL de la playlist est valide et publique.")
            return results
        
        entries = [e for e in playlist_info['entries'] if e is not None]
        total_tracks = len(entries)
        
        if total_tracks == 0:
            st.error("La playlist semble être vide.")
            return results
        
        # Get ffmpeg path once (important for Streamlit Cloud)
        ffmpeg_path = get_ffmpeg_path()
        
        # Download each track individually
        for idx, entry in enumerate(entries, 1):
                if not st.session_state.downloading:
                    break
                    
                track_title = entry.get('title', f'Piste {idx}')
                track_url = entry.get('url') or entry.get('id')
                
                if not track_url:
                    # If we don't have a direct URL, construct it from ID
                    if 'id' in entry:
                        track_url = f"https://www.youtube.com/watch?v={entry['id']}"
                    else:
                        results['failed'].append(f"{track_title} (aucune URL disponible)")
                        continue
                
                st.info(f"Préparation de la piste {idx} sur {total_tracks} : {track_title}")
                
                # Sanitize filename
                sanitized_title = sanitize_filename(track_title)
                final_filename = f"{sanitized_title}.mp3"
                final_path = os.path.join(output_dir, final_filename)
                
                # Configure yt-dlp options for this track
                ydl_opts = {
                    # Most flexible format selection - will accept ANY available format
                    'format': 'bestaudio/best',
                    'format_sort': ['acodec:opus', 'acodec:m4a', 'acodec:mp3'],  # Prefer common codecs
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': os.path.join(output_dir, f'{sanitized_title}.%(ext)s'),
                    'quiet': True,
                    'no_warnings': True,
                    'extractor_args': {'youtube': {'player_client': ['android', 'web', 'ios']}},
                    'http_headers': {'User-Agent': 'Mozilla/5.0'},
                    'ignoreerrors': False,
                    'no_check_certificate': True,
                    'retries': 3,
                    'fragment_retries': 3,
                    'geo_bypass': True,
                    'geo_bypass_country': 'US',
                    'allow_unplayable_formats': False,  # Skip unplayable formats
                    'prefer_free_formats': True,  # Prefer formats that don't require decryption
                }
                
                # Set ffmpeg location if found
                if ffmpeg_path:
                    ydl_opts['ffmpeg_location'] = ffmpeg_path
                
                # Add cookies if available
                cookies_path = get_cookies_path()
                if cookies_path:
                    ydl_opts['cookiefile'] = cookies_path
                
                try:
                    # Download the track
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([track_url])
                    
                    # Verify file was created (yt-dlp converts to .mp3)
                    if os.path.exists(final_path):
                        results['success'].append(track_title)
                    else:
                        # Check for any .mp3 file that might match
                        mp3_files = [f for f in os.listdir(output_dir) if f.endswith('.mp3')]
                        matching_files = [f for f in mp3_files if sanitized_title.lower() in f.lower()]
                        if matching_files:
                            # File exists with slightly different name, rename it
                            old_path = os.path.join(output_dir, matching_files[0])
                            if old_path != final_path:
                                os.rename(old_path, final_path)
                            results['success'].append(track_title)
                        else:
                            results['failed'].append(f"{track_title} (fichier introuvable après téléchargement)")
                            
                except Exception as e:
                    results['failed'].append(f"{track_title} (erreur : {str(e)})")
                    continue
                finally:
                    # Clean up temp cookies file if created
                    if cookies_path and os.path.exists(cookies_path):
                        try:
                            os.unlink(cookies_path)
                        except:
                            pass
            
    except Exception as e:
        st.error(f"Erreur lors du téléchargement : {str(e)}")
        results['failed'].append(f"Échec du téléchargement de la playlist : {str(e)}")
    
    return results


# Main UI (form allows Enter key to submit)
with st.form(key="playlist_form", clear_on_submit=False):
    playlist_url = st.text_input(
        "URL de la playlist YouTube",
        placeholder="https://www.youtube.com/playlist?list=..."
    )
    submit = st.form_submit_button("Trouver les morceaux", type="primary", disabled=st.session_state.downloading)

if submit:
    if not playlist_url:
        st.warning("Entre une URL de playlist YouTube")
    else:
        # Validate URL
        if 'youtube.com' not in playlist_url and 'youtu.be' not in playlist_url:
            st.error("URL YouTube invalide")
        else:
            # Get playlist info first
            with st.spinner("Récupération des informations de la playlist..."):
                info = get_playlist_info(playlist_url)
            
            if info:
                playlist_title = info.get('title', 'Playlist inconnue')
                st.success(f"Playlist trouvée : **{playlist_title}**")
                
                # Create download directory
                downloads_dir = Path("downloads")
                downloads_dir.mkdir(exist_ok=True)
                
                # Create subfolder for this playlist
                playlist_folder_name = sanitize_filename(playlist_title)
                output_dir = downloads_dir / playlist_folder_name
                output_dir.mkdir(exist_ok=True)
                
                # Start download (pass the already-fetched info to avoid duplicate fetch)
                st.session_state.downloading = True
                st.session_state.download_results = {'success': [], 'failed': []}
                st.session_state.downloaded_files = set()
                
                results = download_playlist(playlist_url, str(output_dir), playlist_info=info)
                st.session_state.download_results = results
                st.session_state.current_output_dir = str(output_dir)
                st.session_state.current_playlist_title = playlist_title
                st.session_state.downloading = False
                st.rerun()  # Rerun to show results in the persistent section below

# Show current status
if st.session_state.downloading:
    st.warning("Téléchargement en cours...")

# Display results if available (persists after button click)
if st.session_state.download_results and (st.session_state.download_results.get('success') or st.session_state.download_results.get('failed')):
    results = st.session_state.download_results
    output_dir = Path(st.session_state.get('current_output_dir', 'downloads'))
    playlist_title = st.session_state.get('current_playlist_title', 'Playlist')
    
    st.markdown("---")
    st.success("Préparation terminée ! Les fichiers sont prêts à être téléchargés.")
    
    if results.get('success'):
        st.markdown(f"### ✅ Préparation réussie ({len(results['success'])} pistes)")
        
        # Create ZIP file for download all (only include files from this playlist)
        zip_buffer, zip_name = create_zip_file(str(output_dir), playlist_title, results.get('success', []))
        zip_filename = f"{zip_name}.zip"
        
        # Download All button
        col1, col2 = st.columns([1, 3])
        with col1:
            st.download_button(
                label="📦 Télécharger le ZIP",
                data=zip_buffer.getvalue(),
                file_name=zip_filename,
                mime="application/zip",
                key="download_all_zip",
                type="primary",
                use_container_width=True
            )
        with col2:
            st.info(f"💡 Les fichiers seront enregistrés dans `{output_dir}`.\n\nTélécharge les {len(results['success'])} pistes en un seul fichier ZIP ou individuellement ci-dessous.")
        
        st.markdown("---")
        
        # List downloaded files with download buttons
        with st.expander(f"📥 Télécharger les fichiers préparés ({len(results['success'])} pistes)", expanded=True):
            for idx, track in enumerate(results['success']):
                sanitized_title = sanitize_filename(track)
                file_path = output_dir / f"{sanitized_title}.mp3"
                
                if file_path.exists():
                    download_key = f"download_{sanitized_title}_{idx}"
                    file_id = f"{sanitized_title}_{idx}"
                    is_downloaded = file_id in st.session_state.downloaded_files
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{idx + 1}. {track}**")
                    with col2:
                        # Read file from disk on-demand when button is clicked
                        try:
                            with open(file_path, 'rb') as f:
                                file_data = f.read()
                            
                            button_label = "✅ Téléchargé" if is_downloaded else "⬇️ Télécharger"
                            
                            download_btn = st.download_button(
                                label=button_label,
                                data=file_data,
                                file_name=f"{sanitized_title}.mp3",
                                mime="audio/mpeg",
                                key=download_key,
                                use_container_width=True
                            )
                            
                            # Persist downloaded state on the server side for consistent styling
                            if download_btn:
                                st.session_state.downloaded_files.add(file_id)
                                st.rerun()
                                
                        except Exception as e:
                            st.error(f"Erreur lors de la lecture du fichier : {str(e)}")
                else:
                    st.markdown(f"- {track} (fichier introuvable)")
    
    if results.get('failed'):
        st.markdown(f"### ❌ Téléchargements échoués ({len(results['failed'])} pistes)")
        for track in results['failed']:
            st.markdown(f"- {track}")

    