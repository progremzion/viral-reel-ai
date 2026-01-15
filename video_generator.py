"""
ViralReel AI - Video Generator
This module handles text-to-video generation using the RunwayML API.
Converts visual descriptions into short video clips for each scene.
"""

import os
import requests
import time
from typing import List, Dict, Optional


class VideoGenerator:
    """
    Handles video generation using RunwayML API (Gen-2 or Gen-3).
    """

    def __init__(self, api_key: str):
        """
        Initialize the video generator.

        Args:
            api_key: RunwayML API key
        """
        self.api_key = api_key
        # RunwayML API endpoint (must use dev subdomain)
        self.base_url = "https://api.dev.runwayml.com/v1"

        # API headers
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Runway-Version": "2024-11-06"  # Required API version header
        }

    def generate_video(self, prompt: str, output_path: str, duration: int = 4,
                      aspect_ratio: str = "9:16") -> bool:
        """
        Generate a video from a text prompt.

        Args:
            prompt: Text description of the video to generate
            output_path: Path where the video file should be saved
            duration: Video duration in seconds (typically 4-10 seconds)
            aspect_ratio: Video aspect ratio ("16:9", "9:16", or "1:1")

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Step 1: Create video generation task
            # Updated to match RunwayML API v1 spec
            # Map aspect ratio to resolution
            ratio_map = {
                "9:16": "720:1280",  # Portrait
                "16:9": "1280:720",  # Landscape
                "1:1": "1024:1024"   # Square
            }

            # Adjust duration to valid values for the model
            # veo3* models support 8 seconds
            # gen4.5 supports 5, 8, 10 seconds
            valid_duration = 8 if duration >= 6 else 8  # Default to 8 seconds

            create_payload = {
                "model": "veo3.1_fast",  # Fast model, good quality
                "promptText": prompt,
                "ratio": ratio_map.get(aspect_ratio, "720:1280"),
                "duration": valid_duration
            }

            print(f"Creating video generation task for prompt: '{prompt[:50]}...'")

            create_response = requests.post(
                f"{self.base_url}/text_to_video",  # Note: underscore, not hyphen
                json=create_payload,
                headers=self.headers
            )

            if create_response.status_code not in [200, 201]:
                print(f"RunwayML API error: {create_response.status_code} - {create_response.text}")
                return False

            task_data = create_response.json()
            task_id = task_data.get('id')

            if not task_id:
                print("Failed to get task ID from RunwayML response")
                return False

            print(f"Task created with ID: {task_id}")

            # Step 2: Poll for completion
            max_attempts = 120  # 10 minutes max wait time
            poll_interval = 5  # Check every 5 seconds

            for attempt in range(max_attempts):
                time.sleep(poll_interval)

                # Check task status
                status_response = requests.get(
                    f"{self.base_url}/tasks/{task_id}",
                    headers=self.headers
                )

                if status_response.status_code != 200:
                    print(f"Error checking task status: {status_response.status_code}")
                    continue

                status_data = status_response.json()
                status = status_data.get('status')

                print(f"Task status: {status} (attempt {attempt + 1}/{max_attempts})")

                if status == 'SUCCEEDED':
                    # Get the video URL
                    video_url = status_data.get('output', [None])[0]

                    if not video_url:
                        print("No video URL in completed task")
                        return False

                    # Step 3: Download the video
                    print(f"Downloading video from: {video_url}")
                    video_response = requests.get(video_url)

                    if video_response.status_code == 200:
                        with open(output_path, 'wb') as video_file:
                            video_file.write(video_response.content)

                        print(f"Video saved to: {output_path}")
                        return True
                    else:
                        print(f"Failed to download video: {video_response.status_code}")
                        return False

                elif status == 'FAILED':
                    error_msg = status_data.get('error', 'Unknown error')
                    print(f"Video generation failed: {error_msg}")
                    return False

                elif status in ['PENDING', 'RUNNING']:
                    # Continue polling
                    continue

            print(f"Video generation timed out after {max_attempts * poll_interval} seconds")
            return False

        except Exception as e:
            print(f"Error generating video: {str(e)}")
            return False

    def generate_scene_videos(self, scenes: List[Dict], output_dir: str = "temp/video",
                             duration_per_scene: int = 4) -> List[str]:
        """
        Generate videos for all scenes in a script.

        Args:
            scenes: List of scene dictionaries containing 'visuals' and 'scene_number'
            output_dir: Directory where video files should be saved
            duration_per_scene: Duration in seconds for each scene video

        Returns:
            List[str]: List of paths to generated video files
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        video_files = []

        for scene in scenes:
            scene_number = scene.get('scene_number', 0)
            visuals = scene.get('visuals', '').strip()

            if not visuals:
                print(f"Warning: Scene {scene_number} has no visual description")
                continue

            # Generate filename
            filename = f"scene_{scene_number}_video.mp4"
            output_path = os.path.join(output_dir, filename)

            print(f"\nGenerating video for scene {scene_number}...")

            # Enhance the prompt for better video generation
            enhanced_prompt = self._enhance_video_prompt(visuals)

            # Generate the video
            success = self.generate_video(
                enhanced_prompt,
                output_path,
                duration=duration_per_scene,
                aspect_ratio="9:16"  # Vertical format for social media
            )

            if success:
                video_files.append(output_path)
            else:
                print(f"Failed to generate video for scene {scene_number}")
                # Return empty list to indicate failure
                return []

        return video_files

    def _enhance_video_prompt(self, base_prompt: str) -> str:
        """
        Enhance the video prompt with additional details for better generation.

        Args:
            base_prompt: Original visual description

        Returns:
            str: Enhanced prompt
        """
        # Add cinematic and quality keywords
        enhancements = [
            "cinematic",
            "high quality",
            "smooth camera movement",
            "professional lighting",
            "detailed"
        ]

        # Check if prompt already has quality descriptors
        lower_prompt = base_prompt.lower()
        missing_enhancements = [e for e in enhancements if e not in lower_prompt]

        if missing_enhancements and len(base_prompt) < 200:
            # Add a couple of enhancements without making it too long
            enhanced = f"{base_prompt}, {', '.join(missing_enhancements[:2])}"
            return enhanced

        return base_prompt


