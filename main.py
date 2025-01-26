from pydub import AudioSegment
import subprocess
import os

# Default target duration of 1 hour in seconds
TARGET_DURATION = 1 * 60 * 60
INPUT_FILE = "song.mp3"  # Will also work with song.mkv
OUTPUT_FILE = "looped_" + INPUT_FILE
THUMBNAIL = "thumbnail.jpg"
VIDEO_OUTPUT = "output_video.mp4"

def loop_song(input_file=INPUT_FILE, output_file=OUTPUT_FILE, target_duration=TARGET_DURATION, crossfade_duration=5):
    print(f"\nStarting audio loop process...")
    print(f"Input file: {input_file}")
    print(f"Target duration: {target_duration} seconds")
    
    try:
        # Load the audio file
        print("Loading audio file...")
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
            
        if input_file.endswith('.mkv'):
            audio = AudioSegment.from_file(input_file, format="mkv")
        else:
            audio = AudioSegment.from_mp3(input_file)
        
        # Get original duration in milliseconds
        original_duration = len(audio)
        print(f"Original audio duration: {original_duration/1000:.2f} seconds")
        crossfade_ms = crossfade_duration * 1000
        target_ms = target_duration * 1000

        # Calculate number of loops needed
        num_loops = max(1, int(target_ms / original_duration))
        print(f"Need to create equivalent of {num_loops} loops...")

        # Use recursive doubling for faster processing
        final_audio = audio
        current_loops = 1
        
        while len(final_audio) < target_ms:
            print(f"Current audio length: {len(final_audio)/1000:.2f}s / {target_ms/1000:.2f}s")
            
            if current_loops >= 10:  # If we need many loops, start doubling
                print("Doubling audio length...")
                final_audio = final_audio.append(final_audio, crossfade=crossfade_ms)
                current_loops *= 2
            else:
                print(f"Adding loop {current_loops}...")
                final_audio = final_audio.append(audio, crossfade=crossfade_ms)
                current_loops += 1

        # Trim to exact length if we went over
        if len(final_audio) > target_ms:
            print(f"Trimming to exact length...")
            final_audio = final_audio[:target_ms]

        # Export the final audio
        print(f"Exporting final audio to {output_file}...")
        final_audio.export(output_file, format="mp3")
        print("✓ Audio loop creation complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during audio processing: {str(e)}")
        return False

def create_video_with_thumbnail(audio_file=OUTPUT_FILE, 
                              thumbnail=THUMBNAIL,
                              output_video=VIDEO_OUTPUT):
    """
    Creates a video file using a looped audio track and a static image using ffmpeg
    """
    print(f"\nStarting video creation...")
    print(f"Using audio: {audio_file}")
    print(f"Using thumbnail: {thumbnail}")
    print(f"Output video will be: {output_video}")
    
    try:
        # Check if input files exist
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        if not os.path.exists(thumbnail):
            raise FileNotFoundError(f"Thumbnail file not found: {thumbnail}")
        
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-framerate', '0.5',  # Very low framerate since image is static
            '-i', thumbnail,
            '-i', audio_file,
            '-c:v', 'libx264',
            '-tune', 'stillimage',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
            '-pix_fmt', 'yuv420p',
            '-shortest',
            '-r', '2',  # Output framerate
            output_video
        ]
        
        print("Running ffmpeg command...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")
            
        print("✓ Video creation complete!")
        return True
        
    except FileNotFoundError as e:
        print(f"\n❌ File error: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ Error during video creation: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Starting Audio Loop and Video Creation Process ===")
    
    # Create looped audio
    if not loop_song():
        print("❌ Failed to create looped audio. Exiting.")
        exit(1)
    
    # Create video with the looped audio and thumbnail
    if not create_video_with_thumbnail():
        print("❌ Failed to create video. Exiting.")
        exit(1)
    
    print("\n✓ Process Complete! Output video created successfully.")
