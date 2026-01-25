# 🎓 Agentic Socratic Peer Review

**A Multi-Agent System for Rigorous Research Idea Validation**

![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.10%2B-green) ![LangGraph](https://img.shields.io/badge/LangGraph-0.1-orange) ![Gemini](https://img.shields.io/badge/Google%20Gemini-2.0-blueviolet)

This project implements a **"Socratic Peer Review Ring"** where multiple AI agents, each with a distinct persona and goal, debate your research ideas in real-time. Instead of a simple "yes/no" feedback loop, the system simulates a rigorous academic defense to help you identify novelty, technical debt, and logical fallacies before you write a single line of code.

---

## 🏗️ Architecture

The system uses a **Hub-and-Spoke** architecture managed by a Supervisor agent.

```mermaid
graph TD
    User([👤 User Input]) --> Supervisor{🧠 Supervisor}
    
    Supervisor -->|New Idea?| Novelty[🕵️ Novelty Detector]
    Supervisor -->|Fact Check| Librarian[📚 Librarian]
    Supervisor -->|Feasibility?| Auditor[⚙️ Methodology Auditor]
    Supervisor -->|Attack| Critic[👩‍⚖️ The Critic]
    Supervisor -->|Defend| Proponent[👷 The Proponent]
    
    Novelty -->|Report| Supervisor
    Librarian -->|Report| Supervisor
    Auditor -->|Report| Supervisor
    Critic -->|Rebuttal| Supervisor
    Proponent -->|Defense| Supervisor
    
    subgraph Tools
    Librarian -.-> ArXiv
    Librarian -.-> SemanticScholar
    Novelty -.-> ArXiv
    Novelty -.-> SemanticScholar
    end

