# Google Avatar Frame Generator

English | [简体中文](README_ZH.md)

Bring the iconic Google profile ring to any avatar with ease.


## Features

This tool allows you to generate framed avatars directly in your browser or run it locally using a Python script:

### 🌐 Web App
- **Real-time Adjustments**: Use interactive sliders to fine-tune ring thickness, white spacer gap, avatar zoom, and horizontal/vertical offsets.
- **Color Palettes**: Choose from 4 distinct color schemes (Google Classic, Monochrome, Neon, and Pastel).
- **Privacy & Performance**: All canvas operations are processed locally in your browser. Nothing is sent to a server.

### 🐍 Python CLI Tool
- **Full Parameter Support**: Run the script with custom options matching the web application (thickness, gap, zoom, offset, and color palettes).
- **Headless Safety Fallback**: Includes a Tkinter file picker that automatically falls back to interactive text prompts when run in non-GUI terminal or server environments.

## File Structure

- `index.html`: Structuring the web layout.
- `style.css`: Premium responsive design styles based on Glassmorphism.
- `script.js`: Core Canvas drawing, translations, and slider event logic.
- `google_avatar_frame.py`: Local Python command-line image generator.
- `requirements.txt`: Python dependencies list.

## Getting Started

### Running the Web App
Clone or download this repository and launch a static server in the root folder:
```bash
# Start a simple server using Python
python -m http.server 8000
```
Open `http://localhost:8000` in your web browser. You can deploy this folder directly to GitHub Pages or any static site hosting provider.<br>
**Note:** When deploying to Vercel, please select "Other" as the project type instead of "Python" to avoid deployment errors.

### Running the Python Tool
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute the script:
   - Interactive UI mode:
     ```bash
     python google_avatar_frame.py
     ```
   - Command-line generation with parameters:
     ```bash
     python google_avatar_frame.py input.png -o output.png --zoom 1.2 --offset-x 0.05 --palette neon
     ```
     Run `python google_avatar_frame.py --help` for the full parameter list.

## Credits & Attributions

- **Original Author**: Special thanks to the original creator [2010384626](https://github.com/2010384626) for the core frame layout and baseline algorithm.
- **AI Attribution**: The visual redesign (Glassmorphism layout, color themes, responsive sliders, translations) and Python CLI upgrades (custom arguments, GUI crash protection) were generated and optimized with Google Gemini.
