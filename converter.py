"""
A utility script to create extended loops of audio files (MP3 or MKV).
Uses pydub to seamlessly loop audio tracks with crossfading between iterations,
useful for creating extended versions of songs or background music.

Example:
    >>> loop_song("input.mp3", target_duration=3600)  # Creates 1-hour loop
"""

import os
from pathlib import Path
from typing import Union
from pydub import AudioSegment

def loop_song(
    input_file: Union[str, Path] = "song.mp3",
    output_file: Union[str, Path] = None,
    target_duration: int = 3600,  # 1 hour in seconds
    crossfade_duration: int = 5,  # 5 seconds crossfade
) -> None:
    """
    Create an extended loop of an audio file with smooth crossfading.

    Args:
        input_file: Path to the input audio file (MP3 or MKV)
        output_file: Path for the output MP3 file. If None, prepends "looped_" to input filename
        target_duration: Desired duration in seconds (default: 1 hour)
        crossfade_duration: Duration of crossfade between loops in seconds (default: 5)

    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the input file is empty or invalid
        RuntimeError: If the processing fails
    """
    # Convert to Path objects
    input_path = Path(input_file)
    if output_file is None:
        output_file = input_path.parent / f"looped_{input_path.name}"
    output_path = Path(output_file)

    # Validate input
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if input_path.stat().st_size == 0:
        raise ValueError(f"Input file is empty: {input_path}")

    try:
        print(f"Loading audio file: {input_path}")
        # Load the audio file (auto-detect format)
        audio = AudioSegment.from_file(input_path)
        
        # Get durations in milliseconds
        original_duration = len(audio)
        target_ms = target_duration * 1000
        crossfade_ms = crossfade_duration * 1000

        print(f"Original duration: {original_duration/1000:.2f} seconds")
        print(f"Target duration: {target_duration} seconds")

        # Calculate number of loops needed
        # Add one extra loop to account for crossfade overlap
        effective_duration = original_duration - crossfade_ms
        num_loops = max(1, int(target_ms / effective_duration) + 1)
        
        print(f"Creating {num_loops} loops with {crossfade_duration}s crossfade...")

        # Create the looped audio
        final_audio = audio
        for i in range(num_loops - 1):
            # Crossfade between iterations
            final_audio = final_audio.append(audio, crossfade=crossfade_ms)
            print(f"Loop {i+1}/{num_loops-1} complete")

        # Trim to exact target duration if needed
        if len(final_audio) > target_ms:
            final_audio = final_audio[:target_ms]

        # Create output directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Exporting to: {output_path}")
        # Export with high quality settings
        final_audio.export(
            output_path,
            format="mp3",
            bitrate="320k",
            parameters=["-q:a", "0"]
        )
        print(f"Successfully created {target_duration/3600:.1f} hour loop!")

    except Exception as e:
        raise RuntimeError(f"Failed to create loop: {str(e)}") from e

def main() -> None:
    """Entry point when running the script directly."""
    import argparse

    parser = argparse.ArgumentParser(description="Create extended audio loops with crossfading.")
    parser.add_argument("input", help="Input audio file path (MP3 or MKV)")
    parser.add_argument("-o", "--output", help="Output MP3 file path")
    parser.add_argument(
        "-d", "--duration",
        type=int,
        default=3600,
        help="Target duration in seconds (default: 3600 = 1 hour)"
    )
    parser.add_argument(
        "-c", "--crossfade",
        type=int,
        default=5,
        help="Crossfade duration in seconds (default: 5)"
    )
    
    args = parser.parse_args()
    loop_song(
        args.input,
        args.output,
        args.duration,
        args.crossfade
    )

if __name__ == "__main__":
    main()
