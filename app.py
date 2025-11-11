"""
Gen AI Platform - Flask Application
Main application file for the AI content generation platform
"""

from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import uuid
from pathlib import Path

# Import custom agents
from agents.image_agent import ImageAgent
from agents.video_agent import VideoAgent
from agents.music_agent import MusicAgent
from database import db, Generation, User, init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///genai_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Initialize database
db.init_app(app)

# Create necessary folders
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)
Path(os.path.join(app.config['OUTPUT_FOLDER'], 'images')).mkdir(exist_ok=True)
Path(os.path.join(app.config['OUTPUT_FOLDER'], 'videos')).mkdir(exist_ok=True)
Path(os.path.join(app.config['OUTPUT_FOLDER'], 'music')).mkdir(exist_ok=True)

# Initialize agents
image_agent = ImageAgent()
video_agent = VideoAgent()
music_agent = MusicAgent()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/image-generator')
def image_generator():
    """Image generation page"""
    return render_template('image_generator.html')

@app.route('/video-generator')
def video_generator():
    """Video generation page"""
    return render_template('video_generator.html')

@app.route('/music-generator')
def music_generator():
    """Music generation page"""
    return render_template('music_generator.html')

@app.route('/history')
def history():
    """Generation history page"""
    generations = Generation.query.order_by(Generation.created_at.desc()).limit(50).all()
    return render_template('history.html', generations=generations)

@app.route('/api/generate-image', methods=['POST'])
def api_generate_image():
    """API endpoint for image generation"""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        num_images = int(data.get('num_images', 1))
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Generate unique session ID
        generation_id = str(uuid.uuid4())
        
        # Generate images
        result = image_agent.generate_images(
            prompt=prompt,
            num_images=min(num_images, 4),
            output_dir=os.path.join(app.config['OUTPUT_FOLDER'], 'images', generation_id)
        )
        
        if result['success']:
            # Save to database
            generation = Generation(
                id=generation_id,
                type='image',
                prompt=prompt,
                parameters=json.dumps({'num_images': num_images}),
                output_path=result['output_dir'],
                status='completed'
            )
            db.session.add(generation)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'generation_id': generation_id,
                'images': result['images'],
                'message': f'Generated {len(result["images"])} images successfully'
            })
        else:
            return jsonify({'error': result.get('error', 'Generation failed')}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-video', methods=['POST'])
def api_generate_video():
    """API endpoint for video generation"""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        negative_prompt = data.get('negative_prompt', '')
        resolution = data.get('resolution', '720p')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        generation_id = str(uuid.uuid4())
        
        # Generate video
        result = video_agent.generate_video(
            prompt=prompt,
            negative_prompt=negative_prompt,
            resolution=resolution,
            output_dir=os.path.join(app.config['OUTPUT_FOLDER'], 'videos', generation_id)
        )
        
        if result['success']:
            # Save to database
            generation = Generation(
                id=generation_id,
                type='video',
                prompt=prompt,
                parameters=json.dumps({
                    'negative_prompt': negative_prompt,
                    'resolution': resolution
                }),
                output_path=result['video_path'],
                status='completed'
            )
            db.session.add(generation)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'generation_id': generation_id,
                'video_path': result['video_path'],
                'message': 'Video generated successfully'
            })
        else:
            return jsonify({'error': result.get('error', 'Generation failed')}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-music', methods=['POST'])
def api_generate_music():
    """API endpoint for music generation"""
    try:
        data = request.json
        prompts = data.get('prompts', [])
        bpm = int(data.get('bpm', 120))
        temperature = float(data.get('temperature', 1.0))
        duration = int(data.get('duration', 30))
        
        if not prompts:
            return jsonify({'error': 'At least one prompt is required'}), 400
        
        generation_id = str(uuid.uuid4())
        
        # Generate music
        result = music_agent.generate_music(
            prompts=prompts,
            bpm=bpm,
            temperature=temperature,
            duration=duration,
            output_dir=os.path.join(app.config['OUTPUT_FOLDER'], 'music', generation_id)
        )
        
        if result['success']:
            # Save to database
            generation = Generation(
                id=generation_id,
                type='music',
                prompt=', '.join([p.get('text', '') for p in prompts]),
                parameters=json.dumps({
                    'prompts': prompts,
                    'bpm': bpm,
                    'temperature': temperature,
                    'duration': duration
                }),
                output_path=result['audio_path'],
                status='completed'
            )
            db.session.add(generation)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'generation_id': generation_id,
                'audio_path': result['audio_path'],
                'message': 'Music generated successfully'
            })
        else:
            return jsonify({'error': result.get('error', 'Generation failed')}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generations/<generation_id>')
def get_generation(generation_id):
    """Get details of a specific generation"""
    generation = Generation.query.get(generation_id)
    if generation:
        return jsonify({
            'id': generation.id,
            'type': generation.type,
            'prompt': generation.prompt,
            'parameters': json.loads(generation.parameters),
            'status': generation.status,
            'created_at': generation.created_at.isoformat(),
            'output_path': generation.output_path
        })
    return jsonify({'error': 'Generation not found'}), 404

@app.route('/outputs/<path:filename>')
def serve_output(filename):
    """Serve generated files"""
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename))

@app.route('/api/stats')
def get_stats():
    """Get platform statistics"""
    total_generations = Generation.query.count()
    image_count = Generation.query.filter_by(type='image').count()
    video_count = Generation.query.filter_by(type='video').count()
    music_count = Generation.query.filter_by(type='music').count()
    
    return jsonify({
        'total_generations': total_generations,
        'image_generations': image_count,
        'video_generations': video_count,
        'music_generations': music_count
    })

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
