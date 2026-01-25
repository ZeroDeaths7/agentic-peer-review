Agentic Socratic Peer ReviewA Multi-Agent System for Rigorous Research Idea ValidationThis project implements a "Socratic Peer Review Ring" where multiple AI agents, each with a distinct persona and goal, debate your research ideas in real-time. Instead of a simple "yes/no" feedback loop, the system simulates a rigorous academic defense to help you identify novelty, technical debt, and logical fallacies before you write a single line of code.🏗️ ArchitectureThe system uses a Hub-and-Spoke architecture managed by a Supervisor agent.Code snippetgraph TD
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
🤖 The AgentsAgentPersona & RoleTools🧠 SupervisorThe Router. Analyzes the state of the debate and decides who speaks next (e.g., if a fact is disputed, call the Librarian).None🕵️ Novelty DetectorThe Gatekeeper. Checks if your idea has already been published. Stops "reinventing the wheel" early.ArXiv, Semantic Scholar👩‍⚖️ The Critic"Reviewer #2". Relentlessly attacks logic, finds missing constraints, and highlights weaknesses.None👷 The ProponentThe Architect. "Steel-mans" the user's idea, proposing solutions to the Critic's attacks and defending the vision.None📚 The LibrarianThe Researcher. Fetches live papers to verify claims or find prior art. Purely objective.ArXiv, Semantic Scholar⚙️ Methodology AuditorThe Engineer. Ignores the "vision" and checks technical feasibility (cost, latency, compute limits).None🚀 FeaturesReal-Time Research Tools: The agents don't just hallucinate; they actively search ArXiv and Semantic Scholar to find citations that support or refute your claims.Stateful Debate: The conversation isn't linear. The Supervisor can route the discussion back and forth between Proponent and Critic until a consensus is reached.Feasibility Checks: Dedicated agents ensure your idea isn't just "cool" but actually buildable within modern hardware/cost limits.Interactive UI: Built with Chainlit for a chat-like experience with collapsible "Thinking" steps to show tool usage.🛠️ Installation & SetupPrerequisitesPython 3.10+A Google Cloud Project with the Gemini API enabled (or an API Key from AI Studio).1. Clone the RepositoryBashgit clone https://github.com/yourusername/agentic-peer-review.git
cd agentic-peer-review
2. Install DependenciesBashpip install -r requirements.txt
3. Configure EnvironmentCreate a .env file in the root directory:Ini, TOML# Required: Your Google Gemini API Key
GOOGLE_API_KEY=AIzaSyD...

# Optional: Semantic Scholar API Key (for higher rate limits)
# S2_API_KEY=... 
4. Run the ApplicationBashchainlit run app.py -w
The -w flag enables auto-reload for development.📸 Screenshots(Add your screenshots here once generated)Note on Rate Limits: This project uses Google's Gemini models. The default configuration uses gemini-2.0-flash and gemini-2.0-flash-lite to maximize performance on the free tier. If you encounter 429 Resource Exhausted errors, simply wait a minute for the quota to reset.🗺️ Roadmap[x] MVP: Core Agent Loop (Supervisor, Critic, Proponent).[x] Tool Integration: ArXiv & Semantic Scholar.[x] UI: Chainlit Frontend.[ ] Document Ingestion (RAG): Allow users to upload PDF drafts for specific critique.[ ] Report Generation: Export the debate as a structured Markdown summary.🤝 ContributingContributions are welcome! Please open an issue to discuss proposed changes or submit a Pull Request.📄 LicenseDistributed under the MIT License. See LICENSE for more information.
