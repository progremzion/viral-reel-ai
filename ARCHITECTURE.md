# ViralReel AI - System Architecture

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                     (Browser - Frontend)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  index.html + style.css + script.js                      │  │
│  │  - Input form for topic                                  │  │
│  │  - Progress bar & status updates                         │  │
│  │  - Video player & download button                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP/JSON
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK WEB SERVER                           │
│                        (app.py)                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Routes:                                                  │  │
│  │  GET  /              → Serve HTML                        │  │
│  │  GET  /health        → Health check                      │  │
│  │  POST /generate-script → Script only                     │  │
│  │  POST /create-video  → MAIN WORKFLOW ⭐                  │  │
│  │  GET  /static/videos → Serve videos                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────┬──────────────────┬──────────────────┬───────────────────┘
       │                  │                  │
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────────┐  ┌──────────────────┐
│   OpenAI    │  │   ElevenLabs    │  │    RunwayML      │
│  GPT-4o-mini│  │   Text-to-Speech│  │  Text-to-Video   │
│             │  │                 │  │    Gen-3 API     │
└──────┬──────┘  └────────┬────────┘  └────────┬─────────┘
       │                  │                     │
       │ Script JSON      │ Audio MP3           │ Video MP4
       │                  │                     │
       └──────────────────┴─────────────────────┘
                          │
                          ▼
              ┌──────────────────────┐
              │   Video Assembler    │
              │    (MoviePy)         │
              │  - Combine clips     │
              │  - Add audio         │
              │  - Generate captions │
              │  - Apply transitions │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Final Video Output  │
              │   static/videos/     │
              │   .mp4 file          │
              └──────────────────────┘
```

---

## Detailed Workflow

### Step-by-Step Process

```
1. USER INPUT
   │
   ├─► Topic: "The future of AI"
   │
   └─► Click "Generate Video"
        │
        ▼

2. SCRIPT GENERATION
   │
   ├─► app.py receives POST /create-video
   │
   ├─► Calls OpenAI GPT-4o-mini API
   │   └─► Prompt: "Create viral script about: The future of AI"
   │
   └─► Returns JSON:
       {
         "scenes": [
           {
             "scene_number": 1,
             "visuals": "Futuristic cityscape with AI...",
             "narration": "AI is transforming our world..."
           },
           // ... more scenes
         ]
       }
        │
        ▼

3. VOICEOVER GENERATION
   │
   ├─► voiceover_generator.py processes each scene
   │
   ├─► For each narration text:
   │   └─► Call ElevenLabs API
   │       └─► Returns audio MP3 file
   │
   └─► Saves to: temp/audio/{video_id}/scene_N_voiceover.mp3
        │
        ▼

4. VIDEO CLIP GENERATION
   │
   ├─► video_generator.py processes each scene
   │
   ├─► For each visual description:
   │   ├─► Call RunwayML Gen-3 API
   │   ├─► Create async task
   │   ├─► Poll for completion (1-3 min per scene)
   │   └─► Download video clip
   │
   └─► Saves to: temp/video/{video_id}/scene_N_video.mp4
        │
        ▼

5. VIDEO ASSEMBLY
   │
   ├─► video_assembler.py combines all assets
   │
   ├─► For each scene:
   │   ├─► Load video clip
   │   ├─► Load audio file
   │   ├─► Sync audio to video
   │   ├─► Add caption overlay
   │   └─► Add transitions (fade in/out)
   │
   ├─► Concatenate all scenes
   │
   ├─► Export final video
   │   └─► Codec: H.264
   │   └─► Format: MP4
   │   └─► Bitrate: 8000k
   │
   └─► Saves to: static/videos/viralreel_{timestamp}_{id}.mp4
        │
        ▼

6. RESPONSE TO USER
   │
   ├─► Return JSON:
   │   {
   │     "success": true,
   │     "video_url": "/static/videos/viralreel_...",
   │     "video_id": "abc123",
   │     "scenes_count": 3
   │   }
   │
   └─► Frontend displays video player
       └─► User can watch/download
