from google.adk.agents.llm_agent import LlmAgent
from pydantic import BaseModel, Field


class CapitalOutput(BaseModel):
    capital: str = Field(description="Delhi is the capital of india")


root_agent = LlmAgent(
    model="gemini-3.1-flash-lite",
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="""You are a Capital Information Agent. Given a country, respond ONLY with a JSON object containing the capital. Format: {"capital": "capital_name"}""",
    output_key="capital",
    output_schema=CapitalOutput,
)
