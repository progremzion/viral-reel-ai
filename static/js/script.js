/**
 * ViralReel AI - Frontend JavaScript
 * Handles form submission, API communication, and UI updates
 */

// DOM Elements
const videoForm = document.getElementById('videoForm');
const generateBtn = document.getElementById('generateBtn');
const btnText = generateBtn.querySelector('.btn-text');
const loader = generateBtn.querySelector('.loader');

const statusSection = document.getElementById('statusSection');
const statusMessage = document.getElementById('statusMessage');
const progressBar = document.getElementById('progressBar');

const outputSection = document.getElementById('outputSection');
const generatedVideo = document.getElementById('generatedVideo');
const downloadBtn = document.getElementById('downloadBtn');
const createNewBtn = document.getElementById('createNewBtn');

const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const retryBtn = document.getElementById('retryBtn');

// State
let currentVideoUrl = null;

/**
 * Update the UI to show loading state
 */
function showLoading() {
    generateBtn.disabled = true;
    btnText.textContent = 'Generating...';
    loader.style.display = 'inline-block';

    // Hide other sections
    outputSection.style.display = 'none';
    errorSection.style.display = 'none';

    // Show status section
    statusSection.style.display = 'block';
    progressBar.style.width = '0%';
}

/**
 * Update the progress bar and status message
 */
function updateProgress(percent, message) {
    progressBar.style.width = percent + '%';
    statusMessage.textContent = message;
}

/**
 * Show the generated video
 */
function showVideo(videoUrl) {
    currentVideoUrl = videoUrl;

    // Hide other sections
    statusSection.style.display = 'none';
    errorSection.style.display = 'none';

    // Show output section
    generatedVideo.src = videoUrl;
    outputSection.style.display = 'block';

    // Reset button
    resetButton();
}

/**
 * Show error message
 */
function showError(message) {
    // Hide other sections
    statusSection.style.display = 'none';
    outputSection.style.display = 'none';

    // Show error section
    errorMessage.textContent = message;
    errorSection.style.display = 'block';

    // Reset button
    resetButton();
}

/**
 * Reset the generate button to its initial state
 */
function resetButton() {
    generateBtn.disabled = false;
    btnText.textContent = 'Generate Video';
    loader.style.display = 'none';
}

/**
 * Handle form submission
 */
videoForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const topic = document.getElementById('topic').value.trim();

    if (!topic) {
        showError('Please enter a topic or text for your video.');
        return;
    }

    // Show loading state
    showLoading();

    try {
        // Start progress
        updateProgress(10, 'Initializing AI agents...');

        // Make API request to create video (this will take a while)
        const startTime = Date.now();

        // Update progress periodically while waiting for response
        const progressInterval = setInterval(() => {
            const elapsed = (Date.now() - startTime) / 1000; // seconds

            if (elapsed < 10) {
                updateProgress(15, 'Generating script with GPT-4o-mini...');
            } else if (elapsed < 20) {
                updateProgress(25, 'Script complete! Creating voiceovers...');
            } else if (elapsed < 40) {
                updateProgress(35, 'Voiceovers in progress with ElevenLabs...');
            } else if (elapsed < 60) {
                updateProgress(50, 'Voiceovers ready! Starting video generation...');
            } else if (elapsed < 120) {
                updateProgress(65, 'Generating video clips with RunwayML...');
            } else if (elapsed < 180) {
                updateProgress(80, 'Video clips rendering...');
            } else {
                updateProgress(90, 'Assembling final video...');
            }
        }, 5000);

        const response = await fetch('/create-video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ topic: topic })
        });

        // Clear the progress interval
        clearInterval(progressInterval);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to generate video');
        }

        // Parse response
        const data = await response.json();

        // Final progress update
        updateProgress(100, 'Video complete!');
        await new Promise(resolve => setTimeout(resolve, 500));

        // Show the generated video
        if (data.video_url) {
            showVideo(data.video_url);
        } else {
            throw new Error('Video URL not found in response');
        }

    } catch (error) {
        console.error('Error generating video:', error);
        showError(error.message || 'An unexpected error occurred. Please try again.');
    }
});

/**
 * Handle download button click
 */
downloadBtn.addEventListener('click', () => {
    if (currentVideoUrl) {
        const link = document.createElement('a');
        link.href = currentVideoUrl;
        link.download = 'viralreel-video.mp4';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
});

/**
 * Handle create new button click
 */
createNewBtn.addEventListener('click', () => {
    // Reset form
    videoForm.reset();

    // Hide output section
    outputSection.style.display = 'none';

    // Clear video
    generatedVideo.src = '';
    currentVideoUrl = null;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

/**
 * Handle retry button click
 */
retryBtn.addEventListener('click', () => {
    errorSection.style.display = 'none';
});

/**
 * Check server health on page load
 */
window.addEventListener('load', async () => {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        console.log('Server status:', data.message);
    } catch (error) {
        console.error('Server health check failed:', error);
    }
});
