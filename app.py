from flask import Flask, send_file, request
import yt_dlp
import os

app = Flask(__name__)
OUTPUT_DIR = "/tmp"

@app.route('/download')
def download_video():
    url = request.args.get('url')
    if not url:
        return "❌ URL manquante", 400

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{OUTPUT_DIR}/%(id)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            mp4_file = os.path.splitext(filename)[0] + '.mp4'
            
            if not os.path.exists(mp4_file):
                return "❌ Fichier non généré", 500
                
            return send_file(mp4_file, as_attachment=True, download_name="video.mp4")
    except Exception as e:
        return f"❌ Erreur : {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
