import re 
from Data.Const.constants import DONATION_WEBSITES

def generate_html_report(data):
    """Generates an HTML report from the provided disaster data."""
    warning_flags = {
        "is_severe_weather": "🔴" if data["situation_overview"]["is_severe_weather"] else "🟢",
        "is_pollution_high": "🔴" if data["situation_overview"]["is_pollution_high"] else "🟢",
        "today_disaster_active": "🔴" if data["situation_overview"]["today_disaster_active"] else "🟢"
    }
    
    city = data.get("city", "Unknown Location")
    lat = data.get("lat", "")
    lng = data.get("lng", "")
    google_link = f"https://www.google.com/maps/place/{lat},{lng}" if lat and lng else "#"
    
    weather_summary = data['report'].get('weather_summary', 'No data available')
    air_quality_summary = data['report'].get('air_quality_summary', 'No data available')
    today_disaster_summary = data['report'].get('today_disaster_summary', 'No disaster warnings today.')
    precautions_list = ''.join(f'<li>{precaution}</li>' for precaution in data.get('precautions', []))
    historical_warnings = ''.join(f'<li class="card">{warning}</li>' for warning in data.get('historical_disaster_warnings', []))
    emergency_contacts = ''.join(f'<li><strong>{contact["type"]}:</strong> {contact["number"]}</li>' for contact in data.get('contact_information', {}).get('emergency_numbers', []))
    website_links = ''.join(f'<li><strong>{website["name"]}:</strong> <a href="{website["url"]}" target="_blank">{website["url"]}</a></li>' for website in data.get('contact_information', {}).get('websites', []))
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Disaster Report - {city}</title>
        <style>
            body {{ font-family: 'Arial', sans-serif; background-color: #f4f4f4; color: #333; margin: 0; padding: 20px; }}
            .container {{ max-width: 900px; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); margin: auto; }}
            h1 {{ color: #d9534f; text-align: center; margin-bottom: 20px; font-size: 28px; }}
            .location {{ text-align: center; font-size: 18px; margin-bottom: 20px; }}
            .location a {{ color: #007bff; text-decoration: none; font-weight: bold; }}
            .location a:hover {{ text-decoration: underline; }}
            .section {{ margin-bottom: 25px; padding: 20px; border-left: 6px solid #d9534f; background: #ffffff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }}
            .alert {{ background-color: #f8d7da; color: #721c24; padding: 12px; border-radius: 5px; font-weight: bold; border-left: 5px solid #d9534f; }}
            .card {{ background: #e9ecef; padding: 12px; border-radius: 5px; margin-top: 8px; font-weight: bold; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); }}
            ul {{ padding-left: 20px; }}
            .situation ul {{ list-style-type: none; padding: 0; }}
            .situation li {{ font-size: 18px; margin-bottom: 8px; font-weight: bold; }}
            .contact {{ margin-top: 15px; }}
            a {{ color: #007bff; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌍 Disaster Report</h1>
            <div class="location">
                <p>📍 <strong>Location:</strong> {city} | <a href="{google_link}" target="_blank">View on Google Maps</a></p>
            </div>
            <div class="section">
                <h2>🌦️ Weather Summary</h2>
                <p>{weather_summary}</p>
            </div>
            <div class="section">
                <h2>💨 Air Quality Summary</h2>
                <p>{air_quality_summary}</p>
            </div>
            <div class="section">
                <h2>🚨 Today's Disaster Summary</h2>
                <p class="alert">{today_disaster_summary}</p>
            </div>
            <div class="section">
                <h2>🛑 Precautions</h2>
                <ul>{precautions_list}</ul>
            </div>
            <div class="section">
                <h2>📜 Historical Disaster Warnings</h2>
                <ul>{historical_warnings}</ul>
            </div>
            <div class="section situation">
                <h2>📢 Situation Overview</h2>
                <ul>
                    <li><strong>Weather:</strong> {warning_flags['is_severe_weather']}</li>
                    <li><strong>Air Quality:</strong> {warning_flags['is_pollution_high']}</li>
                    <li><strong>Disaster Status:</strong> {warning_flags['today_disaster_active']}</li>
                </ul>
            </div>
            <div class="section">
                <h2>📞 Contact Information</h2>
                <div class="contact">
                    <h3>📟 Emergency Numbers</h3>
                    <ul>{emergency_contacts}</ul>
                    <h3>🌐 Useful Websites</h3>
                    <ul>{website_links}</ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


def generate_news_html(data):
    """Generates an HTML template using news data."""
    try:
        stored_date = list(data.keys())[0]
        news_list = data.get(stored_date, [])
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Climate News</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
                h2 {{ text-align: center; color: #333; }}
                .news-item {{ border-bottom: 1px solid #ddd; padding: 10px; }}
                .news-item:last-child {{ border-bottom: none; }}
                .news-item img {{ max-width: 100%; height: auto; border-radius: 5px; }}
                .news-item a {{ text-decoration: none; color: #007bff; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Climate News ({stored_date})</h2>
        """
        
        for news in news_list:
            html_template += f"""
                <div class="news-item">
                    <h3>{news['title']}</h3>
                    <img src="{news['image_url']}" alt="News Image">
                    <p><a href="{news['link']}" target="_blank">Read more</a></p>
                </div>
            """
        
        html_template += "</div></body></html>"
        
        return html_template
    except Exception as e:
        return "<h2>Error loading news</h2>"


def generate_website_template(website):
    """Generates the individual HTML for each donation platform."""
    return f"""
    <li style="padding: 5px; border-bottom: 1px solid #ddd;">
        🔹 <a href="{website['url']}" target="_blank" 
            style="color: {website['color']}; text-decoration: none; font-weight: bold;">
            {website['name']} {website['emoji']}
        </a>
    </li>
    """
def pay_list_html():
    """Generates a beautifully styled HTML template with dynamically listed disaster relief donation platforms."""

    # Generate the list of HTML templates for each website
    website_html_list = [generate_website_template(site) for site in DONATION_WEBSITES]

    # Join the list into a single string
    joined_website_html = ''.join(website_html_list)

    # Final HTML template with dynamically joined website HTML
    html_template = f"""
    <div style="
        text-align: center;
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 600px;
        margin: auto;
        font-family: Arial, sans-serif;">
        
        <h2 style="color: #d9534f;">🌍 <b>Support Disaster Relief Efforts</b></h2>
        <p style="font-size: 16px; color: #555;">Click on a trusted platform below to donate and help those in need:</p>
        
        <ul style="
            list-style-type: none;
            padding: 0;
            font-size: 18px;
            line-height: 2;
            text-align: left;">
            {joined_website_html}
        </ul>
        <p><b>Every contribution makes a difference! 🙏</b></p>
    </div>
    """

    return html_template


def generate_nearby_html(nearby_info):
    html = """
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Nearby Locations</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 20px;
                background-color: #f4f4f4;
            }
            h2 {
                text-align: center;
                color: #333;
            }
            .container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: center;
            }
            .card {
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                width: 300px;
            }
            .card h3 {
                margin: 0;
                color: #007BFF;
            }
            .card p {
                margin: 5px 0;
                color: #555;
            }
            .map-link {
                display: inline-block;
                margin-top: 10px;
                color: #007BFF;
                text-decoration: none;
                font-weight: bold;
            }
            .map-link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h2>Nearby Locations</h2>
        <div class='container'>
    """
    
    for place in nearby_info:
        google_maps_link = f"https://www.google.com/maps/search/?api=1&query={place['lat']},{place['lon']}"
        distance_str = f"{place['dist']} m" if place['dist'] < 1000 else f"{(place['dist']/1000):.2f} km"
        html += f"""
            <div class='card'>
                <h3>{place['name']}</h3>
                <p><strong>Type:</strong> {place.get('type', 'Unknown')}</p>
                <p><strong>Distance:</strong> {distance_str}</p>
                <p><strong>Address:</strong> {place.get('address','Unknown')}
                <a class='map-link' href='{google_maps_link}' target='_blank'>View on Google Maps</a>
            </div>
        """
    
    html += """
        </div>
    </body>
    </html>
    """
    
    return html

# def pay_list_html():
#     """Generates an HTML template for listing disaster relief donation platforms."""
    
#     html_template = """
#     <div style="text-align: center;">
#         <h2>🌍 <b>Support Disaster Relief Efforts</b></h2>
#         <p>Click on a trusted platform below to donate and help those in need:</p>
        
#         <ul style="list-style-type: none; padding: 0; font-size: 18px;">
#             <li>🔹 <a href="https://www.redcross.org/donate/donation.html" target="_blank"><b>Red Cross</b> ❤️</a></li>
#             <li>🔹 <a href="https://www.unicef.org/take-action" target="_blank"><b>UNICEF Emergency Fund</b> 💙</a></li>
#             <li>🔹 <a href="https://www.gofundme.com/c/act/disaster-relief" target="_blank"><b>GoFundMe Disaster Relief</b> 🏥</a></li>
#             <li>🔹 <a href="https://www.globalgiving.org/disasters/" target="_blank"><b>Global Giving</b> 🌎</a></li>
#             <li>🔹 <a href="https://www.directrelief.org/" target="_blank"><b>Direct Relief</b> 🚑</a></li>
#         </ul>

#         <p><b>Every contribution makes a difference! 🙏</b></p>
#     </div>
#     """
#     return html_template

# def extract_pincode(text):
#     match = re.search(r"/.*?(\b\d{6}\b)", text)  # Looks for a 6-digit number after "/"
#     return match.group(1) if match else None


def extract_pincode(text):
    match = re.search(r"\b\d{6}\b", text)  # Looks for any standalone 6-digit number
    return match.group(0) if match else None
