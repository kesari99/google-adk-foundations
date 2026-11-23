from os import getenv

from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm



load_dotenv()

openrouter_model = LiteLlm(
    model="openrouter/nvidia/nemotron-3-ultra-550b-a55b:free",
    api_key=getenv("OPENROUTER_API_KEY")
)

root_agent = Agent(
    model=openrouter_model,
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
