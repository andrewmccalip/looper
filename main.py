from pydub import AudioSegment
import subprocess
import os

# Default target duration of 1 hour in seconds
DEFAULT_TARGET_DURATION = 1 * 60 * 60
DEFAULT_INPUT_FILE = "song.mp3"  # Will also work with song.mkv
DEFAULT_OUTPUT_FILE = "looped_" + DEFAULT_INPUT_FILE
DEFAULT_THUMBNAIL = "thumbnail.jpg"
DEFAULT_VIDEO_OUTPUT = "output_video.mp4"

def loop_song(input_file=DEFAULT_INPUT_FILE, output_file=DEFAULT_OUTPUT_FILE, target_duration=DEFAULT_TARGET_DURATION, crossfade_duration=5):
    print(f"\nStarting audio loop process...")
    print(f"Input file: {input_file}")
    print(f"Target duration: {target_duration} seconds")
    
    # Load the audio file
    print("Loading audio file...")
    if input_file.endswith('.mkv'):
        audio = AudioSegment.from_file(input_file, format="mkv")
    else:
        audio = AudioSegment.from_mp3(input_file)
    
    # Get original duration in milliseconds
    original_duration = len(audio)
    print(f"Original audio duration: {original_duration/1000:.2f} seconds")
    crossfade_ms = crossfade_duration * 1000
    
    # Calculate number of loops needed for target duration
    target_ms = target_duration * 1000
    num_loops = max(1, int(target_ms / original_duration))
    print(f"Creating {num_loops} loops with {crossfade_duration}s crossfade...")

    # Create the looped audio
    final_audio = audio
    for i in range(num_loops - 1):
        print(f"Processing loop {i+1}/{num_loops-1}...")
        # Crossfade between iterations
        final_audio = final_audio.append(audio, crossfade=crossfade_ms)

    # Export the final audio
    print(f"Exporting final audio to {output_file}...")
    final_audio.export(output_file, format="mp3")
    print("Audio loop creation complete!")

def create_video_with_thumbnail(audio_file=DEFAULT_OUTPUT_FILE, 
                              thumbnail=DEFAULT_THUMBNAIL,
                              output_video=DEFAULT_VIDEO_OUTPUT):
    """
    Creates a video file using a looped audio track and a static image using ffmpeg
    """
    print(f"\nStarting video creation...")
    print(f"Using audio: {audio_file}")
    print(f"Using thumbnail: {thumbnail}")
    print(f"Output video will be: {output_video}")
    
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-loop', '1',
        '-framerate', '2',  # Very low framerate since image is static
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
    subprocess.run(ffmpeg_cmd)
    print("Video creation complete!")

if __name__ == "__main__":
    print("=== Starting Audio Loop and Video Creation Process ===")
    
    # Create looped audio
    loop_song()
    
    # Create video with the looped audio and thumbnail
    create_video_with_thumbnail()
    
    print("\n=== Process Complete! ===")
