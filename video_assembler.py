"""
ViralReel AI - Video Assembler
This module handles the final video assembly by combining video clips, audio,
and adding subtitles/captions using MoviePy.
"""

import os
from typing import List, Tuple, Optional
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    TextClip,
    concatenate_videoclips
)
from moviepy.video.fx.all import fadein, fadeout
import tempfile


class VideoAssembler:
    """
    Handles assembling multiple video clips with audio and captions into a final video.
    """

    def __init__(self):
        """Initialize the video assembler."""
        self.temp_dir = tempfile.mkdtemp(prefix="viralreel_")

    def assemble_video(self, video_clips: List[str], audio_clips: List[str],
                      narrations: List[str], output_path: str,
                      add_captions: bool = True) -> bool:
        """
        Assemble multiple video clips with corresponding audio and captions.

        Args:
            video_clips: List of paths to video files
            audio_clips: List of paths to audio files
            narrations: List of narration texts for captions
            output_path: Path where final video should be saved
            add_captions: Whether to add captions/subtitles

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if len(video_clips) != len(audio_clips) or len(video_clips) != len(narrations):
                print("Error: Mismatched number of video clips, audio clips, and narrations")
                return False

            if not video_clips:
                print("Error: No video clips provided")
                return False

            print(f"Assembling {len(video_clips)} scenes into final video...")

            # Process each scene
            processed_clips = []

            for idx, (video_path, audio_path, narration) in enumerate(
                zip(video_clips, audio_clips, narrations), 1
            ):
                print(f"Processing scene {idx}/{len(video_clips)}...")

                # Load video clip
                video_clip = VideoFileClip(video_path)

                # Load audio clip
                audio_clip = AudioFileClip(audio_path)

                # Set the audio duration as the clip duration
                # (trim video to match audio length)
                audio_duration = audio_clip.duration
                video_clip = video_clip.subclip(0, min(video_clip.duration, audio_duration))

                # Set audio to the video
                video_clip = video_clip.set_audio(audio_clip)

                # Add captions if enabled
                if add_captions and narration:
                    video_clip = self._add_caption(video_clip, narration)

                # Add subtle fade transitions
                if idx == 1:
                    # Fade in for first clip
                    video_clip = fadein(video_clip, 0.5)

                if idx == len(video_clips):
                    # Fade out for last clip
                    video_clip = fadeout(video_clip, 0.5)

                processed_clips.append(video_clip)

            # Concatenate all clips
            print("Concatenating clips...")
            final_video = concatenate_videoclips(processed_clips, method="compose")

            # Write the final video
            print(f"Writing final video to {output_path}...")
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                fps=30,
                preset='medium',
                bitrate='8000k',
                audio_bitrate='192k'
            )

            # Clean up
            print("Cleaning up temporary files...")
            for clip in processed_clips:
                clip.close()
            final_video.close()

            print(f"Video assembly complete! Saved to: {output_path}")
            return True

        except Exception as e:
            print(f"Error assembling video: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def _add_caption(self, video_clip: VideoFileClip, text: str,
                    font: str = 'Arial-Bold', fontsize: int = 60,
                    color: str = 'white', bg_color: str = 'black') -> CompositeVideoClip:
        """
        Add caption text overlay to a video clip.

        Args:
            video_clip: The video clip to add captions to
            text: The caption text
            font: Font name
            fontsize: Font size in points
            color: Text color
            bg_color: Background color for text

        Returns:
            CompositeVideoClip: Video with caption overlay
        """
        try:
            # Split text into multiple lines if too long
            max_chars_per_line = 30
            words = text.split()
            lines = []
            current_line = []

            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > max_chars_per_line:
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []

            if current_line:
                lines.append(' '.join(current_line))

            caption_text = '\n'.join(lines)

            # Create text clip
            txt_clip = TextClip(
                caption_text,
                fontsize=fontsize,
                font=font,
                color=color,
                bg_color=bg_color,
                method='caption',
                size=(video_clip.w - 100, None),  # Leave margin on sides
                align='center'
            )

            # Set duration and position
            txt_clip = txt_clip.set_duration(video_clip.duration)

            # Position at bottom center
            txt_clip = txt_clip.set_position(('center', video_clip.h - txt_clip.h - 100))

            # Composite video with text
            return CompositeVideoClip([video_clip, txt_clip])

        except Exception as e:
            print(f"Warning: Failed to add caption: {str(e)}")
            # Return original video if caption fails
            return video_clip

    def add_background_music(self, video_path: str, music_path: str,
                            output_path: str, music_volume: float = 0.1) -> bool:
        """
        Add background music to an existing video.

        Args:
            video_path: Path to the video file
            music_path: Path to the music file
            output_path: Path for output video
            music_volume: Volume of background music (0.0 to 1.0)

        Returns:
            bool: True if successful
        """
        try:
            video = VideoFileClip(video_path)
            music = AudioFileClip(music_path)

            # Loop music if shorter than video
            if music.duration < video.duration:
                music = music.audio_loop(duration=video.duration)
            else:
                music = music.subclip(0, video.duration)

            # Reduce music volume
            music = music.volumex(music_volume)

            # Mix with existing audio
            if video.audio:
                final_audio = video.audio.volumex(1.0)
                # Composite audio not directly supported, would need mixing
                # For now, we'll just use the video audio
                pass

            video_with_music = video.set_audio(music)

            video_with_music.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac'
            )

            video.close()
            music.close()
            video_with_music.close()

            return True

        except Exception as e:
            print(f"Error adding background music: {str(e)}")
            return False


# Convenience function for easy usage
def assemble_final_video(video_clips: List[str], audio_clips: List[str],
                        narrations: List[str], output_path: str,
                        add_captions: bool = True) -> bool:
    """
    Convenience function to assemble a final video from components.

    Args:
        video_clips: List of video file paths
        audio_clips: List of audio file paths
        narrations: List of narration texts
        output_path: Output file path
        add_captions: Whether to add captions

    Returns:
        bool: True if successful
    """
    assembler = VideoAssembler()
    return assembler.assemble_video(
        video_clips,
        audio_clips,
        narrations,
        output_path,
        add_captions
    )


# Example usage (for testing)
if __name__ == "__main__":
    import os

    # Example paths (these would come from previous steps)
    test_videos = [
        "temp/video/scene_1_video.mp4",
        "temp/video/scene_2_video.mp4"
    ]

    test_audios = [
        "temp/audio/scene_1_voiceover.mp3",
        "temp/audio/scene_2_voiceover.mp3"
    ]

    test_narrations = [
        "Welcome to the future of artificial intelligence.",
        "Where machines and humans work together seamlessly."
    ]

    output_file = "static/videos/final_video.mp4"

    # Check if test files exist
    all_exist = all(os.path.exists(f) for f in test_videos + test_audios)

    if all_exist:
        print("Starting video assembly...")
        success = assemble_final_video(
            test_videos,
            test_audios,
            test_narrations,
            output_file,
            add_captions=True
        )

        if success:
            print(f"\nVideo assembled successfully: {output_file}")
        else:
            print("\nVideo assembly failed")
    else:
        print("Test files not found. Please generate videos and audio first.")
        print("This script is meant to be used after video and audio generation.")
