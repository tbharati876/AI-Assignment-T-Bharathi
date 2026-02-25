#Install this and run the main program
!pip install fastapi uvicorn pyngrok nest_asyncio
!pip install crewai==0.130.0 crewai-tools==0.47.1 fastapi==0.110.3 uvicorn pyngrok nest_asyncio python-multipart langchain-google-genai pypdf
!pip install langchain
!pip install langchain_google_genai

import os
import uuid
import sqlite3
import nest_asyncio
import uvicorn
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse
from pyngrok import ngrok
from crewai import Agent, Task, Crew, Process

#  1. SETUP
nest_asyncio.apply()
NGROK_TOKEN = "36mSHpSl4DWk4VZO6zTudKO3Piz_2ReYvKNYAz8zPKgUJRMxH"
ngrok.set_auth_token(NGROK_TOKEN)
app = FastAPI(title="VWO Bonus - Queue & DB")

# 2. DATABASE SETUP
DB_NAME = "vwo_production.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Table to track background tasks and store results
    cursor.execute('''CREATE TABLE IF NOT EXISTS task_store
                     (task_id TEXT PRIMARY KEY, filename TEXT, status TEXT, result TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 3. BACKGROUND LOGIC 
def run_ai_in_background(task_id: str, file_path: str, filename: str):
    """The 'Worker' function that runs the heavy AI logic without blocking the API."""
    try:
        # Reusing the LocalFinancialAnalyzer logic from previous steps
        # (Assuming LocalFinancialAnalyzer class is defined as in previous turns)
        # Note: LocalFinancialAnalyzer needs to be defined or imported from previous cells
        # For this fix, I am assuming LocalFinancialAnalyzer is accessible.
        from __main__ import LocalFinancialAnalyzer
        engine = LocalFinancialAnalyzer(file_path)
        analysis_result = engine.run()

        # Update Database with result
        conn = sqlite3.connect(DB_NAME)
        conn.execute("UPDATE task_store SET status='COMPLETED', result=? WHERE task_id=?",
                     (str(analysis_result), task_id))
        conn.commit()
        conn.close()
    except Exception as e:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("UPDATE task_store SET status='FAILED', result=? WHERE task_id=?",
                     (str(e), task_id))
        conn.commit()
        conn.close()

# 4. API ENDPOINTS
@app.get("/", response_class=HTMLResponse)
async def ui():
    return """
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1> VWO Enterprise AI (Queue + DB)</h1>
        <p>Submit a PDF. The system will process it in the background using workers.</p>
        <form action="/analyze" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".pdf" required><br><br>
            <button type="submit">Start Background Analysis</button>
        </form>
    </body>
    """

@app.post("/analyze")
async def start_analysis(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    task_id = str(uuid.uuid4())
    path = f"data/{file.filename}"
    os.makedirs("data", exist_ok=True)
    with open(path, "wb") as f: f.write(await file.read())

    # 1. Store initial task in DB
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO task_store VALUES (?, ?, ?, ?)", (task_id, file.filename, "PENDING", ""))
    conn.commit()
    conn.close()

    # 2. Add to Background Queue (The Simulation)
    background_tasks.add_task(run_ai_in_background, task_id, path, file.filename)

    return {
        "message": "Task queued successfully",
        "task_id": task_id,
        "check_status_url": f"/status/{task_id}"
    }

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT status, result FROM task_store WHERE task_id=?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if not row: return {"error": "Task not found"}
    return {"task_id": task_id, "status": row[0], "result": row[1]}

# 5. LAUNCH 
public_url = ngrok.connect(8000).public_url
print(f" Enterprise UI: {public_url}")

import asyncio 
config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
server = uvicorn.Server(config)

loop = asyncio.get_event_loop()
task = loop.create_task(server.serve())
