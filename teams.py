"""
Simple Meeting Agent using CrewAI Framework
This example creates a meeting assistant that can help with scheduling and summarizing meetings.
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the language model
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.1
)

# Define the Meeting Coordinator Agent
meeting_coordinator = Agent(
    role='Meeting Coordinator',
    goal='Schedule and organize meetings efficiently',
    backstory="""You are an experienced executive assistant who specializes in 
    coordinating meetings. You understand the importance of clear communication,
    proper scheduling, and ensuring all participants are well-prepared.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Define the Meeting Summarizer Agent
meeting_summarizer = Agent(
    role='Meeting Note Taker',
    goal='Create comprehensive meeting summaries and action items',
    backstory="""You are a skilled note-taker who captures the essence of meetings,
    identifies key decisions, and clearly outlines action items with responsible parties
    and deadlines.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Define the Agenda Planner Agent
agenda_planner = Agent(
    role='Agenda Planner',
    goal='Create structured and effective meeting agendas',
    backstory="""You are an expert at creating meeting agendas that ensure productive
    discussions, proper time allocation, and clear objectives for each meeting.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Example Task 1: Schedule a Meeting
schedule_meeting_task = Task(
    description="""Schedule a project kickoff meeting for next week. 
    The meeting should:
    - Be 1 hour long
    - Include the product team, engineering team, and stakeholders
    - Focus on defining project scope and timeline
    - Consider timezone differences (team is distributed across EST and PST)
    
    Provide:
    1. Suggested meeting times (offer 3 options)
    2. Meeting invite template with all necessary details
    3. Pre-meeting preparation checklist for attendees
    """,
    expected_output="A complete meeting scheduling plan with time options, invite template, and preparation checklist",
    agent=meeting_coordinator
)

# Example Task 2: Create Meeting Agenda
create_agenda_task = Task(
    description="""Create a detailed agenda for the project kickoff meeting.
    The agenda should:
    - Have clear time allocations for each topic
    - Include introductions, project overview, scope discussion, timeline review, Q&A
    - Specify the presenter/owner for each agenda item
    - Include any necessary pre-reading or materials
    """,
    expected_output="A structured meeting agenda with time allocations and topic owners",
    agent=agenda_planner
)

# Example Task 3: Summarize Meeting Notes
summarize_meeting_task = Task(
    description="""Based on the following meeting notes, create a comprehensive summary:
    
    Meeting Notes (Example):
    - Discussed new product feature roadmap
    - John presented Q3 timeline - aiming for September launch
    - Sarah raised concerns about resource allocation
    - Team agreed to hire 2 additional developers
    - Budget approval needed from finance by next Friday
    - Design mockups to be ready by end of month
    - Weekly sync meetings scheduled for Tuesdays at 2 PM
    
    Create:
    1. Executive summary (2-3 sentences)
    2. Key decisions made
    3. Action items with owners and deadlines
    4. Follow-up items for next meeting
    """,
    expected_output="A well-structured meeting summary with action items and follow-ups",
    agent=meeting_summarizer
)

# Create the crew with the defined agents and tasks
meeting_crew = Crew(
    agents=[meeting_coordinator, agenda_planner, meeting_summarizer],
    tasks=[schedule_meeting_task, create_agenda_task, summarize_meeting_task],
    process=Process.sequential,  # Tasks will be executed sequentially
    verbose=True
)

# Function to run the meeting agent crew
def run_meeting_agent():
    """Execute the meeting agent crew and return results"""
    print("🚀 Starting Meeting Agent Crew...\n")
    print(f"📅 Current Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # Execute the crew
    result = meeting_crew.kickoff()
    
    print("\n✅ Meeting Agent Crew Completed!")
    return result

# Custom function to handle specific meeting requests
def handle_meeting_request(meeting_type, details):
    """
    Handle custom meeting requests
    
    Args:
        meeting_type: Type of meeting (e.g., "standup", "planning", "retrospective")
        details: Dictionary with meeting details
    """
    
    # Create a custom task based on the meeting type
    custom_task = Task(
        description=f"""
        Organize a {meeting_type} meeting with the following details:
        Participants: {details.get('participants', 'Team members')}
        Duration: {details.get('duration', '30 minutes')}
        Topics: {details.get('topics', 'General discussion')}
        
        Please provide:
        1. Meeting agenda
        2. Suggested time slots
        3. Meeting objectives
        """,
        expected_output=f"Complete plan for {meeting_type} meeting",
        agent=meeting_coordinator
    )
    
    # Create a temporary crew for this specific request
    temp_crew = Crew(
        agents=[meeting_coordinator, agenda_planner],
        tasks=[custom_task],
        process=Process.sequential,
        verbose=True
    )
    
    return temp_crew.kickoff()

# Example usage
if __name__ == "__main__":
    # Run the main meeting agent crew
    result = run_meeting_agent()
    print("\n📝 Final Result:")
    print(result)
    
    # Example of handling a custom meeting request
    print("\n" + "="*50)
    print("📌 Custom Meeting Request Example")
    print("="*50 + "\n")
    
    custom_meeting_details = {
        'participants': 'Engineering Team',
        'duration': '45 minutes',
        'topics': 'Sprint planning and task allocation'
    }
    
    custom_result = handle_meeting_request(
        meeting_type="Sprint Planning",
        details=custom_meeting_details
    )
    
    print("\n📝 Custom Meeting Result:")
    print(custom_result)

