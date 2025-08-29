# Meeting Agent with CrewAI

A simple meeting assistant built with the CrewAI framework that helps with scheduling, agenda planning, and meeting summarization.

## Features

- **Meeting Coordinator**: Schedules and organizes meetings efficiently
- **Agenda Planner**: Creates structured and effective meeting agendas  
- **Meeting Summarizer**: Creates comprehensive meeting summaries and action items

## Setup

### 1. Install Dependencies

```bash
pip install -e .
```

### 2. Configure API Keys

Create a `.env` file in the project root and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Get your API keys from:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/

### 3. Run the Application

```bash
python teams.py
```

## Usage

The script will automatically:
1. Schedule a project kickoff meeting
2. Create a detailed meeting agenda
3. Summarize example meeting notes

You can also use the `handle_meeting_request()` function for custom meeting types:

```python
custom_meeting_details = {
    'participants': 'Engineering Team',
    'duration': '45 minutes',
    'topics': 'Sprint planning and task allocation'
}

result = handle_meeting_request(
    meeting_type="Sprint Planning",
    details=custom_meeting_details
)
```

## Dependencies

- `crewai` - AI agent framework
- `langchain-openai` - OpenAI integration
- `python-dotenv` - Environment variable management

## Configuration

The agents use GPT-4o-mini by default with a temperature of 0.1 for consistent results. You can modify the model and settings in `teams.py`:

```python
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1
)
```
