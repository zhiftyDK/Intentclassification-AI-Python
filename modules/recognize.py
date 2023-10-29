import queue
import sys
import sounddevice as sd
import json

from vosk import Model, KaldiRecognizer

q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

device = sd.default.device
device_info = sd.query_devices(device, "input")
samplerate = int(device_info["default_samplerate"])
    
model = Model("./data/vosk-model-small-en-us-0.15")

def recognize():
    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=device, dtype="int16", channels=1, callback=callback):
        rec = KaldiRecognizer(model, samplerate)
        transcribing = True
        while transcribing:
            data = q.get()
            if rec.AcceptWaveform(data):
                transcribing = False
                return json.loads(rec.Result())["text"]