# Convenience function for easy usage
def generate_videos_for_script(scenes: List[Dict], api_key: Optional[str] = None,
                               output_dir: str = "temp/video",
                               duration_per_scene: int = 4) -> List[str]:
    """
    Convenience function to generate videos for a complete script.

    Args:
        scenes: List of scene dictionaries from the script
        api_key: RunwayML API key (will use env var if not provided)
        output_dir: Directory to save video files
        duration_per_scene: Duration in seconds for each scene

    Returns:
        List[str]: Paths to generated video files
    """
    if api_key is None:
        api_key = os.getenv('RUNWAYML_API_KEY')

    if not api_key:
        raise ValueError("RunwayML API key not provided and not found in environment")

    generator = VideoGenerator(api_key)
    return generator.generate_scene_videos(scenes, output_dir, duration_per_scene)


# Example usage (for testing)
if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    # Example scenes
    test_scenes = [
        {
            "scene_number": 1,
            "visuals": "A futuristic city skyline at night with glowing neon lights and flying cars",
            "narration": "Welcome to the future of artificial intelligence."
        },
        {
            "scene_number": 2,
            "visuals": "A humanoid robot collaborating with a scientist in a modern laboratory",
            "narration": "Where machines and humans work together seamlessly."
        }
    ]

    # Generate videos
    print("Starting video generation...")
    video_files = generate_videos_for_script(test_scenes, duration_per_scene=4)

    if video_files:
        print(f"\nSuccessfully generated {len(video_files)} videos:")
        for file in video_files:
            print(f"  - {file}")
    else:
        print("\nFailed to generate videos")
