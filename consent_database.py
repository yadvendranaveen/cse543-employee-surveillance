import sqlite3

# Helper function to connect to the database
def connect_db():
    return sqlite3.connect("consent_data.db")

# Function to initialize the database (create table if it doesn't exist)
def create_database():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS consent
                     (user_id TEXT PRIMARY KEY,
                      location_tracking INTEGER,
                      screen_time_tracking INTEGER,
                      activity_monitoring INTEGER)''')
        conn.commit()

# Helper function to fetch data from the database
def fetch_data(query, params=()):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute(query, params)
        return c.fetchall()

# Function to fetch consent data for a specific user
def get_consent_data(user_id):
    query = "SELECT * FROM consent WHERE user_id=?"
    data = fetch_data(query, (user_id,))
    return data[0] if data else None

# Function to update or insert user consent preferences
def update_consent(user_id, location, screen_time, activity):
    query = """INSERT OR REPLACE INTO consent 
               (user_id, location_tracking, screen_time_tracking, activity_monitoring) 
               VALUES (?, ?, ?, ?)"""
    with connect_db() as conn:
        c = conn.cursor()
        c.execute(query, (user_id, location, screen_time, activity))
        conn.commit()

# Function to fetch all consent data
def get_all_consent_data():
    query = "SELECT location_tracking, screen_time_tracking, activity_monitoring FROM consent"
    return fetch_data(query)

# Function to calculate consent percentages for each monitoring category
def calculate_consent_percentages():
    data = get_all_consent_data()
    if not data:
        return 0, 0, 0  # Return 0 if no data

    total_users = len(data)
    location_count = sum(row[0] for row in data)
    screen_time_count = sum(row[1] for row in data)
    activity_count = sum(row[2] for row in data)

    # Calculate percentages
    location_percent = (location_count / total_users) * 100
    screen_time_percent = (screen_time_count / total_users) * 100
    activity_percent = (activity_count / total_users) * 100

    return location_percent, screen_time_percent, activity_percent

# Initialize the database (run this once)
create_database()
