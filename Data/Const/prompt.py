
structured_prompt = {
    "task": "Analyze the provided input data and produce a structured JSON output strictly following the Output Format. Your analysis must be concise, accurate, and actionable, without assuming or inferring details not explicitly provided.",
    "instructions": [
        "1. Analyze the input data categories: weather, air quality, today’s disaster events, historical disasters data, and contact information.",
        "2. Summarize each data category into clear insights:",
        "   - **Weather Summary**: Describe the current weather with terms like hot, cold, humid, dry, or windy. Mention any visible weather phenomena like clouds or rain, focusing on the overall feel of the weather , without excessive numerical details.",
        "   - **Air Quality Summary**: Describe the air quality in simple terms, such as clean, pollutant levels, or hazy. Mention any noticeable effects like poor visibility or difficulty breathing, without excessive numerical details.",
        "   - **Today Disaster Summary**: Summarize only active and hazardous disasters, focusing on the type (e.g., flood, earthquake) and current situation.",
        "3. Use the provided current_date as a reference for determining the timeliness and relevance of events.",
        "4. Provide a list of actionable precautions based on the weather, air quality, or disaster data (e.g., staying indoors during poor air quality or preparing essentials for severe weather).",
        "6. If provided Disaster History indicates recurring patterns or risks, then generate a list of Historical Disaster Warnings.",
        "7. From the contact information, include only emergency numbers and websites that are directly relevant to addressing the current weather, air quality, or active disaster situations.Format them as JSON objects within arrays, as shown in the Output Format.",
        "8. Ensure your final output strictly adheres to the provided Output Format, without adding any extra fields or commentary.",
        "9. All output fields must be present. If any data is missing, incomplete, or provided as an empty list, use an empty string for summary fields and an empty list for list outputs.",
        "10. IMPORTANT,For the boolean fields in the situation_overview (is_severe_weather, is_pollution_high, today_disaster_active)",
    ],
    "input_format": {
        "current_date": "string",
        "weather": {
        "data": 
            {
            "lat": "float",  
            "lng": "float",  
            "timezone": "string", 
            "country_code": "string", 
            "time": "integer", 
            "apparentTemperature": "float", 
            "cloudCover": "float", 
            "dewPoint": "float", 
            "humidity": "integer", 
            "pressure": "float", 
            "precipIntensity": "float", 
            "temperature": "float", 
            "visibility": "float", 
            "windGust": "float", 
            "ozone": "float", 
            "uvIndex": "float", 
            "windSpeed": "float", 
            "windBearing": "float", 
            "icon": "string", 
            "summary": "string", 
            "updatedAt": "string"  
        }
    },
    "air_quality": {
        "stations": [
            {
                "CO": "float",  
                "NO2": "float",  
                "OZONE": "float",  
                "PM10": "float",  
                "PM25": "float",  
                "SO2": "float",  
                "city": "string",  
                "countryCode": "string",  
                "division": "string",  
                "lat": "float",  
                "lng": "float",  
                "placeName": "string",  
                "postalCode": "string",  
                "state": "string",  
                "updatedAt": "string",  
                "AQI": "integer",  
                "aqiInfo": {
                "pollutant": "string",  
                "concentration": "float",  
                "category": "string" }
            }
        ]
    },
    "today_disaster": {
        "result": [
            {
                "event_type": "string",  
                "event_name": "string",  
                "date": "string",  
                "lat": "float",  
                "lng": "float",  
                "continent": "string",  
                "created_time": "string",  
                "source_event_id": "string",  
                "event_id": "string"  
            }
        ]
    },
    "disaster_history": {
        "result": [
            {
                "event_type": "string",  
                "event_name": "string",  
                "date": "string",  
                "lat": "float",  
                "lng": "float",  
                "continent": "string",  
                "created_time": "string",  
                "source_event_id": "string",  
                "event_id": "string"  
            }
        ]
    },
    "contact_information": {
        "emergency_numbers": { 
            "police": "string", 
            "Ambulance":"string",
            "Fire Department":"string"
        },
        "websites": {  
            "Local Police": "string",
            "Red Cross":"string"
        }
    }},
    "output_format": {
    "current_date":"string",
    "city":"string",
    "lat":"float",
    "lng":"float",
    "report": {
        "weather_summary": "string", 
        "air_quality_summary": "string", 
        "today_disaster_summary": "string",
    },

    "precautions": [
        "string" 
    ],

    "Historical_Disaster_Warnings":[
        "string"
    ],
    
    "situation_overview": {
        "is_severe_weather": "boolean", 
        "is_pollution_high": "boolean", 
        "today_disaster_active": "boolean"
    },

    "contact_information": {
        "emergency_numbers": [
            {
                "type": "string",  
                "number": "string" 
            }
        ],
        "websites": [
            {
                "name": "string",
                "url": "string"
            }
        ]
    }},
}
