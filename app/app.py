# importing important tools for the app 
from flask import Flask, request, redirect, url_for, render_template, send_file, flash, jsonify
import os
import re
import yt_dlp

# turning on the app 
app = Flask(__name__)
app.secret_key = 'fsdjfnsdkfnsdksd,nfs'

# making 'downloads' folder for the videos 
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# a function for clearing up messy file names
# substitute the not allowed symbols with empty strings 
def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '', title)

# the homepage 
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# the download button
@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')

    ydl_opts = {
        'format': 'best',  # Automatically select the best available format
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True  # Ensure only the single video is downloaded
    }

    # downloading the video from YouTube
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)

            video_title = info_dict.get('title', None)
            file_extension = info_dict.get('ext', None)

            sanitized_title = sanitize_filename(video_title)
            
            # putting the title and file extension together 
            video_file = f"{sanitized_title}.{file_extension}"
            video_path = os.path.join(DOWNLOAD_DIR, video_file)

            # Debug: print the file path
            print(f"File path: {video_path}")

            if os.path.exists(video_path):
                print('File found, sending file.')
                return send_file(video_path, as_attachment=True, download_name=video_file)
            else:
                flash("The downloaded file could not be found.")
                return jsonify({"error": "File not found"}), 404

    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# serving for full playlist page
@app.route('/playlist')
def display_download_full_playlist():
    return render_template('playlist.html')

# serving to download the full playlist 
@app.route('/download_playlist', methods=['POST'])
def download_full_playlist():
    playlist_url = request.form.get('playlist_url')  # Fetching URL from form input

    if not playlist_url:
        flash("Please provide a valid playlist URL.")
        return redirect(url_for('display_download_full_playlist'))

    def fetch_playlist_videos(playlist_url):
        ydl_opts = {
            'extract_flat': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'cookiefile': 'cookies.txt',  # Path to your cookies file
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            return playlist_info.get('entries', [])  # Use .get() to avoid KeyError

    def download_playlist(playlist_url):
        video_entries = fetch_playlist_videos(playlist_url)
        ydl_opts = {
            'format': 'best',  # Automatically select the best available format
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'cookiefile': 'cookies.txt',  # Path to your cookies file
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for video in video_entries:
                video_url = f"https://www.youtube.com/watch?v={video['id']}"  # Construct video URL
                try:
                    print(f"Downloading {video_url}")
                    ydl.download([video_url])  # Download each video in the playlist
                except Exception as e:
                    print(f"Error downloading {video_url}: {e}")

    try:
        download_playlist(playlist_url)
        flash("Playlist downloaded successfully!")
    except Exception as e:
        flash(f"An error occurred: {str(e)}")

    return redirect(url_for('display_download_full_playlist'))

if __name__ == '__main__':
    app.run(debug=True)
