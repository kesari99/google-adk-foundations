

from datetime import datetime
import logging
from zoneinfo import ZoneInfo

from google.adk import Agent


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def after_model_callback(callback_context, llm_response):
    logging.info(f"Model response: {llm_response}")
    logging.info(f"Callback context: {callback_context}")

def after_tool_callback(tools, args, tool_context, tool_response):
    logging.info(f"Tool response: {tool_response}")
    logging.info(f"Tool context: {tool_context}")

def get_weather_info(city: str) -> dict:
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }

def get_current_time(city:str) -> dict:

    if(city.lower() == "new york"):
        tz_identifyier = "America/New_York"
    else:
        return {
            "status": "error",
            "message": f"City '{city}' not supported. Please provide a valid city."
        }

    tz = ZoneInfo(tz_identifyier)
    now = datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


root_agent = Agent(
    name="weather_agent",
    model="gemini-3.1-flash-lite",
    description="An agent that provides weather information based on user queries.",
    instruction="Please provide the current weather information for a given location. You can ask about temperature, humidity, wind speed, and other weather-related details.",
    tools=[get_weather_info, get_current_time],
    after_model_callback=after_model_callback,
    after_tool_callback=after_tool_callback
    
)

print(root_agent)
