# ViralReel AI - Troubleshooting Guide

## Common Issues and Solutions

---

## 1. OpenAI/urllib3 Version Conflicts

### Error:
```
TypeError: __init__() got an unexpected keyword argument 'proxies'
```

or

```
NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+
```

### Solution:
The issue is caused by incompatible versions of OpenAI SDK, urllib3, and httpx.

**Fix:**
```bash
pip3 uninstall -y openai urllib3 httpx
pip3 install openai==1.3.0 urllib3==1.26.18 httpx==0.24.1
```

This installs compatible versions that work with Python 3.9 and LibreSSL.

---

## 2. Port 5000 Already in Use

### Error:
```
Address already in use
Port 5000 is in use by another program
```

### Solution:
Port 5000 is commonly used by macOS AirPlay Receiver.

**Fix Option 1:** Disable AirPlay Receiver
1. Open System Settings
2. Go to "General" > "AirDrop & Handoff"
3. Disable "AirPlay Receiver"

**Fix Option 2:** Use a Different Port (Already implemented)
The app now uses port 5001 by default. Access at:
```
http://localhost:5001
```

**Fix Option 3:** Set Custom Port
```bash
PORT=8080 python3 app.py
```

---

## 3. Missing Python Packages

### Error:
```
ModuleNotFoundError: No module named 'flask'
```

### Solution:
Install all required dependencies:

```bash
pip3 install -r requirements.txt
```

Or install individually:
```bash
pip3 install Flask==3.0.0
pip3 install python-dotenv==1.0.0
pip3 install openai==1.3.0
pip3 install requests==2.31.0
pip3 install moviepy==1.0.3
pip3 install Pillow==10.1.0
pip3 install urllib3==1.26.18
pip3 install httpx==0.24.1
```

---

## 4. API Key Errors

### Error:
```
openai.error.AuthenticationError: Incorrect API key provided
```

