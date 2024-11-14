import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import requests
import matplotlib.pyplot as plt
import plotly.express as px
from consent_database import get_consent_data, update_consent, calculate_consent_percentages

# Google OAuth credentials
GOOGLE_CLIENT_ID = 'your-google-client-id'
GOOGLE_CLIENT_SECRET = 'your-google-client-secret'
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Function to get Google OAuth2 session and endpoints
def get_oauth2_session():
    response = requests.get(GOOGLE_DISCOVERY_URL)
    oauth2_info = response.json()
    authorization_url = oauth2_info['authorization_endpoint']
    token_url = oauth2_info['token_endpoint']
    client = OAuth2Session(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, scope='openid profile email')
    return client, authorization_url, token_url

# Function to generate the login URL
def google_login():
    client, authorization_url, token_url = get_oauth2_session()
    redirect_uri = 'http://localhost:8501'  # The URL for redirect after Google login
    authorization_url, state = client.create_authorization_url(authorization_url, redirect_uri=redirect_uri)
    return authorization_url

# Function to display current consent preferences
def display_preferences(location, screen_time, activity):
    st.subheader("Your Current Consent Preferences")
    st.write(f"Location Tracking: {'Enabled' if location else 'Disabled'}")
    st.write(f"Screen Time Tracking: {'Enabled' if screen_time else 'Disabled'}")
    st.write(f"Activity Monitoring: {'Enabled' if activity else 'Disabled'}")

# Function to display consent analytics
def display_analytics():
    location_percent, screen_time_percent, activity_percent = calculate_consent_percentages()
    st.header("Consent Analytics")
    st.write("**Percentage of Employees Opted into Monitoring Categories:**")
    st.write(f"Location Tracking: {location_percent:.2f}%")
    st.write(f"Screen Time Tracking: {screen_time_percent:.2f}%")
    st.write(f"Activity Monitoring: {activity_percent:.2f}%")
    
    # Bar Chart
    st.subheader("Consent Percentage Bar Chart")
    categories = ['Location Tracking', 'Screen Time Tracking', 'Activity Monitoring']
    percentages = [location_percent, screen_time_percent, activity_percent]

    fig, ax = plt.subplots()
    ax.bar(categories, percentages, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    ax.set_xlabel('Monitoring Categories')
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Employee Consent for Monitoring Categories')
    st.pyplot(fig)

    # Pie Chart
    st.subheader("Consent Distribution (Pie Chart)")
    consent_data = [location_percent, screen_time_percent, activity_percent]
    labels = ['Location Tracking', 'Screen Time Tracking', 'Activity Monitoring']

    fig = px.pie(names=labels, values=consent_data, title="Consent Distribution by Category")
    st.plotly_chart(fig)

# Main Streamlit App
st.title("Consent-Based Surveillance Dashboard")
st.write("Manage your consent for data monitoring in the workplace.")

# Choose to login or continue as guest
mode = st.radio("Choose an option:", ["Login with Google", "Continue as Guest"])

if mode == "Login with Google":
    # Handle Google login
    if 'google_user_info' not in st.session_state:
        login_url = google_login()
        st.markdown(f"[Login with Google]({login_url})")
    else:
        user_info = st.session_state['google_user_info']
        user_id = user_info['id']
        st.write(f"Welcome {user_info['name']}!")

        # Fetch current consent data
        consent_data = get_consent_data(user_id)
        location_tracking, screen_time_tracking, activity_monitoring = (
            consent_data[1:] if consent_data else (0, 0, 0)
        )

        # Display monitoring categories with checkboxes
        st.header("Monitoring Categories")
        location = st.checkbox("Location Tracking", value=bool(location_tracking))
        screen_time = st.checkbox("Screen Time Tracking", value=bool(screen_time_tracking))
        activity = st.checkbox("Activity Monitoring", value=bool(activity_monitoring))

        # Save consent choices
        if st.button("Save Preferences"):
            update_consent(user_id, int(location), int(screen_time), int(activity))
            st.success("Your preferences have been saved.")
            st.rerun()  # Trigger app rerun to reflect changes
  # Trigger app rerun to reflect changes

        # Display current consent preferences
        display_preferences(location, screen_time, activity)

elif mode == "Continue as Guest":
    # Allow preference selection without login
    st.header("Monitoring Categories (Guest)")

    # Use a common 'guest_user_id' for all guest preferences
    guest_user_id = 'guest_user_id'  # A fixed ID for all guest users
    consent_data = get_consent_data(guest_user_id)
    location_tracking, screen_time_tracking, activity_monitoring = (
        consent_data[1:] if consent_data else (0, 0, 0)
    )

    # Checkboxes to update preferences
    location = st.checkbox("Location Tracking", value=bool(location_tracking))
    screen_time = st.checkbox("Screen Time Tracking", value=bool(screen_time_tracking))
    activity = st.checkbox("Activity Monitoring", value=bool(activity_monitoring))

    # Save guest preferences (update same row in database)
    if st.button("Save Preferences"):
        update_consent(guest_user_id, int(location), int(screen_time), int(activity))
        st.success("Your preferences have been saved as a guest.")
        st.rerun()  # Trigger app rerun to reflect changes

    # Display current consent preferences
    display_preferences(location, screen_time, activity)

# Display consent analytics
display_analytics()
