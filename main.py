import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd

# Load credentials and project ID from st.secrets
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
project_id = st.secrets["gcp_service_account"]["project_id"]

# Function to fetch data from BigQuery
def fetch_data(query: str) -> pd.DataFrame:
    client = bigquery.Client(credentials=credentials, project=project_id)
    query_job = client.query(query)  # Make a query request
    result = query_job.result()  # Wait for the query to finish
    return result.to_dataframe()

# Main app
def main():
    st.title("Streamlit GCP Data Loader")
    
    # Sample query (replace with your table and dataset)
    query = """
    SELECT *
    FROM `bizbuddydemo-v1.facebook_data.lundys_postdata`
    ORDER BY created_time DESC
    LIMIT 10
    """
    
    # Fetch the data
    st.write("Fetching data from BigQuery...")
    data = fetch_data(query)
    
    # Display the DataFrame
    st.write("Data fetched from BigQuery:")
    st.dataframe(data)

if __name__ == "__main__":
    main()
