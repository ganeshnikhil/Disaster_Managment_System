import google.generativeai as genai
from dotenv import load_dotenv
from os import environ
from Data.Const.prompt import structured_prompt
import json 
import re 

# Load environment variables
load_dotenv()
genai_key = environ.get("genai_key")

def parse_json_response(response):
    # Use regex to find and extract the JSON part between ```json and ```
    match = re.search(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
    
    if match:
        try:
            # Extract the JSON part and parse it
            json_data = match.group(1)
            return json.loads(json_data) 
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    else:
        print("No JSON data found.")
    return 

def configure_genai(api_key):
    """
    Configures the GenAI API with the given API key.
    """
    if not api_key:
        raise ValueError("API key for GenAI is not provided.")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def construct_prompt(data):
    """
    Constructs the structured prompt for generating SQL queries.
    
    """
    return f'''{structured_prompt}\n{data}'''


def generate_report(data):
    """
    Generates an diaster report using Google GenAI.
    """
    try:
        # Step 1: Configure GenAI
        model = configure_genai(genai_key)
        
        # Step 2: Construct the prompt
        prmpt = construct_prompt(data)
        
        # Step 3: Generate response
        response = model.generate_content(prmpt)
        # Step 4: Handle and return the response
        if response and hasattr(response, 'text'):
            result = parse_json_response(response.text)
            return result 
    except Exception as e:
        print(f"Error:{e}")
        