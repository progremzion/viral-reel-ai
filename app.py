"""
ViralReel AI - Main Flask Application
This is the main backend server that handles all API requests and orchestrates
the video generation process.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import uuid
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Import our custom modules
from voiceover_generator import generate_voiceovers_for_script
from voiceover_generator_gtts import generate_voiceovers_for_script_gtts
from video_generator import generate_videos_for_script
from video_assembler import assemble_final_video

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configuration
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure required directories exist
os.makedirs('temp/audio', exist_ok=True)
os.makedirs('temp/video', exist_ok=True)
os.makedirs('static/videos', exist_ok=True)


@app.route('/')
def index():
    """
    Main route that serves the homepage.
    Returns: Rendered HTML template for the main interface
    """
    return render_template('index.html')


@app.route('/health')
def health_check():
    """
    Health check endpoint to verify the server is running.
    Returns: JSON response with status
    """
    return jsonify({
        'status': 'ok',
        'message': 'ViralReel AI server is running'
    })


@app.route('/static/videos/<path:filename>')
def serve_video(filename):
    """
    Serve generated video files.
    Args:
        filename: Name of the video file to serve
    Returns: Video file
    """
    return send_from_directory('static/videos', filename)


@app.route('/generate-script', methods=['POST'])
def generate_script():
    """
    Generate a video script using OpenAI GPT-4o-mini.
    Expects JSON body with 'topic' field.
    Returns: JSON with structured script containing scenes with visuals and narration
    """
    try:
        # Get topic from request
        data = request.get_json()
        topic = data.get('topic', '').strip()

        if not topic:
            return jsonify({'error': 'Topic is required'}), 400

        # Create prompt for script generation
        system_prompt = """You are an expert short-form video script writer specializing in viral content for TikTok, Instagram Reels, and YouTube Shorts.

Your task is to create engaging 30-60 second video scripts that:
- Hook viewers in the first 3 seconds
- Are structured into 3-5 clear scenes
- Include specific visual descriptions for each scene
- Have concise, punchy narration
- End with a strong call-to-action or memorable conclusion

Return ONLY a valid JSON object with this exact structure:
{
  "scenes": [
    {
      "scene_number": 1,
      "visuals": "Detailed description of what should be shown visually",
      "narration": "Exact words to be spoken in the voiceover"
    }
  ]
}"""

        user_prompt = f"Create a viral short-form video script about: {topic}"

        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )

        # Parse the response
        script_content = response.choices[0].message.content
        script_data = json.loads(script_content)

        # Validate the script structure
        if 'scenes' not in script_data or not isinstance(script_data['scenes'], list):
            raise ValueError('Invalid script structure returned from API')

        # Ensure scene numbers are correct
        for idx, scene in enumerate(script_data['scenes'], 1):
            scene['scene_number'] = idx

        return jsonify(script_data), 200

    except json.JSONDecodeError as e:
        return jsonify({'error': f'Failed to parse script response: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Script generation failed: {str(e)}'}), 500


@app.route('/create-video', methods=['POST'])
def create_video():
    """
    Main endpoint to orchestrate the entire video creation process.
    Takes a topic, generates script, creates voiceovers and videos, then assembles
    everything into a final video.

    Expects JSON body with 'topic' field.
    Returns: JSON with video_url to the final generated video
    """
    try:
        # Step 1: Get topic from request
        data = request.get_json()
        topic = data.get('topic', '').strip()

        if not topic:
            return jsonify({'error': 'Topic is required'}), 400

        print(f"\n{'='*60}")
        print(f"Starting video creation for topic: {topic}")
        print(f"{'='*60}\n")

        # Generate unique ID for this video
        video_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Step 2: Generate script using OpenAI
        print("Step 1/4: Generating script with OpenAI GPT-4o-mini...")

        system_prompt = """You are an expert short-form video script writer specializing in viral content for TikTok, Instagram Reels, and YouTube Shorts.

Your task is to create engaging 30-60 second video scripts that:
- Hook viewers in the first 3 seconds
- Are structured into 3-5 clear scenes
- Include specific visual descriptions for each scene
- Have concise, punchy narration
- End with a strong call-to-action or memorable conclusion

Return ONLY a valid JSON object with this exact structure:
{
  "scenes": [
    {
      "scene_number": 1,
      "visuals": "Detailed description of what should be shown visually",
      "narration": "Exact words to be spoken in the voiceover"
    }
  ]
}"""

        user_prompt = f"Create a viral short-form video script about: {topic}"

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )

        script_content = response.choices[0].message.content
        script_data = json.loads(script_content)
        scenes = script_data.get('scenes', [])

        if not scenes:
            return jsonify({'error': 'Failed to generate valid script'}), 500

        # Ensure scene numbers are correct
        for idx, scene in enumerate(scenes, 1):
            scene['scene_number'] = idx

        print(f"✓ Generated script with {len(scenes)} scenes")

        # Step 3: Generate voiceovers for each scene
        print("\nStep 2/4: Generating voiceovers with gTTS (free)...")
        print("Note: Using free Google TTS. Voice will be more robotic than ElevenLabs.")

        # Use gTTS as fallback (free, no API key needed)
        audio_files = generate_voiceovers_for_script_gtts(
            scenes,
            output_dir=f"temp/audio/{video_id}"
        )

        if not audio_files:
            return jsonify({'error': 'Failed to generate voiceovers'}), 500

        print(f"✓ Generated {len(audio_files)} voiceover files")

        # Step 4: Generate video clips for each scene
        print("\nStep 3/4: Generating video clips with RunwayML...")
        print("(This may take several minutes...)")

        video_files = generate_videos_for_script(
            scenes,
            api_key=os.getenv('RUNWAYML_API_KEY'),
            output_dir=f"temp/video/{video_id}",
            duration_per_scene=4
        )

        if not video_files:
            return jsonify({'error': 'Failed to generate video clips'}), 500

        print(f"✓ Generated {len(video_files)} video clips")

        # Step 5: Assemble final video
        print("\nStep 4/4: Assembling final video...")

        final_video_name = f"viralreel_{timestamp}_{video_id}.mp4"
        final_video_path = os.path.join('static', 'videos', final_video_name)

        # Extract narrations for captions
        narrations = [scene.get('narration', '') for scene in scenes]

        success = assemble_final_video(
            video_files,
            audio_files,
            narrations,
            final_video_path,
            add_captions=True
        )

        if not success:
            return jsonify({'error': 'Failed to assemble final video'}), 500

        print(f"✓ Final video saved to: {final_video_path}")

        # Generate URL for the video
        video_url = f"/static/videos/{final_video_name}"

        print(f"\n{'='*60}")
        print(f"VIDEO CREATION COMPLETE!")
        print(f"Video URL: {video_url}")
        print(f"{'='*60}\n")

        return jsonify({
            'success': True,
            'video_url': video_url,
            'video_id': video_id,
            'scenes_count': len(scenes),
            'message': 'Video created successfully!'
        }), 200

    except Exception as e:
        print(f"\n❌ Error creating video: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Video creation failed: {str(e)}'}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Run the Flask development server
    # Debug mode is enabled for development (should be False in production)
    port = int(os.getenv('PORT', 5001))  # Use port 5001 to avoid conflicts
    app.run(
        debug=True,
        host='0.0.0.0',  # Makes server accessible from any IP
        port=port
    )
