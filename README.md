# 🤖 AI Workplace Productivity Assistant

An AI-powered productivity suite built with **Streamlit** and **Google Gemini**
for the **Capaciti AI Skill Accelerator Programme**.

## ✨ Modules

| # | Module | Description |
|---|--------|-------------|
| 1 | 📄 AI Resume Builder | ATS-optimised resumes with Markdown & HTML export |
| 2 | ✉️ Smart Email Generator | Tone & audience-aware professional emails |
| 3 | 📝 Meeting Notes Summarizer | Key points, decisions, actions, owners, risks |
| 4 | 📅 AI Task Planner | Priorities, timelines, definitions of done |
| 5 | 🔎 AI Research Assistant | Executive summaries & key insights |
| 6 | 💬 AI Workplace Chatbot | Multi-turn conversational assistant |

## 🔐 Responsible AI

Every module includes:
- Persistent AI disclaimers
- Bias & fairness warnings
- Validation prompts
- No hard-coded API keys (session / secrets only)

## 🚀 Deploy on Streamlit Cloud

### 1. Get a Gemini API key
Visit https://aistudio.google.com/app/apikey and click **Create API key**.

### 2. Push this repo to GitHub

```bash
git init
git add .
git commit -m "AI Productivity Assistant"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
