## ⚡ TL;DR — Quick Overview

🎥 **Bollywood AI Chat Assistant** is a fun, Hinglish-speaking chatbot that responds with Bollywood-style flair using GPT-4.

**🚀 Live Demo**: *https://gabbar-singh-gpt-production.up.railway.app/*  
**💻 GitHub Repo**: *https://github.com/manasikabra/bollywood-chatbot*

> PS: **Copied the original code from [Mat Miller’s GitHub repository](https://github.com/matdmiller/fasthtml_chat), which served as the foundation and inspiration for building this chatbot. Full credit to him for the elegant, minimal base that made this project possible.**

---

### 🛠️ Tech Stack:
- `FastHTML` + `MonsterUI` – UI framework
- `OpenAI GPT-4` – response engine
- `Cursor` – dev environment
- `Railway` – cloud deployment

---

### 📦 Setup in 5 Steps (for building + deploying)

1. **Set up the project in Cursor**
   - Create a new folder and `main.py` filversion
   - Copy-paste the code from the repo (or [Mat Miller's repo on X](https://x.com/matdmiller/status/1899656268719050758))

2. **Create and activate a virtual environment**
   - Requires system-wide install of [`uv`](https://github.com/astral-sh/uv)
   - Run in terminal:
     ```bash
     uv venv
     source .venv/bin/activate
     ```

3. **Modify the system prompt**
   - Customize `DEFAULT_HISTORY` in `main.py` to include your bot’s personality
   - Ensure the system prompt is always included by using `api_history = DEFAULT_HISTORY.copy()` in the `/send` route

4. **Install Railway CLI on your system**
   - Use Homebrew (macOS):
     ```bash
     brew install railway
     railway login
     ```

5. **Deploy via Railway**
   - From Cursor terminal:
     ```bash
     railway init
     railway up
     ```
   - On Railway Dashboard: **Settings > Generate Domain** to make your chatbot publicly accessible

---

> 💡 For the full backstory, modifications, and deployment steps — check out [`project_journey.md`](https://github.com/manasikabra/bollywood-chatbot/blob/main/project_journey.md).

---

> 💻 **Note:** I’ve developed and tested this project on **macOS**. Some setup steps (like package installation or file paths) may vary slightly across operating systems.\
> 📬 *Feel free to reach out if you need help adapting this to Windows or Linux!*
