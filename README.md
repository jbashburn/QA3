# 📰 Daily Value Newsletter

An AI-powered Python app that fetches Tennessee news, summarizes it using OpenAI, and emails it to subscribers daily.

---

## 🚀 Overview

**Daily Value Newsletter** automates the delivery of local news by combining:
- 🗞️ NewsAPI for article retrieval
- 🤖 OpenAI for summarization
- 📧 SendGrid for email delivery
- 🗃️ SQLite for subscriber storage
- 🖥️ Tkinter for a simple GUI

---

## 🧠 How It Works

### `main.py`
Runs the full workflow:
1. Loads API keys from `.env`
2. Fetches news via `fetch_news.py`
3. Summarizes articles via `summarize.py`
4. Gets subscriber emails from `database.py`
5. Sends emails via `emailer.py`

### `fetch_news.py`
Pulls recent Tennessee-related articles using keywords like “Nashville” and “Memphis”.

### `summarize.py`
Uses OpenAI’s GPT model to condense each article into 3–4 sentences.

### `database.py`
Stores subscriber emails in a private SQLite database (`subscribers.db`). Prevents duplicates using a `UNIQUE` constraint.

### `emailer.py`
Formats and sends the newsletter using SendGrid. Each email includes:
- Article title  
- AI-generated summary  
- Link to full article

### `gui.py`
Simple Tkinter interface:
- White background, light blue title  
- Description and email input  
- “Subscribe” button adds email to database

---

## 🔐 Security & Best Practices

- API keys stored in `.env` (not hardcoded)
- `.gitignore` excludes sensitive files like `.env` and `.db`
- Error handling in all modules to prevent crashes
- Placeholder text and email validation in GUI

---

## 🧪 Installation

```bash
pip install -r requirements.txt

Required packages include:
- openai
- sendgrid
- requests
- python-dotenv
- tkinter (built-in for most Python installs)



1. Create a .env file with your API keys:
NEWS_API_KEY=your_newsapi_key
OPENAI_API_KEY=your_openai_key
SENDGRID_API_KEY=your_sendgrid_key
SENDER_EMAIL=your_verified_sender_email 


run the GUI to add subscribers:
python gui.py

S
python main.py

🛠️ Customization
This project is modular and easy to adapt. Developers can:
- Replace keywords in fetch_news.py to target different regions or topics
- Modify the prompt in summarize.py to change tone or length
- Use their own .env file with personal API keys
- Customize the GUI layout or branding
- Expand the database to include timestamps or export features






