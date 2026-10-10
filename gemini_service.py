import os
import base64
import json
from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

# Get Gemini API key from .env
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.8-flash"


# ============================================================
# COMMON GEMINI FUNCTION
# ============================================================

def generate_recommendation(
    prompt: str,
    image_data=None,
    mime_type=None
):
    """
    Common Gemini function.

    Parameters:
        prompt      : Text prompt sent to Gemini
        image_data  : Image bytes (optional)
        mime_type   : Image MIME type (optional)

    Returns:
        Gemini generated text
    """

    try:

        # ----------------------------------------------------
        # TEXT + IMAGE REQUEST
        # ----------------------------------------------------

        if image_data:

            # Convert image bytes to Base64
            image_base64 = base64.b64encode(image_data).decode("utf-8")

            interaction = client.interactions.create(
                model=MODEL_NAME,
                input=[
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image",
                        "data": image_base64,
                        "mime_type": mime_type or "image/jpeg"
                    }
                ]
            )

        # ----------------------------------------------------
        # TEXT ONLY REQUEST
        # ----------------------------------------------------

        else:

            interaction = client.interactions.create(
                model=MODEL_NAME,
                input=prompt
            )

        # Return Gemini response
        return interaction.output_text

    except Exception as e:

        error_message = str(e)

        # ----------------------------------------------------
        # RATE LIMIT ERROR
        # ----------------------------------------------------

        if (
            "429" in error_message
            or "Rate limit exceeded" in error_message
        ):

            return """
⚠️ GEMINI API LIMIT REACHED

The Gemini Free Tier has temporarily reached its
request limit.

Please wait and try again later.

Your PocketSmart AI application is working correctly.
"""

        # ----------------------------------------------------
        # GENERAL GEMINI ERROR
        # ----------------------------------------------------

        return f"""
⚠️ GEMINI SERVICE ERROR

The recommendation service could not complete
the request.

Please try again later.

Technical information:
{error_message}
"""


# ============================================================
# HOME INTERIOR PLANNER
# ============================================================

# ============================================================
# HOME INTERIOR PLANNER
# ============================================================

# ============================================================
# HOME INTERIOR PLANNER
# ============================================================

