import os
from flask import Flask, render_template_string, request, send_from_directory, jsonify
from mutagen_proba import proces_song

app = Flask(__name__)


if not os.path.exists("music"):
    os.makedirs("music")


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="sr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moj Muzički Server</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #121212; color: #fff; margin: 0; padding: 20px; text-align: center; }
        h1 { color: #1db954; font-size: 24px; }
        .box { background: #1e1e1e; padding: 15px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        input[type="text"] { width: 80%; padding: 12px; border: none; border-radius: 8px; margin-bottom: 10px; font-size: 16px; background: #2a2a2a; color: #fff; }
        button { background: #1db954; color: white; border: none; padding: 12px 20px; border-radius: 20px; font-weight: bold; font-size: 16px; cursor: pointer; width: 85%; }
        button:disabled { background: #555; }
        ul { list-style: none; padding: 0; text-align: left; }
        li { background: #282828; margin: 8px 0; padding: 10px; border-radius: 8px; display: flex; flex-direction: column; gap: 8px; }
        audio { width: 100%; height: 35px; }
        #status { margin-top: 10px; color: #b3b3b3; font-size: 14px; }
    </style>
</head>
<body>
    <h1>Music Server</h1>
    
    <div class="box">
        <input type="text" id="query" placeholder="Name of song...">
        <button id="btn" onclick="downlSong()">Download and play</button>
        <div id="status"></div>
    </div>

    <div class="box">
        <h3>Download songs on my laptop</h3>
        <ul id="lista">
            {% for song in songs %}
            <li>
                <span> {{ song }}</span>
                <audio controls src="/stream/{{ song }}"></audio>
            </li>
            {% endfor %}
        </ul>
    </div>

    <script>
        async function downlSong() {
            const query = document.getElementById('query').value;
            const status = document.getElementById('status');
            const btn = document.getElementById('btn');
            
            if(!query) return alert("Unesi naziv songs!");

            btn.disabled = true;
            status.innerText = "Downloading song...";

            try {
                const res = await fetch('/download', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: query})
                });
                const data = await res.json();
                
                if(data.status === 'ok') {
                    status.innerText = "Song is ready!";
                    document.getElementById('query').value = '';
                    location.reload(); // Osvežavamo listu
                } else {
                    status.innerText = "Error: " + data.message;
                }
            } catch(e) {
                status.innerText = "Errorv2.";
            }
            btn.disabled = false;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    songs = [f for f in os.listdir("music") if f.endswith(".mp3")]
    return render_template_string(HTML_TEMPLATE, songs=songs)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    query = data.get('query')
    try:
        proces_song(query) 
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stream/<filename>')
def stream(filename):
    return send_from_directory("music", filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)