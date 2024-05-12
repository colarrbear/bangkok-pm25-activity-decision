import pandas as pd
import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('dbja.db')

# Retrieve questionnaire responses from the database
questionnaire_df = pd.read_sql_query("SELECT * FROM questionnaire_responses", conn)

# Construct a query to retrieve PM2.5 data based on geographical and temporal attributes
pm25_query = """
    SELECT timestamp, location, pm25_level
    FROM pm25_data
    WHERE location = ? AND timestamp BETWEEN ? AND ?
"""

# Iterate over questionnaire responses and query PM2.5 data for each response
matched_data = []
for index, response in questionnaire_df.iterrows():
    location = response['location']
    timestamp = response['timestamp']
    start_time = timestamp - pd.Timedelta(hours=1)  # Adjust as needed
    end_time = timestamp + pd.Timedelta(hours=1)    # Adjust as needed

    # Execute the query to retrieve PM2.5 data
    pm25_df = pd.read_sql_query(pm25_query, conn, params=(location, start_time, end_time))
    matched_data.append(pm25_df)

# Concatenate the matched PM2.5 dataframes
matched_pm25_data = pd.concat(matched_data)

# Merge or join the questionnaire responses with the matched PM2.5 data
merged_data = pd.merge(questionnaire_df, matched_pm25_data, on=['timestamp', 'location'], how='inner')

# Close the database connection
conn.close()