### Solution:
1. Check your `.env` file exists in the project root
2. Verify API keys are correctly formatted:

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
ELEVENLABS_API_KEY=xxxxxxxxxxxxxxx
RUNWAYML_API_KEY=xxxxxxxxxxxxxxx
```

3. Make sure there are no spaces around the `=` sign
4. No quotes needed around the keys
5. Restart the Flask server after updating `.env`

---

## 5. FFmpeg Not Found (MoviePy Errors)

### Error:
```
MoviePy Error: FFmpeg not found
```

### Solution:

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your PATH

**Verify Installation:**
```bash
ffmpeg -version
```

---

## 6. Font/TextClip Errors

### Error:
```
OSError: cannot open resource
```

### Solution:
MoviePy needs system fonts for captions.

**macOS:**
Fonts should be pre-installed. If issues persist:
```bash
brew install --cask font-arial
```

**Linux:**
```bash
sudo apt-get install fonts-liberation
sudo apt-get install fonts-dejavu
```

**Workaround in code:**
Edit `video_assembler.py`, change font to a simpler one:
```python
font='DejaVu-Sans'  # or 'Liberation-Sans'
```

---

## 7. Memory/Disk Space Issues

### Error:
```
MemoryError
```
or
```
OSError: [Errno 28] No space left on device
```

### Solution:

**Check disk space:**
```bash
df -h
```

**Clean up temporary files:**
```bash
rm -rf temp/audio/*
rm -rf temp/video/*
```

**Reduce video quality** in `video_assembler.py`:
```python
bitrate='4000k'  # Instead of 8000k
```

---

## 8. Slow Video Generation

### Issue:
Video generation takes 10+ minutes

### Explanation:
This is normal! RunwayML's AI video generation:
- Takes 1-3 minutes per scene
- 3 scenes = 3-9 minutes
- Plus overhead for script, voiceovers, assembly

### Tips to Speed Up:
1. **Use fewer scenes** (2-3 instead of 4-5)
2. **Shorter duration** per scene (3 seconds instead of 4)
3. **Simpler prompts** (fewer visual details)

---

## 9. RunwayML API Timeout

### Error:
```
Video generation timed out after 600 seconds
```

### Solution:
Increase timeout in `video_generator.py`:

```python
max_attempts = 240  # Increase from 120 (20 minutes total)
```

Or reduce video duration:
```python
duration_per_scene=3  # Instead of 4
```

---

## 10. ElevenLabs Rate Limiting

### Error:
```
429 Too Many Requests
```

### Solution:
ElevenLabs has rate limits based on your plan.

**Fix in code** (already implemented):
```python
time.sleep(0.5)  # Delay between requests
```

**Upgrade plan** or **wait** before generating more videos.

---

## 11. Import Errors for Custom Modules

### Error:
```
ModuleNotFoundError: No module named 'voiceover_generator'
```

### Solution:
Make sure you're running from the project root directory:

```bash
cd /Users/sanketmehta/viral-reel-ai
python3 app.py
```

Not from subdirectories.

---

## 12. Video Assembly Fails

### Error:
```
Error assembling video
```

### Debug Steps:

1. **Check if temp files exist:**
```bash
ls temp/audio/
ls temp/video/
```

2. **Verify file sizes:**
```bash
du -h temp/audio/*
du -h temp/video/*
```

3. **Test MoviePy directly:**
```python
from moviepy.editor import VideoFileClip
clip = VideoFileClip("temp/video/scene_1_video.mp4")
print(clip.duration)
```

4. **Check logs** in terminal for specific errors

---

## 13. Frontend Not Loading

### Issue:
Blank page or 404 errors

### Solution:

1. **Check Flask is running:**
```bash
curl http://localhost:5001/health
```

Should return:
```json
{"status":"ok","message":"ViralReel AI server is running"}
```

2. **Check static files exist:**
```bash
ls templates/index.html
ls static/css/style.css
ls static/js/script.js
```

3. **Clear browser cache** (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)

---

## 14. Video Not Playing in Browser

### Issue:
Video file generated but won't play

### Solution:

1. **Check codec compatibility:**
The app uses H.264/AAC which is widely supported.

2. **Download and test locally:**
Click download button and play in VLC or QuickTime

3. **Check file size:**
```bash
ls -lh static/videos/
```

If file is 0 bytes, assembly failed.

---

## 15. API Costs Too High

### Issue:
Video generation is expensive

### Solution:

**Cost Breakdown (per 3-scene video):**
- OpenAI: $0.01-0.02
- ElevenLabs: $0.05-0.10
- RunwayML: $0.60-1.80 ⬅️ Most expensive

**Reduce costs:**
1. Use fewer scenes (2 instead of 3)
2. Shorter duration (3 sec instead of 4)
3. Test with script generation only first
4. Cache generated assets for reuse

---

## Getting More Help

### Check Logs
The terminal shows detailed progress. Look for error messages.

### Verify API Status
- OpenAI: https://status.openai.com/
- ElevenLabs: Check dashboard for credits
- RunwayML: https://status.runwayml.com/

### Test Components Individually

**Test script generation:**
```bash
curl -X POST http://localhost:5001/generate-script \
  -H "Content-Type: application/json" \
  -d '{"topic":"Test topic"}'
```

**Test voiceover module:**
```bash
python3 voiceover_generator.py
```

**Test video generator:**
```bash
python3 video_generator.py
```

---

## Still Having Issues?

1. Check all dependencies are installed: `pip3 list`
2. Verify Python version: `python3 --version` (should be 3.8+)
3. Make sure all API keys are valid
4. Check internet connection
5. Review the [README.md](README.md) for setup steps
6. Look at code comments for implementation details

---

## Quick Diagnostic Checklist

```bash
# 1. Check Python version
python3 --version  # Should be 3.8+

# 2. Check packages
pip3 list | grep -E "Flask|openai|moviepy|requests"

# 3. Check FFmpeg
ffmpeg -version

# 4. Check API keys
cat .env

# 5. Test server
python3 app.py

# 6. In another terminal
curl http://localhost:5001/health

# 7. Check file structure
ls -la
ls templates/
ls static/css/
ls static/js/
```

If all checks pass, the app should work correctly!
