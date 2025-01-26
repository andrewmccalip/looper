from pydub import AudioSegment
import subprocess
import os

# Configuration constants
TARGET_DURATION = 1 * 60 * 60  # Default target duration of 1 hour in seconds
INPUT_FILE = "song.mp3"        # Source audio file (supports MP3 and MKV)
OUTPUT_FILE = "looped_" + INPUT_FILE  # Name of the looped audio output
THUMBNAIL = "thumbnail.jpg"    # Static image for video background
VIDEO_OUTPUT = "output_video.mp4"  # Final video output filename

def loop_song(input_file=INPUT_FILE, output_file=OUTPUT_FILE, target_duration=TARGET_DURATION, crossfade_duration=5):
    """
    Creates a seamlessly looped version of the input audio file by:
    1. Creating chunks of 10x song length
    2. Calculating optimal combination to reach target duration
    3. Combining chunks with crossfade
    """
    print(f"\nStarting audio loop process...")
    print(f"Input file: {input_file}")
    print(f"Target duration: {target_duration/60:.1f} minutes")
    
    try:
        # Load and validate the audio file
        print("Loading audio file...")
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
            
        # Handle different input formats
        if input_file.endswith('.mkv'):
            audio = AudioSegment.from_file(input_file, format="mkv")
        else:
            audio = AudioSegment.from_mp3(input_file)
        
        # Calculate durations
        original_duration = len(audio)
        print(f"Original audio duration: {original_duration/1000/60:.2f} minutes")
        crossfade_ms = crossfade_duration * 1000
        target_ms = target_duration * 1000
        chunk_size = original_duration * 10  # 10 songs per chunk

        # Create chunks of 10x song length
        chunks = []
        current_audio = audio
        chunk_number = 1
        
        while len(current_audio) < target_ms:
            # Create chunk of 10 songs
            chunk_file = f"temp_chunk_{chunk_number}.mp3"
            print(f"Creating chunk {chunk_number} ({(chunk_size/1000/60):.1f} minutes)...")
            
            for _ in range(9):  # Add 9 more copies to make 10
                current_audio = current_audio.append(audio, crossfade=crossfade_ms)
            
            current_audio.export(chunk_file, format="mp3", bitrate="192k")
            chunks.append(chunk_file)
            chunk_number += 1
            
            # Start fresh for next chunk to prevent memory buildup
            current_audio = audio

        # Calculate best combination of chunks to reach target duration
        print("\nCalculating optimal chunk combination...")
        best_duration = 0
        best_chunks = []
        chunk_duration = chunk_size - crossfade_ms  # Account for crossfade

        # Try different combinations of chunks
        for i in range(1, len(chunks) + 1):
            duration = chunk_duration * i
            if duration <= target_ms and duration > best_duration:
                best_duration = duration
                best_chunks = chunks[:i]

        # Combine the chunks
        print(f"\nCombining {len(best_chunks)} chunks...")
        final_audio = AudioSegment.from_mp3(best_chunks[0])
        for chunk_file in best_chunks[1:]:
            chunk = AudioSegment.from_mp3(chunk_file)
            final_audio = final_audio.append(chunk, crossfade=crossfade_ms)
            chunk = None  # Clear memory

        # Clean up temp files
        print("Cleaning up temporary files...")
        for chunk_file in chunks:
            try:
                os.remove(chunk_file)
            except:
                pass

        # Export the final audio file
        print(f"Exporting final audio to {output_file}...")
        final_audio.export(output_file, format="mp3", bitrate="192k")
        final_audio = None  # Clear from memory
        
        print("✓ Audio loop creation complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during audio processing: {str(e)}")
        # Clean up temp files on error
        for chunk_file in chunks:
            try:
                os.remove(chunk_file)
            except:
                pass
        return False

def create_video_with_thumbnail(audio_file=OUTPUT_FILE, 
                              thumbnail=THUMBNAIL,
                              output_video=VIDEO_OUTPUT):
    """
    Creates a video file using the looped audio and a static image.
    Uses FFmpeg for efficient video creation with minimal CPU usage.
    
    Args:
        audio_file: Path to the looped audio file
        thumbnail: Path to the static image file
        output_video: Path for the output video file
    """
    print(f"\nStarting video creation...")
    print(f"Using audio: {audio_file}")
    print(f"Using thumbnail: {thumbnail}")
    print(f"Output video will be: {output_video}")
    
    try:
        # Validate input files exist
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        if not os.path.exists(thumbnail):
            raise FileNotFoundError(f"Thumbnail file not found: {thumbnail}")
        
        # Construct FFmpeg command with optimized settings
        ffmpeg_cmd = [
            'ffmpeg', '-y',                # Overwrite output file if it exists
            '-loop', '1',                  # Loop the input image
            '-framerate', '2',             # Low framerate for static image
            '-i', thumbnail,               # Input image
            '-i', audio_file,              # Input audio
            '-c:v', 'libx264',            # Use H.264 codec
            '-tune', 'stillimage',         # Optimize for static image
            '-c:a', 'aac',                # Use AAC audio codec
            '-b:a', '192k',               # Audio bitrate
            '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',  # Scale and center image
            '-pix_fmt', 'yuv420p',        # Standard pixel format
            '-shortest',                   # Match video length to audio
            '-r', '2',                     # Output framerate
            output_video
        ]
        
        # Run FFmpeg and capture any errors
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
    
    loop_song()
    create_video_with_thumbnail()
    
    print("\n✓ Process Complete! Output video created successfully.")
