Project Setup Documentation

Dependencies
To run this application, you’ll need to install several Python libraries. Use the following steps to set up your environment.

1. Create a Virtual Environment (Recommended)

It’s best to keep dependencies isolated by using a virtual environment. You can create one with the following command:

python3 -m venv consent_env
Activate the virtual environment:

On macOS/Linux:
source consent_env/bin/activate
On Windows:
consent_env\Scripts\activate
2. Install Required Packages

Install all necessary packages for the application by running:

pip install streamlit authlib requests sqlite3 matplotlib plotly
Explanation of Dependencies

Streamlit: The main framework for creating the web app.
Authlib: Used for OAuth2 authentication with Google.
Requests: Simplifies HTTP requests, used to retrieve Google’s OAuth2 endpoints.
SQLite3: Built into Python, used for managing the consent data.
Matplotlib & Plotly: Libraries for generating and displaying consent analytics charts.
Optional: Requirements File

If you want to create a requirements.txt file for easy dependency management, you can generate it with:

pip freeze > requirements.txt
To install from a requirements.txt file later, use:

pip install -r requirements.txt
Setting Up Google OAuth Authentication
1. Create a Google Cloud Project

Go to the Google Cloud Console.
Click on Select a project at the top and then New Project to create a new project.
Name your project and note the Project ID.
2. Set Up OAuth Consent Screen

In the Google Cloud Console, navigate to APIs & Services > OAuth consent screen.
Select the user type (External/Internal based on your needs) and fill out the required information.
Add scopes:
openid
profile
email
Save and continue.
3. Configure OAuth 2.0 Client Credentials

Go to APIs & Services > Credentials.
Click on Create Credentials and select OAuth client ID.
Choose Web application as the Application type.
In Authorized redirect URIs, add your app’s URI:
If running locally with Streamlit, use: http://localhost:8501
Click Create to generate the client ID and client secret.
4. Add OAuth Credentials to Your App

In your app's code (app.py), replace the placeholders in GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET with the values generated:

GOOGLE_CLIENT_ID = 'your-google-client-id'
GOOGLE_CLIENT_SECRET = 'your-google-client-secret'
5. Run the Application

Once you’ve set up Google OAuth, start the application with:

streamlit run app.py
Open http://localhost:8501 in your browser to access the app.

