# ⚡ ContentPilot AI

A production-ready **Multi-Agent AI Content Marketing Assistant** built with LangGraph.

Generate:
- Research-backed insights
- SEO blog posts
- LinkedIn content
- Marketing visuals (image prompts + generation)
- Content strategies

All powered by a **multi-agent system with memory, guardrails, and quality validation**.


### 🧠 Architecture

User Query
    ↓
Input Guardrail
    ↓
Query Handler (Intent Detection)
    ↓
LangGraph Workflow
    ├── Research Agent
    ├── Blog Agent
    ├── LinkedIn Agent
    ├── Image Agent
    ├── Strategy Agent
    ↓
Quality Validation
    ↓
Output Guardrail
    ↓
Memory Update

## 🛠️ Tech Stack

- Python 3.11
- LangGraph (multi-agent orchestration)
- LangChain
- OpenAI (LLM + Image)
- Tavily (web search)
- Streamlit (UI)
- Docker (deployment)
- Pytest (testing)

### Project structure

```text
contentpilot-ai/
├── src/
│   ├── agents/
│   │   ├── query_handler.py
│   │   ├── research_agent.py
│   │   ├── content_strategist.py
│   │   ├── blog_writer.py
│   │   ├── linkedin_writer.py
│   │   └── image_generator.py
│   ├── core/
│   │   ├── config.py
│   │   ├── state.py
│   │   └── workflow.py
│   ├── integrations/
│   │   ├── llm_client.py
│   │   ├── search_client.py
│   │   └── image_client.py
│   ├── utils/
│   │   ├── quality_validation.py
│   │   └── export_tools.py
│   └── web_app/
│       └── streamlit_app.py
├── outputs/
├── tests/
├── .env
├── .env.example
└── README.md
```

### Setup (Local)

```bash
git clone <your-repo>
cd contentpilot-ai

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
```

Add API keys in .env

```bash
OPENAI_API_KEY=your_key
TAVILY_API_KEY=your_key
ENABLE_IMAGE_GENERATION=false
```

**Run the app:**
```bash
streamlit run src/web_app/streamlit_app.py
```

```bash
# Tests
pytest -q
```

#### Setup (Docker)

```bash
## 🐳 Run with Docker
cp .env.example .env
docker compose up --build
```

```bash
# Stop the app
docker compose down
```


### Example User queries

**Flow 1:** 

- Research AI trends in retail, create a blog, LinkedIn post, and image idea.
- Research AI-powered personalization in e-commerce, create an SEO blog, LinkedIn post, image prompt, and content strategy.

**Flow 2:**
- I am building a content marketing assistant for SaaS startups.
- Focus the brand voice on clear, practical, founder-friendly content.
- Now research AI lead generation tools and create a LinkedIn post.


- Research AI-powered customer support trends and create a LinkedIn post.

**Multi-intent query:**

- Research AI in retail, create a blog, LinkedIn post, and image prompt.

**Safe query:**

- Research AI tools for small business marketing and create a LinkedIn post.

**Blocked query:**

- Research AI tools for small business marketing and create a LinkedIn post.

- Research AI automation for real estate agents and create a blog and LinkedIn post.

**Flow 3:**
Choose</br>
Blog Template: How-To Guide</br>
LinkedIn Template: Practical Tips</br>
Strategy Template: Weekly Plan</br>

- Research AI automation for local restaurants and create a blog, LinkedIn post, and content strategy.

- Research AI automation for dentists and create a blog, LinkedIn post, image prompt, and content strategy.

**Flow 4:**
- Chat input: Research AI automation for dental clinics and create a blog, LinkedIn post, and image prompt.
- Enter refinement: Make the LinkedIn post shorter and more founder-friendly.
- Click Regenerate LinkedIn

**Image generation query:**
- Research AI automation for restaurants and create an image prompt. (just generates image prompt when image generation setting is set to false)
- Create a clean marketing image idea for AI automation in restaurants.
