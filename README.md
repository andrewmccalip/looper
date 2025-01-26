# Audio/Video Looper

A Python script that creates seamlessly looped audio tracks and converts them into videos with a static image. Perfect for creating extended versions of songs or ambient sounds for YouTube, meditation apps, or background music.

## Features

- Creates seamlessly looped audio with crossfading
- Converts audio to video with a static image/thumbnail
- Optimized for long duration loops using recursive doubling
- Supports MP3 and MKV input formats
- Creates high-quality MP4 output with H.264 video codec

## Requirements

- Python 3.6+
- FFmpeg installed on your system
- Required Python packages:
  ```bash
  pip install pydub
  ```

## Installation

1. Install FFmpeg:
   - Windows: `winget install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org)
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` (Ubuntu/Debian)

2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/audio-video-looper.git
   cd audio-video-looper
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your input audio file (MP3 or MKV) in the project directory
2. Add your thumbnail image as `thumbnail.jpg`
3. Edit the constants in `main.py` if needed:
   ```python
   TARGET_DURATION = 1 * 60 * 60  # 1 hour in seconds
   INPUT_FILE = "song.mp3"        # Your input file
   THUMBNAIL = "thumbnail.jpg"     # Your thumbnail image
   ```
4. Run the script:
   ```bash
   python main.py
   ```

The script will:
1. Create a looped version of your audio file
2. Generate a video using the looped audio and your thumbnail
3. Output progress and status messages

## Output Files

- `looped_song.mp3`: The looped audio file
- `output_video.mp4`: The final video file with audio and thumbnail

## Configuration

You can modify these parameters in the script:
- `TARGET_DURATION`: Length of the final audio/video in seconds
- `INPUT_FILE`: Name of your input audio file
- `OUTPUT_FILE`: Name of the looped audio file
- `THUMBNAIL`: Name of your thumbnail image
- `VIDEO_OUTPUT`: Name of the final video file
- `crossfade_duration`: Length of crossfade between loops (default: 5 seconds)

## Troubleshooting

- **FFmpeg errors**: Make sure FFmpeg is installed and accessible from command line
- **File not found**: Ensure input files are in the correct directory
- **Audio processing errors**: Check input file format and permissions

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 