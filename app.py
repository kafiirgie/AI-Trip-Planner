import os
import streamlit as st
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Google Calendar API Scopes
SCOPES = [
  "openid",
  "https://www.googleapis.com/auth/userinfo.email",
  "https://www.googleapis.com/auth/userinfo.profile",
  "https://www.googleapis.com/auth/calendar",
]


# Function to authenticate and get the credentials
def get_google_calendar_service(creds):
  try:
    service = build("calendar", "v3", credentials=creds)
    return service
  except HttpError as error:
    st.error(f"An error occurred: {error}")
    return None


# Authentication and session management
def authenticate_user():
  creds = None
  # Check if token.json exists to store user credentials
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  # If there are no valid credentials, prompt the user to log in
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
      creds = flow.run_local_server(port=8080)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  return creds

# Function to fetch user info
def get_user_info(creds):
  try:
    userinfo_endpoint = "https://www.googleapis.com/oauth2/v3/userinfo"
    response = requests.get(userinfo_endpoint, headers={"Authorization": f"Bearer {creds.token}"})
    userinfo = response.json()
    return userinfo
  except requests.RequestException as error:
    st.error(f"An error occurred while fetching user info: {error}")
    return None

# Main Streamlit app
def main():
  # Check if the user is authenticated
  # creds = authenticate_user()
  if 'service' not in st.session_state:
    st.session_state["service"] = None

  if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
  
  if st.session_state['authenticated']:
    # If authenticated, get the Google Calendar service
    creds = authenticate_user()
    service = get_google_calendar_service(creds)
    st.session_state["service"] = service

    # Fetch user info
    user_info = get_user_info(creds)
    user_name = user_info.get("name", "there")  # Default to "there" if the name is not available

    # Setup personalized welcome text
    welcome_text = f"Hi, {user_name}!"
    st.sidebar.markdown(
      f'<p style="font-size:18px; font-weight:600">{welcome_text}</p>',
      unsafe_allow_html=True
    )

    if st.sidebar.button('Log out'):
      os.remove("token.json")
      st.session_state['authenticated'] = False
      st.session_state['service'] = None
      st.rerun()

    # Setup sidebar menu
    create_trip = st.Page("view/create-trip.py", title="Create Trip")
    profile = st.Page("view/profile.py", title="Profile")
    nav = st.navigation([create_trip, profile])
    nav.run()
  
  else:
    st.title('📆✈️ Amon AI Trip Planner')
    # Hide sidebar
    blank =	st.Page("view/blank.py", title="AI Trip Planner")
    nav = st.navigation([blank], position="hidden")
    nav.run()
    # If not authenticated, show login button
    st.markdown(
      '<p style="font-size:24px">Welcome to Amon AI Trip Planner, discover your dream vacation with personalized itineraries tailored just for you.</p>',
      unsafe_allow_html=True
    )
    st.write('')
    if st.button("Login with Google"):
      st.session_state['authenticated'] = True
      st.rerun()  # Rerun the app after authentication


if __name__ == "__main__":
  main()
