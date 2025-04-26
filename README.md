# 🧠 cai - Command-line AI Assistant (for hackers, tinkerers & learners)

> “Just type it. Let AI handle the rest.”

`cai` is a customizable command-line tool powered by AI (Gemini). It helps you summarize man pages and command outputs, fix command errors and chat with an AI assistant — all from your terminal.

---

## ✨ Features

- 📘 **Man Page Simplification and command output analysis**
  - `man ping | cai` → Instantly summarized with examples
  - `your_cmd | cai` → Analyse the output

- 🧠 **AI Query**
  - `cai "what is nmap?"` → Ask anything instantly
  - `cai` → Open interactive chat session

- 🔧 **Command Error Fix**
  - `cai --fix` → Reruns the last failed command, explains the error & suggests fix

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


---

## 📦 Installation

### 🔧 For Linux

```bash
wget https://raw.githubusercontent.com/dip-bash/cai/main/setup_cai.sh && chmod +x setup_cai.sh && ./setup_cai.sh
```
then add gemini api key to "/usr/local/cai/.env"

### 🔧 For Windows
> "coming soon"
