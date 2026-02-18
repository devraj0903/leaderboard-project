from fastapi import FastAPI, Form, Request, Query
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# sqlite database
conn = sqlite3.connect("leaderboard.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS scores (name TEXT PRIMARY KEY, score INTEGER)")
conn.commit()

@app.get("/")
def home(request: Request, n: int = Query(10)):
    cur.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT ?", (n,))
    rows = cur.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "rows": rows, "n": n})

@app.post("/submit")
def submit(name: str = Form(...), score: int = Form(...)):
    name = name.strip()
    cur.execute("INSERT OR REPLACE INTO scores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    return RedirectResponse(url="/", status_code=303)
