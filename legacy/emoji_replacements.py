# Emoji replacements for better Linux compatibility
# Maps emoji characters to text-based alternatives

EMOJI_REPLACEMENTS = {
    # Interface elements
    "🤖": "[AI]",
    "🔍": "[SEARCH]",
    "📚": "[DOCS]",
    "📅": "[DATE]",
    "📄": "[PDF]",
    "⚙️": "[CONFIG]",
    "📊": "[STATS]",
    "🖥️": "[SYS]",
    "⚠️": "[!]",
    "✅": "[OK]",
    "❌": "[ERR]",
    "🎯": "[TARGET]",
    "💡": "[TIP]",
    "🔑": "[KEY]",
    "🧠": "[AI]",
    
    # Categories
    "🤖": "[ROBOT]",
    "🧠": "[AI]", 
    "📊": "[ML]",
    "👁️": "[CV]",
    "⚙️": "[SYS]",
    "🖱️": "[HCI]",
    "💬": "[NLP]",
    
    # Actions & Status
    "⚡": "[PROC]",
    "📝": "[LOG]",
    "🎉": "[SUCCESS]",
    "🚀": "[GO]",
    "✨": "[NEW]",
    "🔧": "[TECH]",
    "📋": "[LIST]",
    "🗓️": "[CAL]",
    "📁": "[FOLDER]",
    "💼": "[WORK]",
    "🎨": "[DESIGN]",
    "🔬": "[RESEARCH]",
    
    # Symbols
    "•": "*",
    "©": "(c)",
    "→": "->",
    "✓": "[+]",
    "×": "[x]"
}

def replace_emojis(text):
    """Replace emojis in text with text-based alternatives"""
    for emoji, replacement in EMOJI_REPLACEMENTS.items():
        text = text.replace(emoji, replacement)
    return text

def clean_text_for_linux(text):
    """Clean text for better Linux tkinter compatibility"""
    # Replace emojis
    text = replace_emojis(text)
    
    # Ensure UTF-8 compatibility
    try:
        text = text.encode('ascii', errors='replace').decode('ascii')
    except:
        pass
        
    return text 