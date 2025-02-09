#pip install newsdataapi


from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
from os import environ
import json
import logging
from datetime import datetime
from src.File.json_op import read_json_file, write_json_file

# Load environment variables
load_dotenv()
newsdata_api = environ.get("newsdata_api")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
NEWS_STORAGE_PATH = "./data/Cache/news_storage.json"

def get_climate_news():
    today_date = cur_date()
    
    try:
        news_data = read_json_file(NEWS_STORAGE_PATH)
    except Exception as e:
        logging.error(f"Error reading news storage file: {e}")
        news_data = {}
    if news_data:
        stored_date = list(news_data.keys())[0]  # Get the first key (assuming single date stored)
        
        if if_news_exist(stored_date):
            return news_data
        else:
            with open(NEWS_STORAGE_PATH, "w") as file:
                json.dump({}, file)
                logging.info("Old news data cleared as it's outdated.")
    
    try:
        api = NewsDataApiClient(apikey=newsdata_api)
        response = api.latest_api(q="climate", country="in", category = "environment",max_result=20)
        results = response.get("results", [])
    except Exception as e:
        logging.error(f"Error fetching news data from API: {e}")
        return {}
    
    news_storage = {today_date: []}
    
    if results:
        for news in results:
            temp_news = {
                "title": news.get("title"),
                "link": news.get("link"),
                "image_url": news.get("image_url")
            }
            news_storage[today_date].append(temp_news)
    
    try:
        if news_storage[today_date]:
            write_json_file(NEWS_STORAGE_PATH, news_storage)
            logging.info("New climate news data stored successfully.")
        else:
            logging.info("New climate news data is empty.")
    except Exception as e:
        logging.error(f"Error writing news storage file: {e}")
    
    return news_storage



def cur_date():
    return datetime.today().strftime('%Y-%m-%d')

def if_news_exist(stored_date):
    """Checks if the report exists for the current date."""
    try:
        provided_date = datetime.strptime(stored_date, "%Y-%m-%d").date()
        return provided_date == datetime.today().date()
    except (ValueError, TypeError) as e:
        logging.error(f"Invalid date format or missing key: {e}")
        return False

#news_api(q='Pizza',scroll=True,max
# url = "https://www.streamlit.io"
# st.write("check out this [link](%s)" % url)
# st.markdown("check out this [link](%s)" % url)