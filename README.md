# 🎬 ViralReel AI - Automated Short-Form Video Creator

> Transform any topic into viral-ready videos in minutes, not hours.

An AI-powered web application that automatically generates short-form videos for TikTok, Instagram Reels, and YouTube Shorts. Simply provide a topic, and ViralReel AI handles everything: script writing, voiceovers, visuals, and video assembly.

## ✨ Features

- 🤖 **AI Script Generation**: OpenAI GPT-4o-mini creates engaging viral video scripts
- 🎤 **Voiceovers**: Google Text-to-Speech generates voiceovers (ElevenLabs support included)
- 🎥 **AI Video Generation**: RunwayML's Veo 3.1 creates stunning visuals from text
- 📝 **Automatic Captions**: Synchronized captions for better engagement
- 📱 **Vertical Format**: Optimized 9:16 aspect ratio for social media
- ⚡ **One-Click Creation**: Fully automated end-to-end workflow

## 🎯 Perfect For

- Content creators looking to scale video production
- Social media marketers automating content creation
- Educators creating engaging educational videos
- Businesses generating marketing content
- Anyone wanting to create viral videos without video editing skills

## 🚀 Demo

https://github.com/user-attachments/assets/your-demo-video-here

*(Add a demo video or GIF of your interface once you record one)*

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI Services**:
  - OpenAI GPT-4o-mini (script generation)
  - ElevenLabs (text-to-speech)
  - RunwayML Gen-3 (text-to-video)
- **Video Processing**: MoviePy

## Prerequisites

- Python 3.8 or higher
- API keys for:
  - OpenAI (GPT-4o-mini)
  - ElevenLabs
  - RunwayML

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd viral-reel-ai
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv

   # On macOS/Linux:
   source venv/bin/activate

   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Edit the `.env` file and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   RUNWAYML_API_KEY=your_runwayml_api_key_here
   ```

## Getting API Keys

### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API keys section
4. Create a new API key

### ElevenLabs API Key
1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Sign up or log in
3. Go to your profile settings
4. Copy your API key

### RunwayML API Key
1. Go to [RunwayML](https://runwayml.com/)
2. Sign up or log in
3. Navigate to API settings
4. Generate an API key

## Usage

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5001
   ```

   Note: The app uses port 5001 by default to avoid conflicts with macOS AirPlay Receiver on port 5000.

3. **Create a video**:
   - Enter a topic or paste article text in the text area
   - Click "Generate Video"
   - Wait for the AI to create your video (this may take 3-10 minutes)
   - Download and share your video!

## Project Structure

```
viral-reel-ai/
├── app.py                      # Main Flask application
├── voiceover_generator.py      # ElevenLabs integration
├── video_generator.py          # RunwayML integration
├── video_assembler.py          # Video assembly with MoviePy
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
├── templates/
│   └── index.html             # Frontend HTML
├── static/
│   ├── css/
│   │   └── style.css          # Styles
│   ├── js/
│   │   └── script.js          # Frontend JavaScript
│   └── videos/                # Generated videos
└── temp/
    ├── audio/                 # Temporary audio files
    └── video/                 # Temporary video clips
```

## How It Works

1. **Script Generation**: User provides a topic → OpenAI GPT-4o-mini generates a structured script with scenes
2. **Voiceover Creation**: Script narration → ElevenLabs converts to speech audio files
3. **Video Generation**: Visual descriptions → RunwayML creates video clips
4. **Video Assembly**: MoviePy combines clips, audio, and captions into final video

## Example Topics

- "The future of artificial intelligence"
- "5 mind-blowing space facts"
- "How to boost productivity in 2024"
- "The science behind dreams"
- "Ancient civilizations mysteries"

## Troubleshooting

**For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

### Video generation is slow
- This is normal! RunwayML's AI video generation can take 2-5 minutes per scene
- A typical 3-scene video takes 5-10 minutes total

### API errors
- Verify all API keys are correctly set in `.env`
- Check that you have sufficient API credits
- Ensure your API keys have the necessary permissions

### MoviePy/FFmpeg errors
- MoviePy requires FFmpeg. Install it:
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt-get install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/)

### Font errors (TextClip)
- Ensure Arial or another system font is available
- On Linux, install: `sudo apt-get install fonts-liberation`

## Cost Considerations

Each video generation uses:
- OpenAI GPT-4o-mini: ~$0.01-0.02 per video
- ElevenLabs: ~10,000 characters per video
- RunwayML: Most expensive - varies by scene count and duration

Test with short scripts (2-3 scenes) first to manage costs.

## Future Enhancements

- Background music integration
- Multiple voice options
- Custom branding/watermarks
- Batch video generation
- Video editing/trimming tools
- Direct social media posting

## 🤝 Contributing

Contributions are welcome! This is an open-source project under active development.

**Areas for improvement:**
- Better voiceover quality (OpenAI TTS, ElevenLabs enhancement)
- Hybrid video generation (mix AI + stock footage)
- Advanced caption styling (word-by-word highlighting)
- Background music integration
- Template system for different video styles
- User authentication and payment system

See `ARCHITECTURE.md` for system design details.

## ⭐ Star History

If you find this project useful, please consider giving it a star! It helps others discover the project.

## 📝 License

MIT License - feel free to use this for personal or commercial projects.

## 🙏 Credits

Built with:
- [OpenAI](https://openai.com/) - GPT-4o-mini for script generation
- [RunwayML](https://runwayml.com/) - Veo 3.1 for AI video generation
- [Google TTS](https://cloud.google.com/text-to-speech) - Free voiceovers
- [MoviePy](https://zulko.github.io/moviepy/) - Video assembly
- [Flask](https://flask.palletsprojects.com/) - Web framework

## 📧 Contact

Questions or suggestions? Open an issue or reach out!

---

**⚠️ Note**: This is a working MVP/prototype. For production use, additional features needed:
- User authentication & multi-tenancy
- Payment/subscription system
- Queue system for video generation (Celery/Redis)
- Cloud storage (AWS S3/CloudFlare R2)
- Monitoring & error tracking
- Rate limiting & abuse prevention

**💡 Interested in the commercial version?** This project demonstrates core capabilities. A production-ready SaaS version with premium features is in development.
