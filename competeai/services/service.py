import json
import google.generativeai as genai
from decouple import config  # Import config from python-decouple
from django.http import HttpResponse
import logging

from ..models import DirectRating, InDirectRating

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_report(phrase):
    query = "I am trying to perform a competitor analysis can you list the direct and indirect competitors for the following product description along with their customer rating: " + '"' + phrase + '"' + " in the following format {" + '"' + "result" + '"' + " : [{" + '"' + "direct" + '"' + " : [{" + '"' + "org_name" + '"' + ":company name," + '"' + "cust_Rating" + '"' + ":company rating," + '"' + "market_share" + '"' + ":market share}]},{" + '"' + "indirect" + '"' + " : [{" + '"' + "org_name" + '"' + ":company name," + '"' + "cust_Rating" + '"' + ":company rating," + '"' + "market_share" + '"' + ":market share}]}]} without any explanation and must be in strict format as mentioned without any additional charater like quote or the word json"
    data = initialize_gemini_model(query)
    direct_array = []
    indirect_array = []
    for item in data['result'][0]['direct']:
        direct_array.append(DirectRating(item['org_name'], item['cust_Rating'], item['market_share']))
    for item in data['result'][1]['indirect']:
        indirect_array.append(InDirectRating(item['org_name'], item['cust_Rating'], item['market_share']))
    direct_array.extend(indirect_array)
    jsonstr = json.dumps([comp.__dict__ for comp in direct_array])
    return jsonstr


def get_org_offerings(request):
    query = "what are the core business services and additional services offered by ixigo can you provide in the following format{" + '"' + "result" + '"' + " : [{" + '"' + "core_business_service" + '"' + ": [{" + '"' + "travel" + '"' + ": [" + '"' + "flight" + '"' + "," + '"' + "train" + '"' + "]}]}  without any explanation and any additional character like quote or the word json"
    data = initialize_gemini_model(query)
    return data


def get_industry_category(phrase):
    query = "find the industry from the following prompt : " + phrase + " in the following format{" + '"' + "result" + '"' + " :  " + '"' + "industry" + '"' + "}  without any explanation and any additional character like quote or the word json"
    data = initialize_gemini_model(query)
    if not data:
        return {'result':'Industry'}
    return data

def initialize_gemini_model(query):
    try:
        genai.configure(api_key=config('GOOGLE_API_KEY'))
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        logger.info("gemini prompt: " + query)
        response = model.generate_content([query])
        logger.info("gemini response: " + response.text)
        data = json.loads(response.text)
        return data
    except json.JSONDecodeError:
        logger.info("Failed to parse the JSON response.")
        return None
    except Exception as e:
        logger.info(f"An exception occurred {e}")
        return None
