import os
from flask import Flask, render_template_string, request, jsonify, send_file
import yt_dlp
import uuid
from flask import render_template
app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ================= FRONTEND =================

# ================= ROUTES =================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')

    if not url:
        return jsonify({"success": False, "message": "No URL provided"})

    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{file_id}.mp4")

        ydl_opts = {
            'format': 'best',
            'outtmpl': file_path,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        return jsonify({
            "success": True,
            "file": f"/get-file/{file_id}",
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail")
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/get-file/<file_id>')
def get_file(file_id):
    file_path = os.path.join(DOWNLOAD_FOLDER, f"{file_id}.mp4")

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)

    return "File not found"

# ================= RUN =================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
