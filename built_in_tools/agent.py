from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search, AgentTool


def calculate_area(shape:str, value:float) -> dict:
    """
    Calculate the area of a given shape.

    Args: 
        shape (str): The shape for which to calculate the area. Supported shapes are "circle", "square", and "rectangle".
        value (float): The value needed to calculate the area. For a circle, this is the radius; for a square, this is the side length; for a rectangle, this is the area.
    """

    if shape.lower() == 'circle':
        area = 3.14159 * (value ** 2)
        return {"status": "success", "report": f"The area of the circle is {area:2f}"}
    elif shape.lower() == 'square':
        area = value ** 2
        return {"status": "success", "report": f"The area of the square is {area:2f}"}
    else:
        return {"status": "error", "message": f"Shape '{shape}' not supported. Please provide a valid shape."}



# root_agent = Agent(
#     model="gemini-3.1-flash-lite",
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
#     tools=[calculate_area]
# )

search_agent = Agent(
    model="gemini-3.1-flash-lite",
    name='search_agent',
    description='A helpful assistant for user questions when needed google search and extraction from internet.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[ google_search]
)

search_agent_tool = AgentTool(search_agent)

root_agent = Agent(
    model="gemini-3.1-flash-lite",
    name='root_agent',
    description='A helpful assistant for user questions when needed google search and extraction from internet.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[ calculate_area, search_agent_tool]
)