```

---

## Component Architecture

### 1. Frontend Layer (Client-Side)

```javascript
// script.js - Main Flow
User Input
    ↓
Validation
    ↓
POST /create-video
    ↓
Progress Updates (polling)
    ↓
Display Video Player
```

**Key Functions**:
- `showLoading()` - Show progress UI
- `updateProgress(percent, message)` - Update progress bar
- `showVideo(url)` - Display final video
- `showError(message)` - Handle errors

---

### 2. Backend Layer (Server-Side)

#### Main Application (app.py)

```python
@app.route('/create-video')
def create_video():
    1. Parse request
    2. Generate script (OpenAI)
    3. Generate voiceovers (ElevenLabs)
    4. Generate videos (RunwayML)
    5. Assemble final video (MoviePy)
    6. Return video URL
```

#### Voiceover Generator (voiceover_generator.py)

```python
class VoiceoverGenerator:
    def generate_voiceover(text, output_path):
        - Prepare API request
        - Call ElevenLabs API
        - Save audio file
        - Return success/failure

    def generate_scene_voiceovers(scenes):
        - Iterate through scenes
        - Generate audio for each
        - Return list of file paths
```

#### Video Generator (video_generator.py)

```python
class VideoGenerator:
    def generate_video(prompt, output_path):
        - Create RunwayML task
        - Poll for completion
        - Download video
        - Return success/failure

    def generate_scene_videos(scenes):
        - Iterate through scenes
        - Generate video for each
        - Return list of file paths
```

#### Video Assembler (video_assembler.py)

```python
class VideoAssembler:
    def assemble_video(videos, audios, narrations):
        - Load video clips
        - Load audio clips
        - Sync audio with video
        - Add caption overlays
        - Apply transitions
        - Concatenate clips
        - Export final video
        - Return success/failure
```

---

## Data Flow

### Input Data
```json
{
  "topic": "The future of artificial intelligence"
}
```

### Intermediate: Script Data
```json
{
  "scenes": [
    {
      "scene_number": 1,
      "visuals": "A futuristic city with flying cars and holographic displays",
      "narration": "Imagine a world where AI powers everything around us"
    },
    {
      "scene_number": 2,
      "visuals": "Scientists working with advanced AI systems in a lab",
      "narration": "From healthcare to transportation, AI is revolutionizing every industry"
    },
    {
      "scene_number": 3,
      "visuals": "Diverse people collaborating with AI assistants",
      "narration": "The future isn't about replacing humans, it's about empowering them"
    }
  ]
}
```

### Intermediate: File Assets
```
temp/audio/abc123/
  ├── scene_1_voiceover.mp3
  ├── scene_2_voiceover.mp3
  └── scene_3_voiceover.mp3

temp/video/abc123/
  ├── scene_1_video.mp4
  ├── scene_2_video.mp4
  └── scene_3_video.mp4
```

### Output Data
```json
{
  "success": true,
  "video_url": "/static/videos/viralreel_20240115_143022_abc123.mp4",
  "video_id": "abc123",
  "scenes_count": 3,
  "message": "Video created successfully!"
}
```

### Final File
```
static/videos/viralreel_20240115_143022_abc123.mp4
- Duration: ~12 seconds (3 scenes × 4 sec)
- Format: MP4 (H.264)
- Resolution: 1080×1920 (9:16)
- Audio: AAC 192k
- Captions: Embedded
```

---

## External API Integration

### OpenAI API
```
Endpoint: https://api.openai.com/v1/chat/completions
Method: POST
Headers:
  - Authorization: Bearer {API_KEY}
  - Content-Type: application/json

Request:
{
  "model": "gpt-4o-mini",
  "messages": [...],
  "temperature": 0.8,
  "max_tokens": 1000,
  "response_format": {"type": "json_object"}
}

