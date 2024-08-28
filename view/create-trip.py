import os
import json
from datetime import datetime
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from constants.json_format import json_format
from utils.show_result import display_hotels, display_itinerary

# Load environment variables
load_dotenv()

# Configure the Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

st.title("🏝️ Create Trip")

# Destination input
destination = st.text_input("What is your destination of choice?")

# Date input
trip_date = st.date_input(
    "When will you be going on your trip?",
    value=datetime.today(),
    min_value=datetime.today(),
    format="MM/DD/YYYY"
)

# Number of days input
days = st.number_input("How many days are you planning your trip?", min_value=1, max_value=5, value=1)

# Budget selection
budget = st.radio(
	"What is Your Budget?",
	options=["Low (0 - 1000 USD)", "Medium (1000 - 2500 USD)", "High (2500+ USD)"],
	index=0
)

is_preference = st.radio(
	"Do you want to add Travel Preference?",
	options=["No Preference", "Add Preference"],
	index=0
)

preference = None
if is_preference == "Add Preference":
	preference = st.multiselect(
    "What is Your Travel Preference?",
    options=["Nature", "Culture", "Adventure", "Health and Wellness", "Culinary", "Art and Architecture", "Technology and Innovation"],
	)
	preference = ", ".join(preference)

companions = st.radio(
	"Who do you plan on traveling with on your next adventure?",
	options=["Solo", "Couple", "Family", "Friends"],
	index=0
)

if companions == "Family" or companions == "Friends":
	num_persons = st.number_input("How many persons are you traveling with?", min_value=2, max_value=20, value=2)
elif companions == "Solo":
	num_persons = st.number_input("How many persons are you traveling with?", value=1, disabled=True)
elif companions == "Couple":
	num_persons = st.number_input("How many persons are you traveling with?", value=2, disabled=True)

# Initialize session state if not already present
if 'response' not in st.session_state:
    st.session_state['response'] = None

# Submit button inside the form
with st.spinner("Processing..."):
	try:
		with st.form(key="trip_planner_form"):
			submit = st.form_submit_button(label="Submit")

			if submit:
				if destination:
					# st.write("Prompt:")
					prompt = f'''
						Generate a travel plan for the location {destination} for {days} days with {companions} ({num_persons} people) and a budget of {budget}. Provide a list of hotel options with the following details: Hotel Name, Hotel Address, Price Range, Hotel Image URL, Rating, and Descriptions.
						Additionally, suggest an itinerary based on the preferences: {preference}, start from {trip_date} (MM/DD/YYYY), including the following details for each place: Place Name, Place Descriptions, Place Addresss, Place Image URL, Rating, Ticket Range Pricing, Distance to each location, and Travel Time to each location.
						The itinerary should cover {days} days with a daily plan, including the best time to visit each location, ordered by time to visit. 
						For Best Time to Visit, Specify the time range when each place should be visited. For example, "10 AM - 12 PM".
						For Distance to Each Location, Provide the distance from the previous location to the current location in a clear unit (e.g., "1.5 km").
						For Travel Time to Each Location, Specify the estimated travel time between locations in a clear format (e.g., "15 minutes").
						For Hotel and Ticket Price, specify the currency too.
						Provide the data in the following JSON format: {json_format}
					'''
					# st.write(prompt)

					# Send the prompt to the Gemini API
					model = genai.GenerativeModel(
						model_name="gemini-1.5-flash",
						generation_config={
							"temperature": 1,
							"top_p": 0.95,
							"top_k": 64,
							"max_output_tokens": 8192,
							"response_mime_type": "application/json",
						},
					)

					chat_session = model.start_chat(
						history=[
							{
								"role": "user",
								"parts": [prompt],
							}
						]
					)

					response = chat_session.send_message(prompt)
					# Display the response
					st.write("Generated Travel Plan:")
					st.session_state['response'] = response.text
					st.json(st.session_state['response'])
				else:
					st.write("Please input the destination")
		
		if st.button('Clear'):
			st.session_state['response'] = None
			st.rerun()

		if st.session_state['response']:
			data = json.loads(st.session_state['response'])
			display_hotels(data['hotels'])
			display_itinerary(data['itinerary'])

	except Exception as e:
		st.write('Oops, something went wrong')
		st.write(e)

