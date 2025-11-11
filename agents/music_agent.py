"""
Music Generation Agent
Refactored for Flask integration with Google's Lyria API
"""

import asyncio
from google import genai
from google.genai import types
import os
from pathlib import Path
from datetime import datetime
import wave
import io
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MusicAgent:
    """Agent for generating music using Google's Lyria model"""
    
    def __init__(self, model='models/lyria-realtime-exp'):
        """Initialize the music agent"""
        api_key = os.environ.get('GOOGLE_API_KEY')
        self.client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})
        self.model = model
    
    def generate_music(self, prompts, bpm=120, temperature=1.0, 
                      duration=30, output_dir=None):
        """
        Generate music based on text prompts
        
        Args:
            prompts (list): List of prompt dictionaries with 'text' and 'weight'
            bpm (int): Beats per minute (60-180)
            temperature (float): Generation temperature (0.0-2.0)
            duration (int): Duration in seconds
            output_dir (str): Directory to save generated audio
            
        Returns:
            dict: Result dictionary with success status and audio path
        """
        try:
            # Create output directory if needed
            if output_dir:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            else:
                output_dir = 'outputs/music'
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Run async generation
            result = asyncio.run(self._async_generate_music(
                prompts, bpm, temperature, duration, output_dir
            ))
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'audio_path': None
            }
    
    async def _async_generate_music(self, prompts, bpm, temperature, duration, output_dir):
        """Async function to generate music"""
        try:
            audio_chunks = []
            
            async def receive_audio(session):
                """Receive and collect audio chunks"""
                nonlocal audio_chunks
                start_time = asyncio.get_event_loop().time()
                
                while True:
                    async for message in session.receive():
                        if hasattr(message, 'server_content') and message.server_content.audio_chunks:
                            audio_data = message.server_content.audio_chunks[0].data
                            audio_chunks.append(audio_data)
                        
                        # Stop after specified duration
                        elapsed = asyncio.get_event_loop().time() - start_time
                        if elapsed >= duration:
                            return
                        
                        await asyncio.sleep(0.1)
            
            # Convert prompts to WeightedPrompt objects
            weighted_prompts = []
            for p in prompts:
                if isinstance(p, dict):
                    weighted_prompts.append(
                        types.WeightedPrompt(
                            text=p.get('text', ''),
                            weight=p.get('weight', 1.0)
                        )
                    )
                else:
                    weighted_prompts.append(
                        types.WeightedPrompt(text=str(p), weight=1.0)
                    )
            
            # Generate music
            async with (
                self.client.aio.live.music.connect(model=self.model) as session,
                asyncio.TaskGroup() as tg,
            ):
                # Start receiving audio
                receive_task = tg.create_task(receive_audio(session))
                
                # Set configuration
                await session.set_weighted_prompts(prompts=weighted_prompts)
                await session.set_music_generation_config(
                    config=types.LiveMusicGenerationConfig(
                        bpm=max(60, min(bpm, 180)),
                        temperature=max(0.0, min(temperature, 2.0))
                    )
                )
                
                # Start playing
                await session.play()
                
                # Wait for duration
                await asyncio.sleep(duration)
                
                # Stop session
                await session.stop()
            
            # Save audio chunks to file
            if audio_chunks:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"music_{timestamp}.wav"
                filepath = os.path.join(output_dir, filename)
                
                # Combine audio chunks and save
                combined_audio = b''.join(audio_chunks)
                
                with open(filepath, 'wb') as f:
                    f.write(combined_audio)
                
                return {
                    'success': True,
                    'audio_path': filepath,
                    'output_dir': output_dir,
                    'duration': duration
                }
            else:
                return {
                    'success': False,
                    'error': 'No audio data received',
                    'audio_path': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'audio_path': None
            }
    
    def generate_simple_music(self, prompt, bpm=120, duration=30, output_dir=None):
        """
        Simple music generation with a single prompt
        
        Args:
            prompt (str): Music description
            bpm (int): Beats per minute
            duration (int): Duration in seconds
            output_dir (str): Output directory
            
        Returns:
            dict: Result with success status and audio path
        """
        prompts = [{'text': prompt, 'weight': 1.0}]
        return self.generate_music(prompts, bpm=bpm, duration=duration, output_dir=output_dir)
