# 🧠 cai - Command-line AI Assistant (for hackers, tinkerers & learners)

> “Just type it. Let AI handle the rest.”

`cai` is a customizable command-line tool powered by AI (Gemini). It helps you summarize man pages and command outputs, fix command errors and chat with an AI assistant — all from your terminal.

---

## ✨ Features

- 🧠 **AI-Powered Analysis**
  - Explain man pages
  - Analyze command outputs
  - Fix command errors
    
- 💬 **Interactive Chat Modes**
  - General chat with persona
  - Context-aware analysis chat
    
- ⚡ **Quick Fixes**
  - Diagnose last command error (`--fix` flag)
  - Direct question answering
    
- 🎨 **Rich Terminal Interface**
  - Colorized output
  - Markdown formatting
  - Progress indicators

## Future Updates

- 🔍 **Encoding/Decoding**
  - Encode: `echo "admin" | cai -e base64`
  - Decode: `echo "YWRtaW4=" | cai -d`
  - Auto-detect decoding (Base64, URL, Hex, etc.)

- 🧩 **Modular AI**
  - Easy to switch between Gemini, GPT, or local LLMs
  - Configure in `config/ai_config.json`

- 💬 **Chat About Files**
  - `cai -c file.txt` → Analyze and chat about file contents

## Basic Commands
```bash
# Interactive chat (with persona)
python3 cai.py

# Direct question answering
python3 cai.py "how to unzip a tar.gz file?"

# Analyze man page
man ls | python3 cai.py

# Analyze command output + chat
ps aux | python3 cai.py -c

# Fix last command error
python3 cai.py --fix
```

> "For Ai Persona Configuration Edit config/persona.json"
---

## 📦 Installation

### 🔧 For Linux

```bash
wget https://raw.githubusercontent.com/dip-bash/cai/main/setup_cai.sh && chmod +x setup_cai.sh && ./setup_cai.sh
```
 **then add gemini api key to "/usr/local/cai/.env". You can find api key [here](https://aistudio.google.com/apikey)**

### 🔧 For Windows
> "coming soon"
