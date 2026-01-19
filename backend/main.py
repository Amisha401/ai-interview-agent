from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent, InterviewInput

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/interview")
async def interview(data: InterviewInput):
    try:
        result = run_agent(data)
        return {"response": result}
    except Exception as e:
        print("ERROR IN BACKEND:", e)
        return {"response": "Backend error: " + str(e)}
