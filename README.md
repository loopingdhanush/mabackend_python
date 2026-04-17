# mabackend_python

A Flask-based backend for image generation using **Stable Diffusion**.  
It provides a REST API with queued processing to generate images efficiently.

---

## Features

- Image generation using Stable Diffusion
- Queue-based processing system
- REST API endpoints
- Uses Realistic Vision model
- Supports both GPU and CPU

---

## Prerequisites

- Python 3.8+
- CUDA 11.8+ (for GPU acceleration) OR CPU (slower)
- ~6–8 GB disk space (model)
- ~8 GB VRAM (GPU) or RAM (CPU)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/loopingdhanush/mabackend_python.git
cd mabackend_python
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### Installed Packages

| Package | Purpose |
|---|---|
| `torch` | Deep learning framework |
| `diffusers` | Stable Diffusion pipeline |
| `transformers` | Model handling |
| `accelerate` | Performance optimization |
| `safetensors` | Safe model storage |
| `flask` | Backend framework |
| `pillow` | Image processing |

---

## Model Setup

The server expects the model at:

```
models/realistic-vision/
```

### Option A (Recommended)

```bash
python model_prepare.py
```

### Option B

```bash
python model_downloader.py
```

- Downloads: `SG161222/Realistic_Vision_V5.1_noVAE`
- Saves to: `./models/realistic-vision/`
- Time: 5–15 minutes

---

## Project Structure

```
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
```

---

## Running the Server

```bash
python server.py
```

### Expected Output

```
Checking hardware...
Using device: cuda (or cpu)
Loading model...
Model ready
 * Running on http://0.0.0.0:8000
```

Server runs at: **http://localhost:8000**

---

## API Endpoints

### 1. Generate Image

**POST** `/generate`

**Request**
```json
{
  "prompt": "a beautiful landscape with mountains"
}
```

**Response**
```json
{
  "task_id": "uuid-string"
}
```

---

### 2. Queue Status

**GET** `/queue`

**Response**
```json
{
  "current": {
    "task_id": "uuid",
    "prompt": "..."
  },
  "pending": [],
  "length": 2
}
```

---

### 3. Get Result

**GET** `/result/<task_id>`

Returns: Generated PNG image

---

### 4. Health Check

**GET** `/health`

```json
{
  "status": "running",
  "queue": 0
}
```

---

## Example Usage

```bash
# Generate image
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cat wearing sunglasses"}'

# Check queue
curl http://localhost:8000/queue

# Download result
curl http://localhost:8000/result/<task_id> -o output.png
```

---

## Configuration

Edit `server.py` to customize:

| Parameter | Description | Default |
|---|---|---|
| `MODEL_PATH` | Model location | `models/realistic-vision/` |
| `num_inference_steps` | Speed vs quality | `16` |
| `guidance_scale` | Prompt adherence | `7` |
| `height` / `width` | Output resolution | `512x512` |
| `negative_prompt` | Terms to exclude | — |
| `port` | Server port | `8000` |

---

## Troubleshooting

| Issue | Solution |
|---|---|
| CUDA out of memory | Reduce steps/resolution or use CPU |
| Model not found | Run `python model_prepare.py` |
| `ImportError: torch` | Reinstall dependencies |
| Port already in use | Change port in `server.py` |
| Slow generation | Use GPU or reduce steps |

---

## Performance

| Hardware | Speed | Memory |
|---|---|---|
| RTX 3090 | ~15s/image | ~20GB VRAM |
| RTX 3060 | ~30s/image | ~12GB VRAM |
| RTX 2080 | ~45s/image | ~11GB VRAM |
| CPU (i7) | ~300s/image | ~16GB RAM |

---

## Optimization Tips

- Use GPU for best performance
- Reduce `num_inference_steps` for faster results
- Enable memory optimizations:

```python
pipe.enable_attention_slicing()
pipe.enable_vae_slicing()
```

---

## License

Refer to the Hugging Face model card:  
[SG161222/Realistic_Vision_V5.1_noVAE](https://huggingface.co/SG161222/Realistic_Vision_V5.1_noVAE)
