import streamlit as st
from src.LLM.rag import main 
from src.LLM.run_gem import generate_report
from src.Parser.cache_report import update_report, add_new_report
from src.Parser.assemble_data import assemble, assemble_coordinates
from src.Parser.Compont import generate_html_report, generate_news_html, extract_pincode, pay_list_html
from src.api.climate_news import get_climate_news
from streamlit_js_eval import get_geolocation
from src.Locations.loc_ip import get_location
from src.api.email_sender import direct_email
from src.api.nearby_search import get_nearby_healthcare
from src.Parser.Compont import generate_nearby_html
from src.Conversations.text_speech import speak
from src.Conversations.voice_text import voice_to_text
import tempfile
import os
st.set_page_config(layout="wide")


st.sidebar.image("logo.png", use_container_width=True)
st.markdown("<h1 style='text-align: center; color: gray;'>🌍 Disaster Management System</h1>", unsafe_allow_html=True)


st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #FF6F61;
    color: black;
    font-size: 14px;
    font-weight: bold;
    text-transform: uppercase;
    border-radius: 20px;
    padding: 5px 10px;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
    text-align: center;
}
div.stButton > button:first-child:hover {
    background-color: green;
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}
div.stButton > button:first-child:focus {
    outline: none;
    box-shadow: 0 0 0 4px rgba(255, 111, 97, 0.5);
}
div.stButton > button[disabled] {
    background-color: #ddd;
    cursor: not-allowed;
    opacity: 0.6;
    box-shadow: none;
}

/* Styling the checkbox */
div[data-testid="stCheckbox"] {
    display: flex;
    align-items: center;
    font-size: 14px;
    font-weight: bold;
    justify-content: center;
    background-color: #4CAF50;
    border-radius: 50px;
    padding: 6px 16px;
    transition: 0.3s;
    cursor: pointer;
    width: fit-content;
    margin: auto;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
div[data-testid="stCheckbox"]:hover {
    background-color: red;
}
div[data-testid="stCheckbox"] > label {
    color: black !important;
    font-weight: bold;
    font-size: 15px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "audio_input_key_counter" not in st.session_state:
    st.session_state.audio_input_key_counter = 0



def add_message(role, content):
    """Prevent duplicate messages before adding to session state."""
    if not any(msg["content"] == content and msg["role"] == role for msg in st.session_state.messages):
        st.session_state.messages.append({"role": role, "content": content})
        

            
            
if st.sidebar.checkbox("🚨 Emergency"):
    loc = get_geolocation()
    if loc:
        lat, lng = loc["coords"]['latitude'], loc["coords"]['longitude']
        coordinates = [lat, lng]
        sample_data = assemble_coordinates(coordinates)
        report = generate_report(sample_data)
        direct_email(report)
        st.success("Emergency report sent!")
        st.session_state.messages.append({"role": "html", "content": '<p style="color: green;"><b>Emergency report generated and sent!</b></p>'})

if st.sidebar.button("📰 News"):
    data = get_climate_news()
    news_data = generate_news_html(data)
    st.session_state.messages.append({"role": "html", "content": news_data})

if st.sidebar.button("🏥 NGO List"):
    payment_listing = pay_list_html()
    st.session_state.messages.append({"role": "html", "content": payment_listing})

if st.sidebar.checkbox("📍Nearby"):
    loc = get_geolocation()
    if loc:
        lat, lng = loc["coords"]['latitude'], loc["coords"]['longitude']
        adress_details = get_nearby_healthcare(lat, lng)
        if adress_details:
            nearby_html = generate_nearby_html(adress_details)
            st.session_state.messages.append({"role": "html", "content": nearby_html})
        else:
            st.session_state.messages.append({"role": "html", "content": '<p style="color: red;"><b>Error occurred.!</b></p>'})

zip_code = st.sidebar.text_input(" ", placeholder="PINCODE", max_chars=6, help="Get the detailed disaster report")
if st.sidebar.button("📜 Report"):
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
            st.session_state.messages.append({"role": "html", "content": '<p style="color: red;"><b>Invalid Zipcode. Please enter a correct one.</b></p>'})

zip_code_report = st.sidebar.text_input(" ", placeholder="PINCODE ", max_chars=6, help="Send Detailed report to authority.")
if st.sidebar.button("🚓 Reporting"):
    if zip_code_report:
        st.session_state.messages.append({"role": "html", "content": f'<p style="color: green;"><b>Disaster reported for ZIP Code: {zip_code_report}</b></p>'})



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "html":
            st.components.v1.html(message["content"], height=700, scrolling=True)
            st.session_state.messages = [msg for msg in st.session_state.messages if msg["role"] != "html"]
        else:
            st.markdown(message["content"], unsafe_allow_html=True)
            

audio_input_key = f"audio_input_key_{st.session_state.audio_input_key_counter}"
audio_value = st.sidebar.audio_input(label="Voice", key=audio_input_key)
on = st.sidebar.toggle("🗣️ Voice Reply")
if audio_value:
    print("recorded value")
    
    with tempfile.TemporaryFile(suffix=".wav") as temp_audio:
        temp_audio.write(audio_value.getvalue())
        temp_audio.seek(0)  # Move to the beginning of the file
        
        transcribed_text = voice_to_text(temp_audio)
        transcribed_text = transcribed_text +". tell me in two sentence Maximum."
        if transcribed_text:
            st.chat_message("user").markdown(transcribed_text)
            #st.session_state.messages.append({"role": "user", "content": transcribed_text})
            add_message("user",transcribed_text)
            response = main(transcribed_text)
            bot_response = f"**{response}**"
            st.chat_message("assistant").markdown(bot_response)
            
            if on:
                speak(bot_response.replace("*",""))
            
            #st.session_state.messages.append({"role": "assistant", "content": response})
            add_message("assistant",bot_response)
            del st.session_state[audio_input_key]
            st.session_state.audio_input_key_counter += 1


if user_input := st.chat_input("Ask about disasters, weather, or precautions..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = main(user_input)
    bot_response = f"**{response}**"
    st.chat_message("assistant").markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": response})

