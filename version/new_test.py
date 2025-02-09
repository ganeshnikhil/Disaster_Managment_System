import streamlit as st
from src.LLM.rag import main 
from src.LLM.run_gem import generate_report
from src.Parser.cache_report import update_report, add_new_report
from src.Parser.assemble_data import assemble, assemble_coordinates
from src.Parser.Compont import generate_html_report, generate_news_html, extract_pincode, pay_list_html
from src.api.climate_news import get_climate_news
from Data.Const.constants import FEATURES
from streamlit_js_eval import get_geolocation
from src.Locations.loc_ip import get_location
from src.api.email_sender import direct_email
from src.api.nearby_search import get_nearby_healthcare
from src.Parser.Compont import generate_nearby_html

st.set_page_config(layout="wide")

#st.set_page_config(initial_sidebar_state="expanded")
col1, col2 = st.columns([1,7])  # Adjust ratio as needed
# # Left-side top-aligned image
with col1:
    st.image("logo.png", use_container_width=True)
with col2:
    st.markdown("<h2 style='text-align: center; color: gray;'>🌍 Disaster Management Bot</h2>", unsafe_allow_html=True)

#st.title(":blue[Disaster] :gray[Bot]")
st.markdown("""
<style>
/* Styling the smaller button */
div.stButton > button:first-child {
    background-color: #FF6F61;  /* Soft Coral background */
    color: black;  /* White text */
    font-size: 14px;  /* Smaller font size */
    font-weight: bold;  /* Semi-bold text */
    text-transform: uppercase;  /* Uppercase text for emphasis */
    border-radius: 20px;  /* Rounded corners */
    padding: 5px 10px;  /* Reduced padding */
    border: none;  /* No border */
    cursor: pointer;  /* Cursor changes to pointer on hover */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  /* Soft shadow */
    transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;  /* Smooth transitions */
    text-align: center;  /* Center text */
}

/* Hover effect */
div.stButton > button:first-child:hover {
    background-color: green;  /* Darker coral on hover */
    transform: translateY(-2px);  /* Slightly lift button */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);  /* Larger shadow on hover */
}

/* Focus effect when the button is clicked/focused */
div.stButton > button:first-child:focus {
    outline: none;  /* Remove the default outline */
    box-shadow: 0 0 0 4px rgba(255, 111, 97, 0.5);  /* Subtle glowing border */
}

/* Disabled button state */
div.stButton > button[disabled] {
    background-color: #ddd;  /* Grey background for disabled button */
    cursor: not-allowed;  /* Disable pointer cursor */
    opacity: 0.6;  /* Semi-transparent */
    box-shadow: none;  /* No shadow for disabled state */
}
</style>
""", unsafe_allow_html=True)

# Apply CSS for a compact and rounded checkbox style
st.markdown(
    """
    <style>
    /* Style the checkbox container */
    div[data-testid="stCheckbox"] {
        display: flex;
        align-items: center;
        font-size: 14px;  /* Smaller font size */
        font-weight: bold;  /* Semi-bold text */
        justify-content: center;
        background-color: #4CAF50;
        border-radius: 50px;  /* Circular edges */
        padding: 6px 16px;
        transition: 0.3s;
        cursor: pointer;
        width: fit-content;
        margin: auto;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Change background color when hovered */
    div[data-testid="stCheckbox"]:hover {
        background-color: red;
    }

    /* Change text color */
    div[data-testid="stCheckbox"] > label {
        color: white !important;
        font-weight: bold;
        font-size: 15px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# {'coords': {'accuracy': 35, 'altitude': None, 'altitudeAccuracy': None, 'heading': None, 'latitude': 30.412764052531447, 'longitude': 77.96850951931819, 'speed': None}, 'timestamp': 760673780890}
col1, col2, col3, col4, col5 , col6 = st.columns(6)

if "messages" not in st.session_state:
    #st.session_state.messages = [{"role": "assistant", "content": FEATURES}]
    st.session_state.messages = []


    
with col1:
    if st.checkbox("🚨 Emergency"):
        # when run on http serve than works.
        loc = get_geolocation()
        print(loc)
        if loc:
            lat, lng = loc["coords"]['latitude'], loc["coords"]['longitude']
            print(lat , lng)
        else:
            lat, lng = get_location()
        coordinates = [lat, lng]
        print(coordinates)
        sample_data = assemble_coordinates(coordinates)
        report = generate_report(sample_data)
        direct_email(report)
        st.success("Emergency report sent!")
        st.session_state.messages.append({"role": "html", "content": f'<p style="color: green;"><b>Emergency report generated and sent!</b></p>'})

with col2:
    if st.button("📰 News"):
        data = get_climate_news()
        news_data = generate_news_html(data)
        st.session_state.messages.append({"role": "html", "content": news_data})

with col3:
    if st.button("🏥 NGO List"):
        payment_listing = pay_list_html()
        st.session_state.messages.append({"role": "html", "content": payment_listing})
        
with col4:
    if st.checkbox("📍Near by"):
        loc = get_geolocation()
        if loc:
            lat, lng = loc["coords"]['latitude'], loc["coords"]['longitude']
        else:
            lat, lng = get_location()
        
        adress_details = get_nearby_healthcare(lat , lng)
        if adress_details:
            nearby_html = generate_nearby_html(adress_details)
            st.session_state.messages.append({"role": "html", "content": nearby_html})
        else:
            st.session_state.messages.append({"role": "html", "content": f'<p style="color: red;"><b>Error occured.!</b></p>'})
            
with col5:
    zip_code = st.text_input(" ",placeholder="PINCODE",max_chars=6, help="get the detailed disaster report")
    if st.button("📜 Report"):
        if zip_code:
            zipcode = extract_pincode(zip_code)
            if zipcode:
                cached_report = update_report(zipcode)
                if cached_report:
                    html_report = generate_html_report(cached_report)
                else:
                    sample_data = assemble(zipcode)
                    report = generate_report(sample_data)
                    add_new_report(zipcode, report)
                    html_report = generate_html_report(report)
                st.session_state.messages.append({"role": "html", "content": html_report})
            else:
                #st.chat_message("assistant").markdown(":red[**Invalid Zipcode. Please enter a correct one.**]")
                st.session_state.messages.append({"role": "html", "content": f'<p style="color: red;"><b>Invalid Zipcode. Please enter a correct one.</b></p>'})
                
with col6:
    zip_code_report = st.text_input(" ",placeholder="PINCODE ",max_chars=6,help="send Detailed report to authority.")
    if st.button("🚓 Reporting"):
        if zip_code_report:
            #st.chat_message("assistant").markdown(":green[***The Disaster is reported to authorities...***]")
            st.session_state.messages.append({"role": "html", "content": f'<p style="color: green;"><b>Disaster reported for ZIP Code: {zip_code_report}</b></p>'})
            

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "html":
            st.components.v1.html(message["content"], height=700, scrolling=True)
            st.session_state.messages = [msg for msg in st.session_state.messages if msg["role"] != "html"]
        else:
            st.markdown(message["content"], unsafe_allow_html=True)

if user_input := st.chat_input("Ask about disasters, weather, or precautions..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = main(user_input)
    bot_response = f"**{response}**"
    st.chat_message("assistant").markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": response})
