# 🧬 Agentic POC: Cancer Gene Data Assistant

A first-working proof-of-concept AI agent that allows non-technical stakeholders to interact with cancer gene data using natural language.

## 🚀 Overview

This project implements a functional, lightweight agentic system designed to:
1.  **Understand natural language queries** about cancer genes and expression values.
2.  **Orchestrate data tools** to retrieve and analyze information from a CSV dataset.
3.  **Provide a web interface** (Streamlit) and a **portable environment** (Docker) for seamless local execution.

### ✅ Success Criteria Met
- **Pragmatic Design:** Focused on delivering a working solution within a 4-hour window.
- **Robust Execution:** Runs on standard hardware (<= 16GB RAM) without requiring a GPU or API keys.
- **Stakeholder Ready:** Non-technical users can interact via a simple chat interface.
- **Dynamic Dataset:** The agent automatically adapts to the available cancers in the CSV.

---

## 🛠️ Quick Start

### Prerequisites
- **Python 3.10+** (if running via Python)
- **Docker** (if running via Container)

### 1. Running with Docker (Recommended)
This approach is the most portable and handles all dependencies automatically.
```bash
# Clone the repository
git clone <repo-url>
cd owk-poc

# Build the image
docker build -t owk-poc .

# Run the container
docker run -p 8501:8501 owk-poc
```
Open your browser to `http://localhost:8501`.

### 2. Running Locally (Python)

#### Windows (PowerShell)
```powershell
# Setup environment
python -m venv venv
.\venv\Scripts\activate

# Install and configure
pip install -r requirements.txt
$env:PYTHONPATH = (Get-Location)

# Run
streamlit run owk_poc/app.py
```

#### Mac
```bash
# Setup environment
python -m venv venv
source venv/bin/activate

# Install and configure
pip install -r requirements.txt
export PYTHONPATH=$(pwd)

# Run
streamlit run owk_poc/app.py
```

---

## 🤖 Supported Queries (Natural Language)

The system handles both exact and variations of the following requirements:
- **Help:** "How can you help me?"
- **Gene Targets:** "What are the main genes involved in lung cancer?"
- **Expression Analysis:** "What is the median value expression of genes involved in breast cancer?"
- **Multi-Cancer Support:** "Show me genes for breast, ovarian, and prostate"
  - *Note: The agent detects multiple entities and provides a stratified, easy-to-read response grouped by cancer type.*
- **Edge Cases:** "What is the median value expression of genes involved in esophageal cancer?"
  - *Note: Since esophageal cancer is not in the provided dataset, the agent provides a helpful response explaining what data is available.*

---

## 🏛️ Architecture & Design Decisions

### Pragmatic AI Implementation
Instead of using a heavyweight LLM (Large Language Model) that would require API keys, complex environment variables, and GPU acceleration, I implemented a **Robust Rules-Based Agent**.

**Why this trade-off?**
- **Zero Latency:** Responses are instant (< 10ms).
- **100% Deterministic:** Zero risk of "hallucinations" (making up data), which is critical in genomic data.
- **Hardware Agnostic:** Fits easily within the 16GB RAM limit and runs on any CPU.
- **Maintenance:** Local logic is easier to test and debug for a first POC.

### AI Component Orchestration
The "Brain" (`owk_poc/agent.py`) acts as a router. It classifies the intent and uses the Function Layer (`owk_poc/tools.py`) to query the Data Layer (Pandas).

---

## 🦾 AI-Assisted Coding: Pros & Cons

This project was developed using AI coding assistance to maximize productivity within the 4-hour constraint.

**Pros:**
- **Velocity:** Rapid generation of Streamlit boilerplate and configurations.
- **Documentation:** Automated generation of initial Markdown templates.

**Cons:**
- **Path Logic Errors:** AI assistants often struggle with complex Python package structures (relative vs absolute imports), requiring manual intervention.
- **Context Oversights:** Occasionally misses subtle business logic requirements (e.g., handling missing cancer types) unless explicitly prompted.
- **Verification:** Every line of code generated requires human review to ensure it meets the specific project "data" constraints.

---

## 🧪 Testing

To verify the agent logic against the requirements locally:
```bash
# Set PYTHONPATH (if not already set)
# Windows: $env:PYTHONPATH = (Get-Location)
# Mac/Linux: export PYTHONPATH=$(pwd)

python -m unittest tests/test_agent.py
```

---

## 🔮 Future Roadmap

To move from this POC to a production-grade Product:
1.  **Hybrid AI Model:** Integrate an LLM (e.g., GPT-4o) as a fallback "Reasoning Engine" for queries that the rule-based agent doesn't understand.
2.  **API Layer:** Move the logic to a FastAPI backend to support multiple frontends (Web, Slack, Teams).
3.  **Data Persistence:** Replace the CSV with a SQL database for better scalability and multi-user access.
