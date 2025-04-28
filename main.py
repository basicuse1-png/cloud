import os
import threading
import subprocess
import gradio as gr
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from flask import Flask

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "DIA TTS Server Running"

def run_flask():
    port = int(os.environ.get('PORT', 7860))
    app.run(host="0.0.0.0", port=port)

def run_dia():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = "nari-labs/dia"
    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True
    )
    model.to(device)
    pipe = pipeline(
        "text-to-speech",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        device=device
    )
    def tts(text):
        speech = pipe(text)
        return (speech["sampling_rate"], speech["audio"])
    demo = gr.Interface(fn=tts, inputs="text", outputs="audio")
    demo.launch(server_name="0.0.0.0", server_port=7861, share=False)

if __name__ == "__main__":
    threading.Thread(target=run_dia).start()
    run_flask()
