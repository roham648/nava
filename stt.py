import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

def speech_to_text():
    model = Model("models/vosk-model-small-fa-0.5")
    recognizer = KaldiRecognizer(model, 16000)
    audio_queue = queue.Queue()
    def callback(indata, frames, time, status):
        if status:
            print(status)
        audio_queue.put(bytes(indata))
    print("Listening...")
    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(
                    recognizer.Result()
                )
                text = result.get("text", "")
                if text:
                    return text