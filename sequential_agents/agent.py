from re import sub

from google.adk.agents.llm_agent import Agent
from google.adk.agents import SequentialAgent, LlmAgent


def make_translator_agent(lang_code, output_key) : 
    return Agent(
        model="gemini-3.1-flash-lite",
        name=f"translator_agent_{lang_code}",
        description=f"A helpful assistant for translating text to {lang_code}.",
        output_key=output_key,
    )


spanish = make_translator_agent("spanish", "es")
french = make_translator_agent("french", "fr")
german = make_translator_agent("german", "de")

sequential_translate= SequentialAgent(
    name="sequential_translate",
    sub_agents=[spanish, french, german],
    description="A sequential agent that translates text to Spanish, French, and German.",)

root_agent = sequential_translate


# root_agent = Agent(
#     model="gemini-3.5-flash-lite",
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )
