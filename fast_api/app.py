# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from generator import generate_music, model, X_seed, length

app = FastAPI()

class NoteRequest(BaseModel):
    note_count: int

@app.post("/generate/")
async def generate_notes(request: NoteRequest):
    melody = generate_music(request.note_count, X_seed, length)
    # Save the generated melody to a MIDI file
    midi_path = 'Melody_Generated.mid'
    melody.write('midi', midi_path)
    return {"midi_file": midi_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
