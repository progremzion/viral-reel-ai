"""
ViralReel AI - Fallback Voiceover Generator using gTTS
This is a free alternative when ElevenLabs is not available.
Uses Google Text-to-Speech (gTTS) - free but more robotic voice.
"""

import os
from typing import List, Dict
from gtts import gTTS
import time


class VoiceoverGeneratorGTTS:
    """
    Fallback voiceover generator using Google TTS (free).
    """

    def __init__(self):
        """Initialize the gTTS generator."""
        pass

    def generate_voiceover(self, text: str, output_path: str, lang: str = 'en',
                          slow: bool = False) -> bool:
        """
        Generate a voiceover from text using gTTS.

        Args:
            text: The text to convert to speech
            output_path: Path where the audio file should be saved
            lang: Language code (default: 'en' for English)
            slow: Whether to speak slowly

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"Generating voiceover with gTTS...")

            # Create gTTS object
            tts = gTTS(text=text, lang=lang, slow=slow)

            # Save to file
            tts.save(output_path)

            print(f"Voiceover saved to: {output_path}")
            return True

        except Exception as e:
            print(f"Error generating voiceover: {str(e)}")
            return False

    def generate_scene_voiceovers(self, scenes: List[Dict], output_dir: str = "temp/audio") -> List[str]:
        """
        Generate voiceovers for all scenes in a script.

        Args:
            scenes: List of scene dictionaries containing 'narration' and 'scene_number'
            output_dir: Directory where audio files should be saved

        Returns:
            List[str]: List of paths to generated audio files
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        audio_files = []

        for scene in scenes:
            scene_number = scene.get('scene_number', 0)
            narration = scene.get('narration', '').strip()

            if not narration:
                print(f"Warning: Scene {scene_number} has no narration text")
                continue

            # Generate filename
            filename = f"scene_{scene_number}_voiceover.mp3"
            output_path = os.path.join(output_dir, filename)

            print(f"Generating voiceover for scene {scene_number}...")

            # Generate the voiceover
            success = self.generate_voiceover(narration, output_path)

            if success:
                audio_files.append(output_path)
            else:
                print(f"Failed to generate voiceover for scene {scene_number}")
                return []

            # Small delay to be respectful
            time.sleep(0.3)

        return audio_files


# Convenience function
def generate_voiceovers_for_script_gtts(scenes: List[Dict], output_dir: str = "temp/audio") -> List[str]:
    """
    Generate voiceovers using free gTTS.

    Args:
        scenes: List of scene dictionaries from the script
        output_dir: Directory to save audio files

    Returns:
        List[str]: Paths to generated audio files
    """
    generator = VoiceoverGeneratorGTTS()
    return generator.generate_scene_voiceovers(scenes, output_dir)


if __name__ == "__main__":
    # Test
    test_scenes = [
        {
            "scene_number": 1,
            "narration": "Welcome to ViralReel AI. This is a test of the fallback voiceover system."
        }
    ]

    audio_files = generate_voiceovers_for_script_gtts(test_scenes, "temp/audio")

    if audio_files:
        print(f"\n✅ Generated {len(audio_files)} voiceovers with gTTS")
    else:
        print("\n❌ Failed to generate voiceovers")
