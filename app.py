from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from yt_data import get_video_transcript
from summarize import summarize_transcription
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'downloads'

# Create downloads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process():
    try:
        # Get form data
        video_url = request.form.get('video_url')
        summary_type = request.form.get('summary_type', 'paragraph')
        summary_length = request.form.get('summary_length', 'medium')
        
        if not video_url:
            return jsonify({'error': 'Please enter a YouTube URL'}), 400
            
        # Get transcript
        transcript = get_video_transcript(video_url)
        
        if not transcript or transcript.startswith("Error"):
            return jsonify({'error': 'Failed to retrieve transcript'}), 400
            
        # Determine if bullet points are requested
        points = summary_type == 'points'
        
        # Add length parameter to summary function
        summary = summarize_transcription(transcript, summary_length, points)
        
        # Clean up any audio files that may have been created
        for file in os.listdir():
            if file.startswith("audio."):
                try:
                    os.remove(file)
                except:
                    pass
        
        return jsonify({
            'transcript': transcript,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        content = request.form.get('content')
        format_type = request.form.get('format', 'text')
        content_type = request.form.get('content_type', 'transcript')
        
        if not content:
            return jsonify({'error': 'No content to download'}), 400
            
        # Generate a unique filename
        filename = f"{content_type}_{uuid.uuid4()}"
        
        # Set file extension and adjust content based on format
        if format_type == 'markdown':
            file_extension = '.md'
        elif format_type == 'json':
            file_extension = '.json'
            content = json.dumps({'content': content}, indent=2)
        else:
            file_extension = '.txt'
            
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename + file_extension)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
            
        return send_file(filepath, as_attachment=True, download_name=f"{content_type}{file_extension}")
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
