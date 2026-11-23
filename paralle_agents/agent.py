
from google.adk.agents import SequentialAgent, Agent,ParallelAgent


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


parallel_agents = ParallelAgent(
    name='Parallel_Translator',
    description='Generate localized marketing taglines for Spanish, French, and German audiences.',
    sub_agents=[spanish, french, german])

merger_agent = Agent(
    model="gemini-3.1-flash-lite",
    name='merger_agent',
    description='A helpful assistant for merging translations.',
    instruction='''You are a Merger Agent. Your task is to merge the translations from Spanish, French, and German into a single coherent output. 
    The input will be a JSON object containing the translations in the following format:
    {
        "es": "Spanish translation",
        "fr": "French translation",
        "de": "German translation"
    }
    
    Your output should be a single string that combines the translations in a meaningful way.
    
    Please ensure that the merged output maintains the essence of the original message while being culturally appropriate for all three languages.
    
    ''')

pipeline = SequentialAgent(
    name='Sequential_Translator',
    description='A sequential agent that translates text to Spanish, French, and German, and then merges the translations.',
    sub_agents=[parallel_agents, merger_agent])

root_agent = pipeline