from ast import mod

from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel
from google.adk import Event, Workflow
from google.genai import types



# city_generator_agent = Agent(
#     model="gemini-3.1-flash-lite",
#     name='city_generator_agent',
#     instruction="""Return the name of a random city.
#       Return only the name, nothing else.""",
# )

# class CityTime(BaseModel):
#     city:str
#     time_info:str

# def look_up_function_time(node_input : str):
#     return CityTime(time_info="10:10 AM", city=node_input)

# city_report_agent = Agent(
#     model="gemini-3.1-flash-lite",
#     name="city_report_agent",
#     input_schema=CityTime,
#     instruction="""Output following line:
#         It is {CityTime.time_info} in {CityTime.city} right now.""",
# )


# def completed_message_function(node_input: str):
#     return Event(content = types.Content(role="model", parts =  [types.Part(f"{node_input} WORKFLOW COMPLETED")]))
    
# root_agent = Workflow(
#     name="root_agent",
#     edges=[
#        ( "START",city_generator_agent, look_up_function_time, city_report_agent,completed_message_function )
#     ]
# )

process_message = Agent(
    name="process_message",
    model="gemini-3.1-flash-lite",
     instruction="""Classify user message into either "BUG", "CUSTOMER_SUPPORT",
      or "LOGISTICS". If you think a message applies to more than one category,
      reply with a comma separated list of categories.
   """,
)

def router(node_input: str):
    routes = node_input.split(",")
    routes = [route.strip() for route in routes]
    return routes 

def response_1_bug():
    return Event(content = types.Content(role="model", parts = [types.Part("Handling Bug")]))

def response_2_support():
    return Event(content = types.Content(role="model", parts = [types.Part("Handling Customer Support")]))

def response_3_logistics():
    return Event(content = types.Content(role="model", parts = [types.Part("Handling Logistics")]))


root_agent = Workflow(
    name="root_agent",
    edges=[
        ("START", process_message, router),
        (router, {
            "BUG": response_1_bug,
            "CUSTOMER_SUPPORT": response_2_support,
            "LOGISTICS": response_3_logistics
        })
        ]
)