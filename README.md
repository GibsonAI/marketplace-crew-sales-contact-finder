# Sales Contact Finder Crew

A CrewAI-powered sales contact finder that identifies and researches potential contacts at target companies for sales outreach.

## Overview

This crew automates the process of:
1. **Company Research** - Gathering comprehensive information about target companies
2. **Organizational Analysis** - Understanding company structure and decision-makers
3. **Contact Discovery** - Finding specific individuals and their contact information
4. **Sales Strategy** - Developing personalized outreach approaches

## Features

- Multi-agent collaboration for comprehensive sales research
- Integration with web scraping and search tools
- Automatic contact storage in GibsonAI database
- Personalized sales strategy generation
- Professional markdown report output

## 🧠 Generate GibsonAI Schema

In [GibsonAI](https://app.gibsonai.com), use the following prompt to create your schema in a new project:

```txt
- I want to create a sales contact aggregator agent. It will store company and contact information.
- Generate a “sales_contact” table with fields (company_id, name, title, linkedin_url, phone, email). Also create a “sales_company” table with fields (name). All string fields, except name, are nullable.
```

Once it's generated, click `Deploy` to Production and then copy the API key from the `Data API` tab.

## ⚙️ Setup Instructions

### 1. Clone the `awesome-gibson` repo

```bash
git clone https://github.com/GibsonAI/marketplace-crew-sales-contact-finder.git
cd marketplace-crew-sales-contact-finder
```

### 2. Create your `.env` file

```bash
cp .env.example .env
```

Update `.env` with your keys:

```env
GIBSONAI_API_KEY=your_project_api_key
SERPER_API_KEY=your_serper_api_key
OPENAI_API_KEY=your_openai_api_key
```

> 🔑 Need a Serper key? [Sign up here](https://serper.dev/)

You can also use other LLM model of your choice, not just OpenAI models.

### 3. Create and activate a virtual environment

```bash
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 4. Install dependencies

First, if you haven't already, install uv:

```bash
pip install uv
```

Next install dependencies:

```bash
uv pip install -e .
```

## 🚀 Running the Crew

```bash
crewai run
```

## Agents

### 1. Company Researcher
- **Role**: Gathers comprehensive company information
- **Tools**: SerperDevTool, ScrapeWebsiteTool
- **Focus**: Industry analysis, recent news, technology initiatives

### 2. Organizational Structure Analyst
- **Role**: Analyzes company hierarchy and decision-making
- **Tools**: SerperDevTool, ScrapeWebsiteTool
- **Focus**: Identifying key roles and departments

### 3. Contact Finder
- **Role**: Locates specific individuals and contact information
- **Tools**: SerperDevTool, ScrapeWebsiteTool, ContactStorageTool
- **Focus**: Finding decision-makers and their contact details

### 4. Sales Strategist
- **Role**: Develops personalized outreach strategies
- **Tools**: None (uses information from other agents)
- **Focus**: Creating actionable sales approaches

## Output

The crew generates:
- **JSON Contact Data**: Stored automatically in GibsonAI database
- **Sales Strategy Report**: Markdown file with personalized outreach strategies
- **Console Output**: Real-time progress and results

## Configuration

- **Agents**: Configured in `src/sales_contact_finder_crew/config/agents.yaml`
- **Tasks**: Configured in `src/sales_contact_finder_crew/config/tasks.yaml`
- **Tools**: Custom tools in `src/sales_contact_finder_crew/tools/`

## API Integration

The crew automatically stores discovered contacts in your GibsonAI database using the hosted API. Make sure to:
1. Set up your `GIBSONAI_API_KEY` environment variable
2. Ensure your GibsonAI project has the sales contact schema deployed

## Example Output

Generated contact information with sales strategy will be saved to:

```txt
output/
└── buyer_contact.md
```

```markdown
# Sales Strategy Report for Example Corp

## Executive Summary
Based on our research, Example Corp is actively expanding their AI initiatives...

## Company Analysis
- Industry: Technology/SaaS
- Size: 500+ employees
- Recent funding: $50M Series B
...

## Target Contacts
1. **John Smith** - VP of Engineering
   - LinkedIn: https://linkedin.com/in/johnsmith
   - Email: john.smith@example.com
   - Background: 10+ years in AI/ML...

## Outreach Strategy
### For VP of Engineering (John Smith)
- Value Prop: Focus on technical efficiency gains...
- Pain Points: Current manual processes, scaling challenges...
- Recommended Approach: Technical demo, ROI calculator...
```

## Development

### Project Structure
```
sales_contact_finder_crew/
├── src/sales_contact_finder_crew/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── crew.py                 # Crew definition
│   ├── config/
│   │   ├── agents.yaml         # Agent configurations
│   │   └── tasks.yaml          # Task configurations
│   └── tools/
│       ├── __init__.py
│       └── contact_storage_tool.py  # Custom tool for storing contacts
├── pyproject.toml              # Project configuration
└── README.md
```

### Adding New Tools
1. Create tool in `src/sales_contact_finder_crew/tools/`
2. Import and add to relevant agents in `crew.py`
3. Update agent configurations if needed

### Customizing Agents/Tasks
Edit the YAML files in the `config/` directory to modify agent roles, goals, backstories, task descriptions, and expected outputs.
