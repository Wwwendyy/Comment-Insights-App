import os
import time
import json
import re
import io
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from dashscope import Generation

# Set your API key securely
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dummy login
USERNAME = "admin"
PASSWORD = "password123"

# Use global variable instead of session to store processed results
global_processed_data = []

def analyze_comment(comment: str) -> dict:
    prompt = f"""
You are a helpful assistant. Analyze the following customer comment and return a JSON object with these fields:
- Sentiment: One of Positive, Neutral, or Negative
- Category: A general topic like Delivery, Product Quality, Customer Service, etc.
- Key Themes: A short list of phrases (comma-separated) that summarize the main issues

Customer Comment: "{comment}"

Respond ONLY with a JSON object like:
{{
  "Sentiment": "...",
  "Category": "...",
  "Key Themes": "..."
}}
"""
    try:
        response = Generation.call(
            model='qwen-plus',
            prompt=prompt,
            api_key=DASHSCOPE_API_KEY,
            temperature=0.3,
            top_p=0.8
        )
        text = response.output.get("text", "").strip()
        match = re.search(r"\{.*?\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in response.")
        result = json.loads(match.group())
        return result
    except Exception as e:
        return {"Sentiment": "Error", "Category": "Error", "Key Themes": str(e)}

@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == USERNAME and password == PASSWORD:
        request.session['user'] = username
        return RedirectResponse(url="/upload", status_code=302)
    return RedirectResponse(url="/", status_code=302)

@app.get("/upload", response_class=HTMLResponse)
def upload_form(request: Request):
    if request.session.get('user') != USERNAME:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/process")
def process_file(request: Request, file: UploadFile = File(...)):
    global global_processed_data
    df = pd.read_csv(file.file)

    print("原始行数:", len(df))
    print("列名:", df.columns)

    if 'Comment' not in df.columns:
        df.columns = [col.strip() for col in df.columns]
        if 'comment' in df.columns:
            df.rename(columns={'comment': 'Comment'}, inplace=True)

    results = []
    for i, comment in enumerate(df['Comment']):
        print(f"⏳ 正在处理第 {i+1} 条: {comment}")
        analysis = analyze_comment(comment)
        results.append({
            "Comment": comment,
            "Sentiment": analysis.get("Sentiment", "Unknown"),
            "Category": analysis.get("Category", "Unknown"),
            "Key Themes": analysis.get("Key Themes", "None")
        })
        time.sleep(1.5)

    global_processed_data = results
    print("✅ 处理完成，共", len(global_processed_data), "条")
    return RedirectResponse(url="/results", status_code=302)

@app.get("/results", response_class=HTMLResponse)
def show_results(request: Request):
    if request.session.get('user') != USERNAME:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("results.html", {"request": request, "data": global_processed_data})

@app.get("/download")
def download_csv(request: Request):
    if request.session.get('user') != USERNAME:
        return RedirectResponse(url="/", status_code=302)

    df = pd.DataFrame(global_processed_data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    return StreamingResponse(stream, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=processed_comments.csv"
    })
