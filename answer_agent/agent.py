from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-3.1-flash-lite",
    name='root_agent',
    description='A helpful assistant for user questions.',
 instruction='''Answer user questions to the best of your knowledge
    You might have to answer questions about the user, their interests, and preferences.
    You can access the same for user {name} in the session state.

    and the data information is:
    {data}
    
    ''')
