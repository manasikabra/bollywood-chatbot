from fasthtml.common import *
from monsterui.all import * 
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create FastHTML app with HTMX websocket extension
app, rt = fast_app(exts='ws', hdrs=Theme.zinc.headers())

DEFAULT_HISTORY = [
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
    },
    {
        "role": "assistant",
        "content": (
            "Namaste dosto! 🎬 Main hoon aapka filmy AI assistant - "
            "short mein baat karunga, point pe aaunga, aur filmy style mein jawab dunga! "
            "Poocho poocho! ✨"
        )
    }
]

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def ChatMessage(role, content):
    """Creates a styled chat message bubble"""
    colors = {
        'system': {'bg': 'bg-gray-200', 'text': 'text-gray-800'},
        'user': {'bg': 'bg-blue-500', 'text': 'text-white'},
        'assistant': {'bg': 'bg-gray-200', 'text': 'text-gray-800'}
    }
    style = colors.get(role.lower(), colors['system'])
    
     # Custom display names for roles
    display_names = {
        'user': 'Pappu',
        'assistant': 'Shahenshah-e-Filmy',
        'system': 'System'
    }
   
    align_cls = 'justify-end' if role.lower() == 'user' else 'justify-start'
    
    return Div(cls=f'flex {align_cls} mb-4')(
        Div(cls=f'{style["bg"]} {style["text"]} rounded-2xl p-4 max-w-[80%]')(
            Strong(display_names.get(role.lower(), role.capitalize()), cls='text-sm font-semibold tracking-wide'),
            Div(content, cls='mt-2')
        )
    )

def create_chat_messages_ui(messages: list[dict]=[]):
    # Filter out system messages when displaying
    visible_messages = [msg for msg in messages if msg["role"] != "system"]

    return Div(
        *[ChatMessage(msg["role"], msg["content"]) for msg in messages],
        Script("document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;"),
        id="chat-messages",
        hx_swap_oob="true",
        cls=("pt-16", "pb-24")
    )

def create_chat_input(history: list[dict]=tuple()):
    return Div(
        Form(
            DivFullySpaced(
                TextArea(
                    id="message", 
                    placeholder="Type your message...", 
                    autofocus=True,
                    hx_on_keydown="""if((event.ctrlKey || event.metaKey || event.shiftKey) && event.key === 'Enter') 
                    { event.preventDefault(); this.closest('form').requestSubmit(); }"""
                ),
                Button(
                    "Send", 
                    id="send-button",
                    type="submit", 
                    cls=("ml-2", ButtonT.primary),
                    uk_tooltip="Press Ctrl+Enter, Cmd+Enter, or Shift+Enter to send"
                ),
                cls="flex items-end gap-2"
            ),
            Input(type="hidden", id="history", value=json.dumps(history)),
            hx_post="/send",
            hx_target="#chat-input",
            hx_swap="outerHTML",
            id="chat-input",
            onsubmit="(() => {b = document.getElementById('send-button'); b.disabled = true; b.innerHTML = '<div uk-spinner></div>';})();"
        ), 
        cls="fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 p-4 shadow-lg"
    )

def create_navbar():
    return NavBar(
        # A("Home", href="#"),
        # A("Chat History", href="#"),
        #A("Settings", href="#"),
        brand=H3("Baatein kuch ankahee si 📽️💬"),
        sticky=True,
        cls="px-6 py-3 shadow-sm bg-background z-50 fixed top-0 left-0 right-0 w-full"
    )

@rt('/')
def homepage():
    # Filter out system messages for initial display
    visible_history = [msg for msg in DEFAULT_HISTORY if msg["role"] != "system"]
    
    return Container(
        create_navbar(),
        Div(create_chat_messages_ui(visible_history), id="chat-container"),
        create_chat_input(DEFAULT_HISTORY)  # Keep full history in the hidden input
    )

@rt('/send', methods=['POST'])
def send_message(message: str, history: str):
    if not message.strip():
        return create_chat_input(json.loads(history))
    
    # Start with DEFAULT_HISTORY for API calls
    api_history = DEFAULT_HISTORY.copy()
    
    # Get the non-system messages from the current history
    current_history = [msg for msg in json.loads(history) if msg["role"] != "system"]
    
    # Add current conversation history to API history
    api_history.extend(current_history)
    
    # Add the new user message
    api_history.append({"role": "user", "content": message})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=api_history,
            temperature=1.0
        )
        
        assistant_message = response.choices[0].message.content
        
        # Create display history (without system message)
        display_history = current_history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": assistant_message}
        ]
        
        # Keep system message in the API history
        api_history.append({"role": "assistant", "content": assistant_message})
        
        return create_chat_input(api_history), create_chat_messages_ui(display_history)
    
    except Exception as e:
        return Alert(f"Error: {str(e)}", cls=AlertT.error)

# Run the app
serve()