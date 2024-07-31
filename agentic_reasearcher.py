from crewai import Agent, Task, Crew
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun
import os

os.environ['OPEN_API_KEY']='sk-None-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
OPENAI_API_KEY = os.environ['OPEN_API_KEY']

# Initialize the language model and search tool
llm = OpenAI(temperature=0.7,api_key=os.environ['OPEN_API_KEY'])
search_tool = DuckDuckGoSearchRun()

# Define agents
researcher = Agent(
    role='Researcher',
    goal='Find relevant information on given topics',
    backstory='You are an expert at finding and summarizing relevant information.',
    tools=[search_tool],
    verbose=True,
    llm=llm
)

writer = Agent(
    role='Writer',
    goal='Create well-written, informative responses based on research',
    backstory='You are a skilled writer with expertise in creating clear and concise content.',
    verbose=True,
    llm=llm
)

fact_checker = Agent(
    role='Fact Checker',
    goal='Verify the accuracy of information and claims',
    backstory='You are a meticulous fact-checker with a keen eye for detail and accuracy.',
    tools=[search_tool],
    verbose=True,
    llm=llm
)

# Define tasks
def create_rag_tasks(query):
    research_task = Task(
        description=f"Research the following topic: {query}. Provide a summary of key points.",
        agent=researcher,
        expected_output="A summary of key points related to the query."
    )

    writing_task = Task(
        description="Using the research provided, create a comprehensive and well-structured response to the original query.",
        agent=writer,
        expected_output="A comprehensive, well-structured response to the original query."
    )

    fact_checking_task = Task(
        description="Verify the accuracy of the written response. Check for any factual errors or misleading statements.",
        agent=fact_checker,
        expected_output="A report on the accuracy of the written response, including any corrections or clarifications."
    )

    return [research_task, writing_task, fact_checking_task]

# Create the crew
rag_crew = Crew(
    agents=[researcher, writer, fact_checker],
    tasks=create_rag_tasks("What are the latest developments in renewable energy?"),
    verbose=2
)

# Run the crew
result = rag_crew.kickoff()

print(result)
