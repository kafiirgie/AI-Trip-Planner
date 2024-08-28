import streamlit as st
from googleapiclient.discovery import build
import datetime
import pytz

# Time zone for GMT+7
TIMEZONE = pytz.timezone('Asia/Bangkok')

# Display hotels
def display_hotels(data):
  st.divider()
  st.header('🏩 Hotels')
  for hotel in data:
    st.markdown(f'### {hotel["Hotel Name"]}')
    with st.container():
      col1, col2 = st.columns([2, 1])
      with col1:
        # st.image(hotel['Hotel Image URL'], use_column_width=True)
        st.write(hotel['Descriptions'])
        st.write(f'📍 {hotel["Hotel Address"]}')
      with col2: 
        st.write(f'⭐ {hotel["Rating"]}/5')
        st.write(f'💵 {hotel["Price"]}')
        st.button('Book Now', key=hotel['Hotel Name'])

    st.divider()

# Display itinerary
def display_itinerary(data):
  st.divider()
  st.header('📜 Itinerary')

  events_list = [] # To store event to create in calendar

  for day in data:
    # Convert day["Date"] from MM/DD/YYYY to a datetime object
    day_date = datetime.datetime.strptime(day["Date"], "%m/%d/%Y").date()

    st.subheader(f'Day {day["Day"]}')
    for place in day['Places']:
      st.markdown(f'##### {place["Place Name"]}')
      with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
          # st.image(place['Place Image URL'], use_column_width=True)
          st.write(place['Descriptions'])
          st.write(f'📍 {place["Place Address"]}')
          st.write(f'⌚ {place["Best Time to Visit"]}')
        with col2:
          st.write(f'⭐ {place["Rating"]}/5')
          st.write(f'💵 {place["Ticket Pricing"]}')
          st.write(f'🚗 {place["Distance to each location"]} | {place["Travel Time to each location"]}')
          
          # Parse time strings and create datetime objects
          start_time_str = place["Start Time"]  # Format: "HH:MM:SS"
          end_time_str = place["End Time"]  # Format: "HH:MM:SS"
          
          # Combine date with start and end times
          start_datetime = datetime.datetime.combine(day_date, datetime.datetime.strptime(start_time_str, "%H:%M:%S").time())
          end_datetime = datetime.datetime.combine(day_date, datetime.datetime.strptime(end_time_str, "%H:%M:%S").time())
          
          # Localize to GMT+7 time zone
          start_datetime = TIMEZONE.localize(start_datetime)
          end_datetime = TIMEZONE.localize(end_datetime)
          
          # Convert to ISO format with the time zone
          start_time_iso = start_datetime.isoformat()
          end_time_iso = end_datetime.isoformat()

          event = {
            'summary': place["Place Name"],
            'location': place["Place Address"],
            'description': f"Holiday Day-{day["Day"]}",
            'start': {
              'dateTime': start_time_iso,
              'timeZone': 'UTC',
            },
            'end': {
              'dateTime': end_time_iso,
              'timeZone': 'UTC',
            },
            'reminders': {
              'useDefault': False,
              'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
              ],
            },
          }
          events_list.append(event)

          # Add to Calendar button
          if st.button('Add to Calendar', key=f'{day["Day"]}_{place["Place Name"]}'):
            service = st.session_state["service"]
            created_event = service.events().insert(calendarId='primary', body=event).execute()
            st.write(f'Event added! [View it on Google Calendar]({created_event.get("htmlLink")})')
      st.divider()

  if st.button('Add All to Calendar'):
    i = 0
    for event in events_list:
      service = st.session_state["service"]
      created_event = service.events().insert(calendarId='primary', body=event).execute()
      i += 1
    st.write(f'{i} Events added! [View it on Google Calendar]({created_event.get("htmlLink")})')