def home_recommendations(
    budget,
    room,
    requirements
):

    prompt = f"""
You are PocketSmart AI.

Create a practical Home Interior Budget Plan.

USER INFORMATION

Total Budget: ₹{budget}

Rooms:
{room}

Requirements:
{requirements}


IMPORTANT:

Return ONLY a valid JSON object.

Do NOT write any explanation before or after the JSON.

Do NOT use markdown.

Do NOT use ```json.

The JSON MUST follow this exact structure:

{{
    "total_budget": {budget},
    "remaining_budget": 500,

    "categories": [

        {{
            "name": "Lighting",
            "allocation": 1500,

            "items": [

                {{
                    "item": "LED Bulb (Warm White)",
                    "description": "Energy-efficient LED bulbs for general lighting.",
                    "price": 100,
                    "quantity": 5,

                    "shopping_links": [
                        {{
                            "label": "Amazon",
                            "url": ""
                        }},
                        {{
                            "label": "Flipkart",
                            "url": ""
                        }},
                        {{
                            "label": "Ikea",
                            "url": ""
                        }},
                        {{
                            "label": "Myntra",
                            "url": ""
                        }},
                        {{
                            "label": "Ajio",
                            "url": ""
                        }}
                    ]
                }}

            ]
        }},


        {{
            "name": "Ceiling Fans",
            "allocation": 2000,

            "items": [

                {{
                    "item": "Havells Ceiling Fan",
                    "description": "Basic functional ceiling fan.",
                    "price": 500,
                    "quantity": 4,

                    "shopping_links": [
                        {{
                            "label": "Amazon",
                            "url": ""
                        }},
                        {{
                            "label": "Flipkart",
                            "url": ""
                        }},
                        {{
                            "label": "Ikea",
                            "url": ""
                        }},
                        {{
                            "label": "Myntra",
                            "url": ""
                        }},
                        {{
                            "label": "Ajio",
                            "url": ""
                        }}
                    ]
                }}

            ]
        }},


        {{
            "name": "Furniture",
            "allocation": 1000,

            "items": [

                {{
                    "item": "Plastic Chair",
                    "description": "Stackable plastic chairs for kitchen or living room.",
                    "price": 250,
                    "quantity": 2,

                    "shopping_links": [
                        {{
                            "label": "Amazon",
                            "url": ""
                        }},
                        {{
                            "label": "Flipkart",
                            "url": ""
                        }},
                        {{
                            "label": "Ikea",
                            "url": ""
                        }},
                        {{
                            "label": "Myntra",
                            "url": ""
                        }},
                        {{
                            "label": "Ajio",
                            "url": ""
                        }}
                    ]
                }},

                {{
                    "item": "Small Wooden Table",
                    "description": "Simple wooden table for dining or side table.",
                    "price": 500,
                    "quantity": 1,

                    "shopping_links": [
                        {{
                            "label": "Amazon",
                            "url": ""
                        }},
                        {{
                            "label": "Flipkart",
                            "url": ""
                        }},
                        {{
                            "label": "Ikea",
                            "url": ""
                        }},
                        {{
                            "label": "Myntra",
                            "url": ""
                        }},
                        {{
                            "label": "Ajio",
                            "url": ""
                        }}
                    ]
                }}

            ]
        }}

    ],

    "additional_suggestions": [

        "Consider purchasing used furniture for further cost savings.",

        "Look for sales and discounts on online marketplaces.",

        "Prioritize essential items and postpone non-essential purchases."

    ]
}}


RULES:

1. Total spending must NOT exceed ₹{budget}.

2. Calculate the allocation values correctly.

3. Calculate remaining_budget correctly.

4. Use Indian Rupees.

5. Consider the selected rooms.

6. Consider the user's requirements.

7. Give practical home interior suggestions.

8. Keep shopping_links as empty URLs if you do not know a real product URL.

9. Return ONLY JSON.
"""

    response = generate_recommendation(prompt)


    # --------------------------------------------------------
    # GEMINI ERROR
    # --------------------------------------------------------

    if response.startswith("⚠️"):
        return response


    # --------------------------------------------------------
    # CLEAN GEMINI RESPONSE
    # --------------------------------------------------------

    try:

        response = response.strip()


        # Remove markdown JSON block

        if "```json" in response:

            response = response.replace(
                "```json",
                ""
            )

        if "```" in response:

            response = response.replace(
                "```",
                ""
            )


        response = response.strip()


        # ----------------------------------------------------
        # FIND JSON OBJECT
        # ----------------------------------------------------

        first_brace = response.find("{")

        last_brace = response.rfind("}")


        if first_brace == -1 or last_brace == -1:

            raise ValueError(
                "Gemini did not return JSON"
            )


        json_text = response[
            first_brace:last_brace + 1
        ]


        # ----------------------------------------------------
        # PARSE JSON
        # ----------------------------------------------------

        data = json.loads(json_text)


        # ----------------------------------------------------
        # ENSURE REQUIRED FIELDS EXIST
        # ----------------------------------------------------

        if "total_budget" not in data:
            data["total_budget"] = budget


        if "categories" not in data:
            data["categories"] = []


        if "additional_suggestions" not in data:

            data["additional_suggestions"] = []


        # ----------------------------------------------------
        # CALCULATE ALLOCATED BUDGET
        # ----------------------------------------------------

        allocated = 0

        for category in data["categories"]:

            allocation = category.get(
                "allocation",
                0
            )

            try:

                allocated += float(allocation)

            except:

                pass


        data["allocated_budget"] = allocated


        # ----------------------------------------------------
        # CALCULATE REMAINING BUDGET
        # ----------------------------------------------------

        data["remaining_budget"] = max(
            0,
            float(budget) - allocated
        )


        return data


    except Exception as e:

        print(
            "HOME GEMINI JSON ERROR:",
            e
        )

        print(
            "RAW GEMINI RESPONSE:"
        )

        print(response)


        # ----------------------------------------------------
        # FALLBACK
        # ----------------------------------------------------

        return {

            "total_budget": budget,

            "allocated_budget": 0,

            "remaining_budget": budget,

            "categories": [],

            "additional_suggestions": [

                "Gemini returned an unexpected response format.",

                "Please try generating the recommendations again."

            ]

        }
# ============================================================
# PARTY PLANNER
# ============================================================



