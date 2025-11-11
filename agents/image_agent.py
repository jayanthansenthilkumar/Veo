"""
Image Generation Agent
Refactored for Flask integration with Google's Imagen API
"""

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ImageAgent:
    """Agent for generating images using Google's Imagen model"""
    
    def __init__(self, model='imagen-4.0-generate-001'):
        """Initialize the image agent"""
        api_key = os.environ.get('GOOGLE_API_KEY')
        self.client = genai.Client(api_key=api_key)
        self.model = model
    
    def generate_images(self, prompt, num_images=1, output_dir=None):
        """
        Generate images based on text prompt
        
        Args:
            prompt (str): Text description of the image to generate
            num_images (int): Number of images to generate (1-4)
            output_dir (str): Directory to save generated images
            
        Returns:
            dict: Result dictionary with success status and image paths
        """
        try:
            # Validate inputs
            num_images = max(1, min(num_images, 4))
            
            # Create output directory if needed
            if output_dir:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            else:
                output_dir = 'outputs/images'
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate images
            response = self.client.models.generate_images(
                model=self.model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=num_images,
                )
            )
            
            # Save images and collect paths
            image_paths = []
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            for idx, generated_image in enumerate(response.generated_images):
                filename = f"image_{timestamp}_{idx+1}.png"
                filepath = os.path.join(output_dir, filename)
                
                # Save image
                generated_image.image.save(filepath)
                image_paths.append(filepath)
            
            return {
                'success': True,
                'images': image_paths,
                'output_dir': output_dir,
                'count': len(image_paths)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'images': []
            }
    
    def generate_single_image(self, prompt, output_path=None):
        """
        Generate a single image
        
        Args:
            prompt (str): Text description
            output_path (str): Full path for output file
            
        Returns:
            dict: Result with success status and image path
        """
        result = self.generate_images(prompt, num_images=1)
        
        if result['success'] and output_path:
            # Move to specified path
            import shutil
            shutil.move(result['images'][0], output_path)
            result['images'][0] = output_path
        
        return result
    
    def get_image_bytes(self, prompt):
        """
        Generate image and return as bytes
        
        Args:
            prompt (str): Text description
            
        Returns:
            bytes: Image data as bytes
        """
        try:
            response = self.client.models.generate_images(
                model=self.model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                )
            )
            
            # Get first image
            img = response.generated_images[0].image
            
            # Convert to bytes
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            return img_byte_arr.getvalue()
            
        except Exception as e:
            raise Exception(f"Failed to generate image: {str(e)}")
