## ⚡ TL;DR — Quick Overview

🎥 **Bollywood AI Chat Assistant** is a fun, Hinglish-speaking chatbot that responds with Bollywood-style flair using GPT-4.

**🚀 Live Demo**: *https://gabbar-singh-gpt-production.up.railway.app/*  
**💻 GitHub Repo**: *https://github.com/mansikabra/bollywood-chatbot*

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
   - Copy-paste the code from the repo (or Mat Miller’s base code if starting fresh)

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

> 💡 For the full backstory, modifications, and deployment steps — [scroll down](#project-journey-building-my-chatbot) or check out `project_journey.md`.

---

> 💻 **Note:** I’ve developed and tested this project on **macOS**. Some setup steps (like package installation or file paths) may vary slightly across operating systems.\
> 📬 *Feel free to reach out if you need help adapting this to Windows or Linux!*

---

## 📅 Project Journey: Building My Chatbot

### Step 1: Discovering the Idea

It all started with a post by [Mat Miller on X](https://x.com/matdmiller/status/1899656268719050758), where he shared:

> *"It's just a single file that's ~100 lines of code to make it easy to work with and easy to paste into your favorite LLM."*

This piqued my interest—it sounded minimal, manageable, and worth exploring.

### Step 2: Exploring the GitHub Repository

The X post linked to Mat Miller’s GitHub repo: [fasthtml_chat](https://github.com/matdmiller/fasthtml_chat).

I checked out the following files:

- **`main.py`**: The core code file—just around 100 lines, easy to read.
- **`README.md`**: Simple and clear docion.

The simplicity of the setup and idea encouraged me to try it out myself.

### Step 3: Setting Up the Project in Cursor

I decided to build and run everything in **Cursor** – an AI-powered code editor that integrates nicely with development workflows.

#### a) Create a New Project Folder

```bash
mkdir Chatbot
```

#### b) Create the Main Python File

Inside the folder:

```bash
touch main.py
```

Copy-pasted the full code from Mat Miller’s main.py file..

#### c) Set Up and Activate a Virtual Environment

To isolate dependencies specific to this project, I used a virtual environment. This helps avoid conflicts with globally installed packages.

```bash
uv venv
source .venv/bin/activate
```

To verify it's activated:

```bash
which python
which pip
```

Should point to `.venv`.

#### d) Create `requirements.txt`

This file lists all the dependencies your project needs to install.

```
python-fasthtml
monsterui
openai
python-dotenv
```

Then install:

```bash
uv pip install -r requirements.txt
```

#### e) Create `.env`

Since we’re working with an AI model (OpenAI), we need to use an API key.

```
OPENAI_API_KEY="your-api-key-here"
```

> Keeps sensitive data secure. instead of hardcoding them into your main code files. It also makes it easier to share the code without exposing your credentials.

### Step 4: Running the Chatbot Locally

```bash
python main.py
```

Visit `http://127.0.0.1:8000` to view the chatbot.

This gave me a working baseline before modifying or customizing anything.

> ✅ Tip: You can include screenshots for reference:
>
> - Terminal output
> - Chatbot UI
> - Sample conversation

---

### Step 5: Modifying the Code

I customised the chatbot to add Bollywood personality, improve message handling, and clean up the UI.

#### a) Custom System Prompt & Assistant Intro

Updated the `DEFAULT_HISTORY` that guides the assistant’s responses and defines the bot’s personality and behaviour.

Modified system message:

```python
{
    "role": "system",
    "content": (
        "You are a Bollywood-style AI assistant who MUST follow these rules:\n"
        "1. ALWAYS respond in Hinglish (mix of Hindi and English)\n"
        "2. Include ONE relevant Bollywood reference or dialogue in each response\n"
        "3. Keep responses SHORT and PUNCHY unless the question needs detailed explanation\n"
        "4. Focus on being entertaining rather than preachy\n"
        "5. Use popular Bollywood dialogues creatively but don't overdo it\n\n"
        "Example short responses:\n"
        "If asked 'how are you': 'Ekdum first class, boss! 😎'\n"
        "If there's an error: 'Galti ek haadsa hai... let's fix it!'\n"
        "If something works: 'Ye to full combo hai, mere bhai! 🚀'\n\n"
        "Remember: Be crisp and fun, go detailed only when necessary!"
    )
}
```

And for the assistant’s intro message:

```python
{
    "role": "assistant",
    "content": (
        "Namaste dosto! 🎥 Main hoon aapka filmy AI assistant - "
        "short mein baat karunga, point pe aaunga, aur filmy style mein jawab dunga! "
        "Poocho poocho! ✨"
    )
}
```

#### b) Ensured System Prompt Is Always Used

The original code simply passed the current history from the frontend to the OpenAI API, which means any modifications to the system prompt would get lost after the first message.

To fix this, I created a separate api_history which always starts with DEFAULT_HISTORY, ensuring the system prompt is always sent.

So, in @rt('/send'), I added logic to:
- Copy the original DEFAULT_HISTORY
- Combine it with current conversation messages (excluding system)
- Use this combined history for the OpenAI API

```python
api_history = DEFAULT_HISTORY.copy()
current_history = [msg for msg in json.loads(history) if msg["role"] != "system"]
api_history.extend(current_history)
```

💡 This keeps the bot’s behavior consistent across multiple user inputs.

#### c) Hide System Messages in UI

Filtered system messages out from visible chat by updating create_chat_messages_ui() and homepage() with:

```python
visible_messages = [msg for msg in messages if msg["role"] != "system"]
```

⚠️ Bonus fix: On each new user message, the assistant’s intro was reappearing due to how the messages were being updated. Separating api_history (for logic) and display_history (for UI) solved this cleanly.

#### d) Add Personality: Bot + User Names

```python
display_names = {
  'user': 'Pappu',
  'assistant': 'Shahenshah-e-Filmy',
  'system': 'System'
}
```

#### e) Disable Unused Navbar Items

Commented out links like Home, Chat History, Settings. This keeps the interface clean and focused.

#### f) Load `.env` Securely

This ensures my OPENAI_API_KEY is not hardcoded and keeps sensitive info secure.

```python
from dotenv import load_dotenv
load_dotenv()
```

---

### Step 6: Testing the Bot on Local Network

- Ran the bot locally
- Verified Hinglish + Bollywood replies
- Iterated on the system prompt in DEFAULT_HISTORY:
  - Slight tweaks to tone or rules
  - Modifying examples for better alignment
  - Adding/removing instructions based on observed behavior

💡 Tip: LLM responses can be sensitive to wording in the system prompt. Small changes can lead to big differences in personality and accuracy.

---

### Step 7: Deployment Using Railway 🚀

Once the chatbot was working as expected on my local machine, I deployed it to the web using Railway—a developer-friendly platform for hosting full-stack apps.

#### a) Prepare Files

- `.railwayignore`: `.env`, `.venv/`, `__pycache__/`
- `Procfile`: `web: python main.py`

#### b) Railway Login

- Visit [railway.app](https://railway.app) and sign in with GitHub

#### c) Install Railway CLI

To deploy from my system, I installed the Railway CLI by following their [Quickstart guide](https://docs.railway.com/guides/cli)

```bash
brew install railway
```

💡 Make sure Homebrew is installed on your macOS

Verify it was installed correctly:

```bash
railway login
```

#### d) Link Project from Cursor

```bash
railway init
railway link
railway up
```

---

### Step 8: Hosting & Going Live 🌐

1. Open Railway Dashboard
2. Click on your project
3. Go to **Settings** > **Generate Domain**

> ⚠️ Don’t skip this step — it makes your bot publicly accessible!

**Celebrate:** 🎊 YOUR CHATBOT IS NOW LIVE FOR THE WORLD TO USE!

You can now:
- Share the link with friends
- Use it for demos
- Collect feedback
- Or just show off your filmy AI sidekick 😅

---

### 🔧 Additional Tip: Updating After Deployment

Want to update the live chatbot after code changes?

```bash
railway init
railway up
```

That’s it. Quick and easy re-deploy!

---

