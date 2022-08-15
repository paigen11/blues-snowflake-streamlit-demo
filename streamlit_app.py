import streamlit as st
import pandas as pd
import snowflake.connector

# Initialize connection.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

# Perform query.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

"""
# Asset Tracker Data

This page shows asset tracker environment readings and device location from a Blues
Wireless Notecard.
"""

"""
### Options
"""
num_rows = st.slider('Rows to fetch?', 10, 500, 100)
sort = st.selectbox('Sort?',('asc', 'desc'))
show_table_data = st.checkbox('Show table data?', True)
show_charts = st.checkbox('Show charts?', True)
show_map = st.checkbox('Show map?', False)

location_rows = run_query(f'SELECT * from tracker_vw ORDER BY created {sort} LIMIT {num_rows};')
location_data = pd.DataFrame(location_rows, columns=("ID", "Device", "Created", "lat", "lon", "Location", "Location Type", "Timezone", "Country", "Temp", "Motion", "Voltage"))

if show_table_data:
  """
  ## Notecard `track.qo` Events
  """

  # Flip the column order to show voltage and temp first. If you don't
  # want to do this, change the line below to location_data.
  location_data[location_data.columns[::-1]]

if show_charts:
  """
  ### Environment Chart
  """

  location_group = location_data[["Temp", "Motion"]]
  st.line_chart(location_group)

if show_map:
  """
  ### Tracker Map
  """

  tracker_locations = location_data[["lat", "lon"]]

  st.map(tracker_locations)