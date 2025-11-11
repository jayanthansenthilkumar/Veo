"""
Video Generation Agent
Refactored for Flask integration with Google's Veo API
"""

from google import genai
from google.genai import types
import time
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VideoAgent:
    """Agent for generating videos using Google's Veo model"""
    
    def __init__(self, model='veo-3.1-generate-preview'):
        """Initialize the video agent"""
        api_key = os.environ.get('GOOGLE_API_KEY')
        self.client = genai.Client(api_key=api_key)
        self.model = model
    
    def generate_video(self, prompt, negative_prompt='', resolution='720p', 
                      output_dir=None, max_wait_time=600):
        """
        Generate video based on text prompt
        
        Args:
            prompt (str): Text description of the video
            negative_prompt (str): What to avoid in the video
            resolution (str): Video resolution ('720p' or '1080p')
            output_dir (str): Directory to save generated video
            max_wait_time (int): Maximum time to wait for generation (seconds)
            
        Returns:
            dict: Result dictionary with success status and video path
        """
        try:
            # Create output directory if needed
            if output_dir:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            else:
                output_dir = 'outputs/videos'
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Configure generation
            config = types.GenerateVideosConfig(
                number_of_videos=1,
                resolution=resolution
            )
            
            if negative_prompt:
                config.negative_prompt = negative_prompt
            
            # Start video generation
            operation = self.client.models.generate_videos(
                model=self.model,
                prompt=prompt,
                config=config
            )
            
            # Poll for completion
            elapsed_time = 0
            while not operation.done and elapsed_time < max_wait_time:
                time.sleep(10)
                elapsed_time += 10
                operation = self.client.operations.get(operation)
            
            if not operation.done:
                return {
                    'success': False,
                    'error': 'Video generation timeout',
                    'video_path': None
                }
            
            # Download the generated video
            generated_video = operation.response.generated_videos[0]
            self.client.files.download(file=generated_video.video)
            
            # Save to output directory
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"video_{timestamp}.mp4"
            filepath = os.path.join(output_dir, filename)
            
            generated_video.video.save(filepath)
            
            return {
                'success': True,
                'video_path': filepath,
                'output_dir': output_dir
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'video_path': None
            }
    
    def generate_video_with_image(self, prompt, image_path, output_dir=None):
        """
        Generate video starting from an image
        
        Args:
            prompt (str): Text description
            image_path (str): Path to input image
            output_dir (str): Directory to save generated video
            
        Returns:
            dict: Result with success status and video path
        """
        try:
            if output_dir:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            else:
                output_dir = 'outputs/videos'
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Load image
            from PIL import Image
            img = Image.open(image_path)
            
            # Generate video
            operation = self.client.models.generate_videos(
                model=self.model,
                prompt=prompt,
                image=img,
            )
            
            # Poll for completion
            while not operation.done:
                time.sleep(10)
                operation = self.client.operations.get(operation)
            
            # Save video
            generated_video = operation.response.generated_videos[0]
            self.client.files.download(file=generated_video.video)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"video_from_image_{timestamp}.mp4"
            filepath = os.path.join(output_dir, filename)
            
            generated_video.video.save(filepath)
            
            return {
                'success': True,
                'video_path': filepath,
                'output_dir': output_dir
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'video_path': None
            }
    
    def extend_video(self, prompt, video_path, output_dir=None):
        """
        Extend an existing video with new content
        
        Args:
            prompt (str): Description for the extension
            video_path (str): Path to existing video
            output_dir (str): Directory to save extended video
            
        Returns:
            dict: Result with success status and video path
        """
        try:
            if output_dir:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            else:
                output_dir = 'outputs/videos'
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate extended video
            operation = self.client.models.generate_videos(
                model=self.model,
                video=video_path,
                prompt=prompt,
                config=types.GenerateVideosConfig(
                    number_of_videos=1,
                    resolution="720p"
                ),
            )
            
            # Poll for completion
            while not operation.done:
                time.sleep(10)
                operation = self.client.operations.get(operation)
            
            # Save video
            generated_video = operation.response.generated_videos[0]
            self.client.files.download(file=generated_video.video)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"video_extended_{timestamp}.mp4"
            filepath = os.path.join(output_dir, filename)
            
            generated_video.video.save(filepath)
            
            return {
                'success': True,
                'video_path': filepath,
                'output_dir': output_dir
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'video_path': None
            }
