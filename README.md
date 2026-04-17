Setup Guide for mabackend_python
This is a Flask-based backend for image generation using Stable Diffusion. It provides a REST API to generate images with queued processing.

Prerequisites
Python 3.8+
CUDA 11.8+ (for GPU acceleration) or CPU (slower)
~6-8GB of disk space for the model
~8GB of VRAM (GPU) or RAM (CPU)
Installation
1. Clone the Repository
bash
git clone https://github.com/loopingdhanush/mabackend_python.git
cd mabackend_python
2. Create Virtual Environment (Recommended)
bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
pip install -r requirements.txt
This installs:

torch - Deep learning framework
diffusers - Stable Diffusion pipeline
transformers - Model transformers
accelerate - Performance optimization
safetensors - Safe model storage
flask - Web framework
pillow - Image processing
4. Download and Prepare the Model
The server expects the model at models/realistic-vision. You have two options:

Option A: Automatic Download (Recommended)

bash
python model_prepare.py
Option B: Alternative Download Script

bash
python model_downloader.py
Both scripts will:

Download the SG161222/Realistic_Vision_V5.1_noVAE model from Hugging Face
Save it to ./models/realistic-vision/
This takes 5-15 minutes depending on your internet speed
Expected folder structure after download:

Code
mabackend_python/
├── models/
│   └── realistic-vision/
│       ├── text_encoder/
│       ├── tokenizer/
│       ├── unet/
│       ├── vae_decoder/
│       ├── safety_checker/
│       ├── feature_extractor/
│       └── model_index.json
├── server.py
├── requirements.txt
└── ...
Running the Server
bash
python server.py
You should see output like:

Code
Checking hardware...
Using device: cuda  (or cpu)
Loading model...
Model ready
 * Running on http://0.0.0.0:8000
The server will start on http://localhost:8000

API Endpoints
1. Generate Image
POST /generate

Request body:

JSON
{
  "prompt": "a beautiful landscape with mountains"
}
Response:

JSON
{
  "task_id": "uuid-string"
}
2. Check Queue Status
GET /queue

Response:

JSON
{
  "current": {
    "task_id": "uuid",
    "prompt": "..."
  },
  "pending": [...],
  "length": 2
}
3. Get Result
GET /result/<task_id>

Returns: PNG image file (when ready)

4. Health Check
GET /health

Response:

JSON
{
  "status": "running",
  "queue": 0
}
Example Usage
bash
# Generate an image
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cat wearing sunglasses"}'

# Check queue status
curl http://localhost:8000/queue

# Get the result (replace with your task_id)
curl http://localhost:8000/result/your-task-id -o output.png
Configuration
Edit server.py to customize:

MODEL_PATH (line 12): Change model location
num_inference_steps (line 74): Quality vs speed (default: 16)
guidance_scale (line 75): Prompt adherence (default: 7)
height/width (lines 76-77): Output resolution (default: 512x512)
negative_prompt (lines 62-65): Terms to exclude from generation
Port (line 144): Change server port (default: 8000)
Troubleshooting
Issue	Solution
CUDA out of memory	Reduce num_inference_steps or height/width, or use CPU
Model not found	Run python model_prepare.py first
ImportError: torch	Run pip install -r requirements.txt again
Port already in use	Change port in server.py line 144
Slow generation	Use GPU (install CUDA), or reduce inference steps
Performance Tips
GPU: Generates ~1 image every 20-30 seconds (GTX 1080+)
CPU: Generates ~1 image every 5+ minutes
Use enable_attention_slicing() and enable_vae_slicing() to reduce memory usage (already enabled)
Reduce num_inference_steps for faster but lower-quality results
Hardware Requirements
Hardware	Speed	Memory
RTX 3090	~15s/image	~20GB VRAM
RTX 3060	~30s/image	~12GB VRAM
RTX 2080	~45s/image	~11GB VRAM
CPU (i7)	~300s/image	~16GB RAM
License
Refer to the Hugging Face model card: SG161222/Realistic_Vision_V5.1_noVAE