Response Time: ~5-10 seconds
```

### ElevenLabs API
```
Endpoint: https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
Method: POST
Headers:
  - xi-api-key: {API_KEY}
  - Content-Type: application/json

Request:
{
  "text": "Your narration text here",
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
  }
}

Response: Binary audio data (MP3)
Response Time: ~2-5 seconds per scene
```

### RunwayML API
```
Step 1: Create Task
Endpoint: https://api.runwayml.com/v1/text-to-video
Method: POST
Headers:
  - Authorization: Bearer {API_KEY}
  - Content-Type: application/json

Request:
{
  "prompt": "Visual description",
  "duration": 4,
  "aspect_ratio": "9:16",
  "model": "gen3a_turbo"
}

Response:
{
  "id": "task_123456",
  "status": "PENDING"
}

Step 2: Poll Status
Endpoint: https://api.runwayml.com/v1/tasks/{task_id}
Method: GET

Response:
{
  "id": "task_123456",
  "status": "SUCCEEDED",
  "output": ["https://video-url.mp4"]
}

Response Time: ~1-3 minutes per scene
```

---

## Error Handling Strategy

```
┌─────────────────────┐
│  User Request       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Input Validation   │──► Error: "Topic required"
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Script Generation  │──► Error: "OpenAI API failed"
└──────────┬──────────┘    Retry: Yes (1x)
           │
           ▼
┌─────────────────────┐
│ Voiceover Creation  │──► Error: "ElevenLabs API failed"
└──────────┬──────────┘    Retry: Yes (per scene)
           │               Fallback: Skip scene
           ▼
┌─────────────────────┐
│  Video Generation   │──► Error: "RunwayML timeout"
└──────────┬──────────┘    Retry: No (too expensive)
           │               Fallback: Return partial
           ▼
┌─────────────────────┐
│  Video Assembly     │──► Error: "FFmpeg missing"
└──────────┬──────────┘    Retry: No
           │               Error: Installation needed
           ▼
┌─────────────────────┐
│  Success Response   │
└─────────────────────┘
```

---

## Performance Optimization Opportunities

### Current Bottlenecks
1. **Video Generation (RunwayML)**: 1-3 min per scene (sequential)
2. **Video Assembly (MoviePy)**: 30-60 seconds
3. **API Rate Limits**: Can slow down multi-scene videos

### Optimization Strategies

```
CURRENT (Sequential):
Script → Voice 1 → Voice 2 → Voice 3 → Video 1 → Video 2 → Video 3 → Assemble
Total: ~6-10 minutes

OPTIMIZED (Parallel):
Script ──┬──► Voice 1 ──┬──► Video 1 ──┐
         ├──► Voice 2 ──┼──► Video 2 ──┼──► Assemble
         └──► Voice 3 ──┴──► Video 3 ──┘
Total: ~3-5 minutes (with async/threading)
```

### Caching Strategy
```
Cache Key: hash(topic + model_settings)
├─► Script Cache (Redis): 24 hours
├─► Voice Cache (S3): 7 days
└─► Video Cache (S3): 30 days

On Cache Hit:
- Skip API calls
- Retrieve from storage
- Instant assembly
Total Time: ~30 seconds
```

---

## Scalability Considerations

### Single Server Limits
- Max concurrent videos: ~3-5
- Disk space: 500MB per video
- Memory: 2GB per video assembly

### Horizontal Scaling Architecture
```
                    Load Balancer
                          ↓
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
    Server 1          Server 2          Server 3
        ↓                 ↓                 ↓
        └─────────────────┼─────────────────┘
                          ↓
                    Message Queue
                    (Redis/RabbitMQ)
                          ↓
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
    Worker 1          Worker 2          Worker 3
    (Video Gen)       (Voice Gen)       (Assembly)
        ↓                 ↓                 ↓
        └─────────────────┼─────────────────┘
                          ↓
                  Shared Storage (S3)
```

---

This architecture supports the complete video generation pipeline from user input to final output, with clear separation of concerns and integration points for all AI services.
