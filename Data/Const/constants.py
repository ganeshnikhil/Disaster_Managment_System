INPUT_TEMPLATE = {   
    "current_date":"2025-01-28",
    "weather": {
    
    },
    "air_quality": {

    },
    "today_disaster": {

    },
    "disaster_history": {

    },
    "contact_information": {
        "emergency_numbers": {
            "Police": "100",
            "Fire Department": "101",
            "Ambulance": "102"
        },
        "websites": {
            "Local Police": "http://bangalorepolice.gov",
            "Red Cross": "http://redcross.org",
            "Club": "http://daneclub.org"
        }
    }
}

CITY_EMAILS = {
    "Dehradun":"deoc.pgrc.ddn@gmail.com",
    "Bihar":"pgrodisaster@gmail.com",
    "Kerala": "krishidirector@gmail.com",
    "Meghalaya": "eo.sdma@gmail.com",
    "Assam": "sdma-assam@gov.in",  # :contentReference[oaicite:0]{index=0}
    "Delhi": "specialceo-dm@delhi.gov.in",  # :contentReference[oaicite:1]{index=1}
    "Nagaland": "sdma.nagaland@gmail.com",
    "Tamil Nadu": "com-ra@nic.in",
    "Local":"controlroom@ndma.gov.in" # send if states email is not persent
}



DONATION_WEBSITES = [
    {"name":"Red Cross", "url": "https://www.redcross.org/donate/donation.html", "emoji": "❤️", "color": "#c9302c"},
    {"name":"UNICEF Emergency Fund", "url": "https://www.unicef.org/take-action", "emoji": "💙", "color": "#1E90FF"},
    {"name":"GoFundMe Disaster Relief", "url": "https://www.gofundme.com/c/act/disaster-relief", "emoji": "🏥", "color": "#32CD32"},
    {"name":"Global Giving", "url": "https://www.globalgiving.org/disasters/", "emoji": "🌎", "color": "#FFA500"},
    {"name":"Direct Relief", "url": "https://www.directrelief.org/", "emoji": "🚑", "color": "#8B0000"},
    {"name":"Rapid Response(india)","url":"https://www.rapidresponse.org.in/donate.php","emoji":"🔴","color":"#E9967A"},
    {"name":"HelpAge India","url":"https://www.helpageindia.org/donate","emoji":"👴🏿","color":"#1A5276"},
    {"name":"Smile Foundation India","url":"https://donate.smilefoundationindia.org/donate-for-education#donateSection","emoji":"👴🏿","color":"#1A5276"}
]


FEATURES = """
# 🌟 **Features**
✅ <span style="color:red; font-size:18px;">**`<query>`**</span>: <span style="font-size:16px;">🤖 Normal Chat</span>  
✅ <span style="color:green; font-size:18px;">**`/<zipcode>`**</span>: <span style="font-size:16px;"> ⛈️ Get Disaster Analysis for a Specific Area</span>  
✅ <span style="color:green; font-size:18px;">**`/news`**</span>: <span style="font-size:16px;">📰 Get Current News</span>  
✅ <span style="color:green; font-size:18px;">**`/report <zipcode>`**</span>: <span style="font-size:16px;">🚨 Report a Disaster</span>  
✅ <span style="color:green; font-size:18px;">**`/pay`**</span>: <span style="font-size:16px;">💰 Help Disaster-Affected People</span>  
✅ <span style="color:green; font-size:18px;">**`/nearby`**</span>: <span style="font-size:16px;">📍 List hospital and websites.</span> 
"""