from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search,AgentTool


def check_order_status(order_id:str) -> dict:
    """
     Return the status of order booking based on the provided order ID.

     INPUT : order_id:booking_reference_number (e.g., "ORD123456")

     Output(dict):  
      {
        "order:str
        "status": str,
        "pnr": str | None,
        "from": str | None,
        to: str | None,
        departure_time: str
      }
    """

    print(f"Checking order status for order ID: {order_id}")

    bookings = {
    "ORD123456": {
        "status": "confirmed",
        "pnr": "ABC123",
        "from": "Hyderabad",
        "to": "Bengaluru",
        "departure_time": "2026-11-05 09:30 AM"
    },
    "ORD123457": {
        "status": "confirmed",
        "pnr": "XYZ789",
        "from": "Delhi",
        "to": "Mumbai",
        "departure_time": "2026-11-06 06:45 PM"
    },
    "ORD123458": {
        "status": "pending",
        "pnr": None,
        "from": "Chennai",
        "to": "Hyderabad",
        "departure_time": "2026-11-08 11:00 AM"
    }
}

    if order_id in bookings:
        info = {"order_id": order_id, **bookings[order_id]}
    else:
        info = {
            "order_id": order_id,
            "status": "not found",
            "pnr": None,
            "from": None,
            "to": None,
            "departure_time": None
        }
    return info

def lookup_product_info(product_name: str) -> dict:
    """
    Return destination/package details such as price, availability, seasons, and highlights.

    Input:
        product_name (str): Destination or package name (e.g., "Paris").

    Output (dict):
        {
            "name": str,
            "avg_price": str,       # Display-friendly price range
            "availability": str,    # "Open", "Limited", "Seasonal", "Not Listed"
            "best_season": str,     # Human-friendly season guidance
            "highlights": list      # Short bullets of attractions or features
        }
    """

    print(f"[destination] looking up: {product_name}")

    # Mock catalog for demo
    catalog = {
        "bali": {
            "avg_price": "$1,299",
            "availability": "Open",
            "best_season": "Apr-Oct",
            "highlights": [
                "Beautiful beaches and resorts",
                "Ubud rice terraces",
                "Temples and cultural experiences",
                "Water sports and snorkeling"
            ]
        },
        "paris": {
            "avg_price": "$1,599",
            "availability": "Limited",
            "best_season": "Apr-Jun, Sep-Oct",
            "highlights": [
                "Eiffel Tower",
                "Louvre Museum",
                "Seine River cruises",
                "French cuisine and shopping"
            ]
        },
        "tokyo": {
            "avg_price": "$1,799",
            "availability": "Open",
            "best_season": "Mar-May, Oct-Nov",
            "highlights": [
                "Mount Fuji views",
                "Shibuya Crossing",
                "Cherry blossom festivals",
                "Traditional Japanese temples"
            ]
        }
    }

    key = product_name.lower().strip()

    if key in catalog:
        info = {
            "name": product_name.title(),
            **catalog[key]
        }
    else:
        info = {
            "name": product_name.title(),
            "avg_price": "Not Available",
            "availability": "Not Listed",
            "best_season": "Unknown",
            "highlights": []
        }

    return info


# SPECIAL AGENTS


# order booking agent
order_agent = Agent(
    model="gemini-3.6-flash",
    name='order_agent',
    description='I handle all booking related inquires and tracking',
    instruction="""You are the Order Agent for a travel booking service. You help users
check the status of their bookings.

How to work:
- Booking references look like "ORD123456". If the user asks about a booking but has not
  given a reference, ask for it. Do not guess or invent one.
- Always call the check_order_status tool with the exact reference the user gave. Never
  answer about a booking from memory or assumption.
- Report only what the tool returns: status, PNR, origin, destination, and departure time.
  Skip any field that is empty.
- If the status is "confirmed", summarise the trip clearly (route, departure time, PNR).
- If the status is "pending", explain the booking is not yet confirmed and has no PNR yet.
- If the status is "not found", say so, suggest the user double-check the reference, and
  offer to look up another one.
- Do not make changes to bookings (cancel, modify, refund). Say you can only check status.
- If the user asks about destinations, prices, or packages, say that is outside your scope
  and that the product team handles it.
- Keep replies short, polite, and plain-text.""",
    tools=[check_order_status]
)

# product search agent
product_agent = Agent(
    model="gemini-3.1-flash-lite",
    name='product_agent',
    description='I provide information about destinations and packages',
    instruction="""You are the Product Agent for a travel booking service. You provide
information about destinations and travel packages.

How to work:
- When the user asks about a destination or package (price, availability, best season,
  highlights), call the lookup_product_info tool with the destination name. Never answer
  these details from your own knowledge.
- If the user has not named a destination, ask which one they are interested in.
- Present the results from the tool: average price, availability, best season, and
  highlights as a short bullet list.
- Availability meanings: "Open" means bookable now, "Limited" means few spots left,
  "Seasonal" means only offered in certain months.
- If availability is "Not Listed" or the price is "Not Available", tell the user we do not
  currently offer that destination. Do not invent details. Offer to check another one.
- If the user wants to compare destinations, call the tool once per destination and
  compare the results side by side.
- Do not check booking status or handle bookings. If asked, say the order team handles it.
- Keep replies friendly, concise, and plain-text.""",
    tools=[lookup_product_info]
)


search_agent = Agent(
    model="gemini-3.1-flash-lite",
    name='search_agent',
    description='I search the web for current, general-knowledge information such as travel advisories, weather, news, and events.',
    instruction="""You are the Search Agent for a travel booking service. You use Google
Search to find up-to-date information from the web.

How to work:
- Use the google_search tool for anything that needs current or external information:
  weather, travel advisories, visa rules, local events, news, opening hours, and similar.
- Base your answer on the search results. Do not present guesses as facts.
- Summarise the findings briefly and clearly. Mention the source or website when it helps
  the user trust the answer.
- If results conflict or look outdated, say so and note the date if one is available.
- If the search finds nothing useful, say that plainly and suggest how the user could
  rephrase the question.
- For travel advice involving safety, health, or visa rules, remind the user to confirm
  with an official source before they travel.
- Do not look up booking status or our own package prices and availability. Say that the
  order and product teams handle those.
- Keep replies concise and plain-text.""",
    tools=[google_search]
)


root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name='root_agent',
    description='I am travel service manager who cordinate all inquires',
    instruction='Answer user questions to the best of your knowledge',
    sub_agents=[product_agent],
    tools=[AgentTool(search_agent), check_order_status]
)