def party_recommendations(
    budget,
    guests,
    event_type,
    venue,
    catering=False,
    decoration=False,
    entertainment=False,
    requirements=""
):

    prompt = f"""
You are PocketSmart AI, a smart party budget planning assistant.

Party Information:

Total Budget: ₹{budget}

Number of Guests: {guests}

Party Type:
{event_type}

Venue:
{venue}

Catering Required:
{catering}

Decoration Required:
{decoration}

Entertainment Required:
{entertainment}

Additional Requirements:
{requirements}

Create a practical party budget plan.

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not add explanations outside the JSON.

Use exactly this structure:

{{
    "total_budget": {budget},
    "allocated_budget": 0,
    "remaining_budget": 0,

    "categories": [
        {{
            "name": "Venue",
            "allocation": 0,
            "items": [
                {{
                    "item": "Venue",
                    "description": "Short description",
                    "price": 0,
                    "quantity": 1,
                    "shopping_links": []
                }}
            ]
        }},

        {{
            "name": "Catering",
            "allocation": 0,
            "items": []
        }},

        {{
            "name": "Decoration",
            "allocation": 0,
            "items": []
        }},

        {{
            "name": "Entertainment",
            "allocation": 0,
            "items": []
        }},

        {{
            "name": "Contingency",
            "allocation": 0,
            "items": []
        }}
    ],

    "additional_suggestions": [
        "Suggestion 1",
        "Suggestion 2",
        "Suggestion 3"
    ]
}}

Rules:

- Do not exceed the total budget of ₹{budget}.
- Consider {guests} guests.
- Consider the party type.
- Consider the venue.
- Include catering only if required.
- Include decoration only if required.
- Include entertainment only if required.
- Keep the plan practical.
- Calculate allocated budget correctly.
- Calculate remaining budget correctly.
- Use Indian Rupees.
- Keep prices realistic.
- Shopping links may be empty if not applicable.
"""

    response = generate_recommendation(prompt)

    # --------------------------------------------------------
    # HANDLE GEMINI ERROR
    # --------------------------------------------------------

    if response.startswith("⚠️"):
        return response

    # --------------------------------------------------------
    # CONVERT RESPONSE TO JSON
    # --------------------------------------------------------

    try:

        response = response.strip()

        if response.startswith("```json"):
            response = response[7:]

        elif response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        return json.loads(response)

    except json.JSONDecodeError:

        return {
            "total_budget": budget,
            "allocated_budget": 0,
            "remaining_budget": budget,
            "categories": [],
            "additional_suggestions": [
                "Gemini returned an unexpected response format.",
                "Please try generating the party plan again."
            ],
            "raw_response": response
        }


# ============================================================
# JEWELRY PLANNER
# ============================================================

# ============================================================
# JEWELRY PLANNER
# ============================================================

def jewelry_recommendations(
    budget,
    occasion,
    style,
    image_data=None,
    mime_type=None
):

    prompt = f"""
You are PocketSmart AI, a smart jewelry recommendation assistant.

User Information:

Budget: ₹{budget}

Occasion:
{occasion}

Preferred Style:
{style}

The user may provide an outfit image.

If an outfit image is provided, analyze ONLY:
- Visible outfit colors
- Clothing style
- Patterns
- Overall fashion style
- Suitable jewelry colors
- Suitable jewelry designs
- Formality of the outfit

Do NOT identify the person.

Create personalized jewelry recommendations.

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not add explanations outside JSON.

Use exactly this structure:

{{
    "total_budget": {budget},

    "remaining_budget": 0,

    "outfit_analysis": {{
        "colors": "Blue, White",
        "style": "Casual",
        "formality": "Informal"
    }},

    "jewelry_recommendations": [

        {{
            "name": "Bracelet",
            "description": "A simple bracelet that matches the outfit.",
            "price": 500,
            "style": "Casual",
            "shopping_links": [
                {{
                    "label": "Amazon",
                    "url": ""
                }},
                {{
                    "label": "Flipkart",
                    "url": ""
                }},
                {{
                    "label": "Bluestone",
                    "url": ""
                }},
                {{
                    "label": "Tanishq",
                    "url": ""
                }},
                {{
                    "label": "CaratLane",
                    "url": ""
                }},
                {{
                    "label": "Myntra",
                    "url": ""
                }}
            ]
        }},

        {{
            "name": "Ring",
            "description": "A simple ring suitable for the occasion.",
            "price": 700,
            "style": "Minimalist",
            "shopping_links": []
        }},

        {{
            "name": "Watch",
            "description": "A stylish watch that complements the outfit.",
            "price": 3000,
            "style": "Classic",
            "shopping_links": []
        }}

    ],

    "styling_tips": [
        "Keep the jewelry minimal to match the outfit.",
        "Choose jewelry colors that complement the outfit.",
        "Avoid using too many accessories together."
    ]
}}

Important rules:

- Do not exceed the budget.
- Calculate remaining_budget correctly.
- Use Indian Rupees.
- Consider the occasion.
- Consider the preferred style.
- Consider the outfit image if provided.
- Give 3 to 5 practical jewelry recommendations.
- Use realistic estimated prices.
- Keep the recommendations within ₹{budget}.
"""

    response = generate_recommendation(
        prompt,
        image_data=image_data,
        mime_type=mime_type
    )

    # --------------------------------------------------------
    # GEMINI ERROR
    # --------------------------------------------------------

    if response.startswith("⚠️"):
        return response

    # --------------------------------------------------------
    # CONVERT GEMINI RESPONSE TO JSON
    # --------------------------------------------------------

    try:

        response = response.strip()

        if response.startswith("```json"):
            response = response[7:]

        elif response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        return json.loads(response)

    except json.JSONDecodeError:

        return {
            "total_budget": budget,
            "remaining_budget": budget,

            "outfit_analysis": {
                "colors": "Not available",
                "style": style,
                "formality": "Not available"
            },

            "jewelry_recommendations": [],

            "styling_tips": [
                "Gemini returned an unexpected response.",
                "Please try generating the recommendations again."
            ],

            "raw_response": response
        }