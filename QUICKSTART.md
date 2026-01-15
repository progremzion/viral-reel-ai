# ViralReel AI - Quick Start Guide

Get your first AI-generated video in 5 simple steps!

## Step 1: Install Dependencies

```bash
pip3 install -r requirements.txt
```

**Important:** If you get version conflicts with OpenAI/urllib3, run:
```bash
pip3 uninstall -y openai urllib3 httpx
pip3 install openai==1.3.0 urllib3==1.26.18 httpx==0.24.1
```

## Step 2: Add Your API Keys

Edit the `.env` file and add your API keys:

```
OPENAI_API_KEY=sk-your-key-here
ELEVENLABS_API_KEY=your-key-here
RUNWAYML_API_KEY=your-key-here
```

## Step 3: Start the Server

```bash
python3 app.py
```

## Step 4: Open the App

Open your browser and go to: **http://localhost:5001**

*Note: Port 5001 is used to avoid conflicts with macOS AirPlay*

## Step 5: Create Your First Video

1. Enter a topic (e.g., "The future of AI")
2. Click "Generate Video"
3. Wait 5-10 minutes for AI magic to happen
4. Download your video!

---

## Important Notes

- **First video will take time**: Video generation is compute-intensive (5-10 minutes is normal)
- **Check console output**: Watch the terminal for detailed progress
- **API costs apply**: Each video costs approximately:
  - OpenAI: ~$0.01-0.02
  - ElevenLabs: Based on character count
  - RunwayML: $0.05-0.15 per second of video

## Troubleshooting

**Server won't start?**
- Make sure Python 3.8+ is installed: `python --version`
- Check all dependencies installed: `pip list`

**API errors?**
- Verify API keys are correct in `.env`
- Check you have credits/billing enabled for each service

**Video assembly fails?**
- Install FFmpeg:
  - Mac: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`
  - Windows: Download from ffmpeg.org

## What Happens Behind the Scenes

```
Your Topic
    ↓
[OpenAI GPT-4o-mini]
    ↓
Generated Script (3-5 scenes)
    ↓
[ElevenLabs TTS]        [RunwayML Gen-3]
    ↓                        ↓
Audio Files            Video Clips
    ↓                        ↓
        [MoviePy Assembly]
              ↓
        Final Video! 🎉
```

## Example Topics That Work Well

- "5 amazing ocean facts"
- "The history of chocolate"
- "Future of space exploration"
- "Ancient Egypt mysteries"
- "How photosynthesis works"

Keep topics focused and specific for best results!

---

Need help? Check [README.md](README.md) for detailed documentation.
