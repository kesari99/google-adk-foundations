

from dotenv import load_dotenv
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
import asyncio
from agent import root_agent
from google.genai import types


load_dotenv()

session_service_in_memmory = InMemorySessionService()

initial_state = {
    "name":"kesari",
    "data": """ I am Kesari Devaraya, a software engineer with a passion for developing innovative solutions.
        I love IPL and my favorite team is RCB and favorite player is Virat Kholi.
    """,
}

APP_NAME = "Answer Agent"
USER_ID="kesari"
SESSION_ID = "kesari_session"


async def main():
    current_session = await session_service_in_memmory.create_session(
        session_id=SESSION_ID,
        user_id=USER_ID,
        app_name=APP_NAME,
        state=initial_state
    )

    print(f"Session created with id: {SESSION_ID}")

    created_sessions = await session_service_in_memmory.list_sessions(
        user_id=USER_ID,
        app_name=APP_NAME
    )
    print(f"Created sessions: {created_sessions}")

    runner = Runner(
        agent=root_agent,
        session_service=session_service_in_memmory,
        app_name=APP_NAME,
    )

    new_message = types.Content(
        role="user",
        parts = [types.Part(text='Which is my Favourite team in ipl')]

    )

    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=new_message)
    print(f"Events: {events}")

    for event in events:
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"Final response: {event.content.parts[0].text}")

asyncio.run(main())