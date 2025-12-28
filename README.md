# Motorola Voice File Converter (MVA Converter)

A simple GUI application to convert audio files into formats compatible with Motorola two-way radio Customer Programming Software (CPS) for voice announcements.

## Overview

This tool converts standard audio files (WAV, MP3, FLAC, etc.) into the specific formats required by Motorola radio programming software:

- **APX CPS-ready WAV**: 8 kHz, 16-bit PCM, mono WAV files for use with APX CPS VA Converter Utility
- **MOTOTRBO MVA**: 8 kHz, 8-bit μ-law encoded MVA files for legacy MOTOTRBO CPS

The converter uses FFmpeg under the hood and includes loudness normalization to ensure voice prompts are at appropriate levels.

## Features

- **User-friendly GUI**: Simple interface built with tkinter
- **Multiple input formats**: Supports any audio format that FFmpeg can read (WAV, MP3, M4A, FLAC, AIFF, OGG, AAC, WMA, etc.)
- **Two conversion profiles**:
  - APX CPS-ready WAV (8 kHz, 16-bit PCM, mono)
  - MOTOTRBO MVA (8 kHz, 8-bit μ-law, legacy CPS safe)
- **Automatic loudness normalization**: Applies audio normalization for consistent voice prompt levels
- **Custom output naming**: Choose your own output filename and location

## Requirements

- **Python 3.10+** (uses modern type hints like `str | None`)
- **FFmpeg**: Must be installed and available in your system PATH
- **tkinter**: Usually included with Python installations

## Installation

1. **Install Python 3.10 or later**
   - Download from [python.org](https://www.python.org/downloads/)
   - Ensure Python is added to your system PATH during installation

2. **Install FFmpeg**
   
   **Windows:**
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extract and add the `bin` folder to your system PATH
   - Or use a package manager like [Chocolatey](https://chocolatey.org/): `choco install ffmpeg`

   **macOS:**
   ```bash
   brew install ffmpeg
   ```

   **Linux (Debian/Ubuntu):**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

3. **Download the converter**
   ```bash
   git clone https://github.com/RoseOO/MotorolaMVAConverter.git
   cd MotorolaMVAConverter
   ```

## Usage

1. **Run the application**:
   ```bash
   python mva_maker.py
   ```
   
   Or on some systems:
   ```bash
   python3 mva_maker.py
   ```

2. **Convert your audio**:
   - Click **Browse** next to "Input WAV" to select your audio file
   - Choose an output folder (defaults to current directory)
   - Enter a filename (without extension)
   - Select the appropriate profile:
     - Use **APX CPS-ready WAV** for APX radios
     - Use **MOTOTRBO MVA** for MOTOTRBO radios with legacy CPS
   - Click **Convert**

3. **Import to CPS**:
   - **For APX**: Import the generated WAV file into CPS using Tools → VA Converter Utility
   - **For MOTOTRBO**: Use the generated .mva file directly in your CPS

## Profiles Explained

### APX CPS-ready WAV (8 kHz, 16-bit PCM, mono)
This profile creates a standard WAV file with specifications compatible with the APX CPS VA Converter Utility. After conversion, you'll import this WAV file into CPS where it will be further processed by Motorola's own converter.

**Technical specs:**
- Sample rate: 8 kHz
- Bit depth: 16-bit
- Channels: Mono
- Codec: PCM (signed 16-bit little-endian)

### MOTOTRBO MVA (legacy CPS safe)
This profile creates an MVA file (which is actually a WAV file with a .mva extension) using μ-law encoding. This format is compatible with legacy MOTOTRBO CPS versions and can be used directly.

**Technical specs:**
- Sample rate: 8 kHz
- Channels: Mono
- Codec: μ-law (PCM mu-law)
- Metadata: Stripped for maximum compatibility
- Bitexact flags: Enabled for deterministic output

## Audio Normalization

The converter automatically applies loudness normalization using FFmpeg's `loudnorm` filter with the following parameters:
- Integrated loudness target: -16 LUFS
- True peak: -4 dBTP
- Loudness range: 11 LU

This ensures consistent volume levels across different voice announcements. If you prefer to preserve the original audio levels, you can modify the `audio_filter` line in the code.

## Troubleshooting

**"FFmpeg not found in PATH" error:**
- Ensure FFmpeg is installed
- Verify it's in your system PATH by running `ffmpeg -version` in a terminal
- Restart the application after installing FFmpeg

**Conversion fails:**
- Check that your input file is a valid audio file
- Ensure the output directory exists and is writable
- Check the error message for specific FFmpeg errors

**Output file won't import to CPS:**
- Ensure you selected the correct profile for your radio type
- For APX: Use the "APX CPS-ready WAV" profile
- For MOTOTRBO: Use the "MOTOTRBO MVA" profile

## License

This project is provided as-is for use with Motorola radio programming. Please ensure compliance with Motorola's software licensing terms when using CPS and related tools.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Acknowledgments

- Built with Python and tkinter for cross-platform compatibility
- Uses FFmpeg for reliable audio conversion
- Designed for Motorola APX and MOTOTRBO radio systems
