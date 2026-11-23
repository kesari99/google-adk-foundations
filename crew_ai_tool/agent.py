import os

from google.adk.agents.llm_agent import Agent
from google.adk.integrations.crewai import CrewaiTool
from crewai_tools import SerperDevTool

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY environment variable is not set. Please set it in the .env file.")

serper_crewai_tool = SerperDevTool(country='in', locale='in', location="Bangalore, India", n_results=10)

adk_serper_tool = CrewaiTool(name="InternetNewsSearch", description="A tool to search the internet using Serper.dev API.",tool=serper_crewai_tool)

root_agent = Agent(
    model="gemini-3.1-flash-lite",
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge. Use the search tool for current information.',
    tools=[adk_serper_tool]
)
