# 🧠 Summary AI 📊

Welcome to Summary AI, your intelligent CSV summarization tool! 🚀

## 📌 Overview

Summary AI is a powerful application that leverages artificial intelligence to analyze and summarize CSV files. It provides concise insights into your data, helping you quickly understand key trends and patterns. 🔍💡

## ✨ Features

- 📁 Easy CSV file upload
- 🤖 AI-powered data analysis
- 📝 Concise summary generation
- 🎨 Sleek and intuitive user interface
- ⚡ Fast processing with local LLM

## 🛠️ Tech Stack

- 🐍 Backend: Python with Flask
- 🧠 AI: LangChain, Ollama, Nomic Embeddings
- 🌐 Frontend: Next.js with shadcn/ui components
- 🗃️ Database: Chroma (vector store)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Ollama (I used the llama3.1:8b model, but you can replace with your preferred model /backend/rag:12)

```
local_llm = "llama3.1:8b" # change model here
```

### Setup

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/summary-ai.git
   cd summary-ai
   ```

2. Set up the backend:

   ```
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

3. Set up the frontend:

   ```
   cd frontend
   npm install
   npm run dev
   ```

4. Open your browser and navigate to \`http://localhost:3000\`

## 🖥️ Usage

1. 📤 Upload your CSV file using the file input.
2. 🚀 Click the "Upload" button to process your file.
3. ⏳ Wait for the AI to analyze your data.
4. 📊 View the generated summary in the text area.

**_Happy Summarizing! 📈🎉_**
