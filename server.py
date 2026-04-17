import torch
import threading
import queue
import uuid
import io

from flask import Flask, request, send_file, jsonify
from diffusers import StableDiffusionPipeline

app = Flask(__name__)

MODEL_PATH = "d:/dhanush/models/realistic-vision"

print("Checking hardware...")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("Using device:", DEVICE)

print("Loading model...")

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    low_cpu_mem_usage=True
)

pipe = pipe.to(DEVICE)

pipe.enable_attention_slicing()
pipe.enable_vae_slicing()

print("Model ready")

task_queue = queue.Queue()
results = {}

queue_state = {
    "current": None,
    "pending": []
}

def worker():

    while True:

        # get next task
        task_id, prompt = task_queue.get()

        # set current job
        queue_state["current"] = {
            "task_id": task_id,
            "prompt": prompt
        }

        # remove first item from pending queue
        if queue_state["pending"]:
            queue_state["pending"].pop(0)

        print("Generating:", prompt)

        negative_prompt = """
        human, person, mannequin, model, body, face, arms,
        watermark, logo, text
        """

        try:

            with torch.inference_mode():

                image = pipe(
                    prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=16,
                    guidance_scale=7,
                    height=512,
                    width=512
                ).images[0]

            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            # store result
            results[task_id] = img_bytes

            print("Finished task:", task_id)

        except Exception as e:

            print("Generation failed:", e)
            results[task_id] = None

        finally:

            # clear current job
            queue_state["current"] = None

            task_queue.task_done()

thread = threading.Thread(target=worker, daemon=True)
thread.start()

@app.route("/generate", methods=["POST"])
def generate():

    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt missing"}), 400

    task_id = str(uuid.uuid4())
    task_queue.put((task_id, prompt))
    queue_state["pending"].append({
        "task_id": task_id,
        "prompt": prompt
    })
    print("Queued:", task_id)
    return jsonify({
        "task_id": task_id
    })

@app.route("/queue")
def queue_status():

    return jsonify({
        "current": queue_state["current"],
        "pending": queue_state["pending"],
        "length": task_queue.qsize()
    })

@app.route("/result/<task_id>")
def get_result(task_id):
    if task_id not in results:
        return jsonify({"status":"processing"})
    img = results.pop(task_id)
    return send_file(img, mimetype="image/png")

@app.route("/health")
def health():
    return {"status": "running", "queue": task_queue.qsize()}

app.run(host="0.0.0.0", port=8000)