import streamlit as st
from src.LLM.rag import main 
from src.LLM.run_gem import generate_report
from src.Parser.cache_report import update_report , add_new_report
from src.Parser.assemble_data import assemble , assemble_coordinates
from src.Parser.Compont import generate_html_report , generate_news_html , extract_pincode , pay_list_html
from src.api.climate_news import get_climate_news
from Data.Const.constants import FEATURES
from streamlit_js_eval import  get_geolocation
from src.Locations.loc_ip import get_location
from src.api.email_sender import  direct_email 

LOGO_PATH = "logo.png"

#st.title("Disaster Bot")

#st.set_page_config(initial_sidebar_state="expanded")
col1, col2 = st.columns([1,3])  # Adjust ratio as needed
# # Left-side top-aligned image
with col1:
    st.image(LOGO_PATH, use_container_width=True)
with col2:
    st.title(":blue[Disaster] :gray[Bot]")
    #st.markdown("<h2 style='text-align: center; color: gray;'>🌍 Disaster Management Bot</h2>", unsafe_allow_html=True)

    
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(204, 49, 49);
}
</style>""", unsafe_allow_html=True)

if st.button("Emergency."):
    loc = get_geolocation()
    # This will only work when not running locally.
    if loc:
        lat , lng = loc['latitude'] , loc['longitude']
    else:
        lat , lng  = get_location()
    coordinates = [lat , lng]
    # sample_data = assemble_coordinates(coordinates)
    # report = generate_report(sample_data)
    # direct_email(report)
    st.success("Emergency report sent!")
    st.session_state.messages.append({"role": "html", "content": f'<h3 style="color: green;"><b>Emergency report generated and sent!</b></h3>'})

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": FEATURES}]
    #st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"] , unsafe_allow_html=True)


# React to user input
if user_input := st.chat_input("Ask about disasters, weather, or precautions..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    user_input = user_input.strip()
    
    if user_input.startswith("/"):
        # Display the disaster report as HTML
        user_input = user_input.replace("/","")
        if user_input.isnumeric():
            zipcode = extract_pincode(user_input)
            zipcode = zipcode.strip()
            if zipcode:
                cached_report = update_report(zipcode)
                if cached_report:
                    html_report = generate_html_report(cached_report)
                else:
                    sample_data = assemble(zipcode)
                    report = generate_report(sample_data)
                    add_new_report(zipcode , report)
                    html_report = generate_html_report(report)
                st.components.v1.html(html_report, height=700, scrolling=True) 
            else:
                st.chat_message("assistant").markdown(":red[**Invalid Zipcode. Please enter a correct one.**]")
                    
        elif user_input == "news":
            data = get_climate_news()
            news_data = generate_news_html(data)
            st.components.v1.html(news_data, height=700, scrolling=True)
            
        elif user_input.split()[0].strip() == "report":
            # send report to the goverment agency.
            reporting_zip = user_input.split()
            if len(reporting_zip) == 2:
                zip_code = reporting_zip[1]
            st.chat_message("assistant").markdown(":green[***The Disaster is reported to authorities...***]")
        
        elif user_input == "nearby":
            st.chat_message("assistant").markdown(":green[***Trying to get detils of nearby hospitals....***]")
            
        elif user_input == "pay":
            payment_listing = pay_list_html()
            st.components.v1.html(payment_listing, height=700, scrolling=True)
        
        else:
            st.chat_message("assistant").markdown(":red[**Invalid command. Use `/news` or a valid `/zipcode` , `/report`.**]")

    else:
        response = main(user_input)
        bot_response = f"Echo: {response}"
        st.chat_message("assistant").markdown(f"**{bot_response}**")
        st.session_state.messages.append({"role": "assistant", "content": response})


