import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd

st.set_page_config(page_title="Social Overview", layout="wide")

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
    
    query = """
    SELECT *
    FROM `bizbuddydemo-v1.ig_data.lundys_postdata`
    ORDER BY created_time DESC
    LIMIT 10
    """
    
    # Fetch the data
    st.write("Fetching data from BigQuery...")
    data = fetch_data(query)

    # Get top 10 posts
    top_posts = data.sort_values(by='reach', ascending=False).head(10)
    
    st.markdown("""
    <style>
        .media {
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 10px;
            display: flex;
            justify-content: center;
        }
        .scorecards {
            margin-left: 20px;
            margin-right: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Define a consistent media width
    MEDIA_WIDTH = 500  # Adjust this value as needed
    
    # Iterate through the top posts and display them
    for index, row in top_posts.iterrows():
        # Create three columns for spacing and content
        spacer1, col1, col2, spacer2 = st.columns([0.5, 2, 1, 0.5])  # Adjust widths as needed
        
        with col1:
            # Display caption
            st.markdown(f"### {row['caption']}")
            
            # Display metrics in scorecards
            st.markdown("""
            <style>
            .scorecard {
                display: inline-block;
                padding: 10px 20px;
                margin: 5px;
                background-color: #f3f3f3;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
            }
            </style>
            """, unsafe_allow_html=True)
            
            metrics_html = f"""
            <div class="scorecard">Likes: {row['like_count']}</div>
            <div class="scorecard">Comments: {row['comments_count']}</div>
            <div class="scorecard">Reach: {row['reach']}</div>
            <div class="scorecard">Saves: {row['saved']}</div>
            """
            st.markdown(f'<div class="scorecards">{metrics_html}</div>', unsafe_allow_html=True)
        
        with col2:
            # Display media in a styled container
            st.markdown('<div class="media">', unsafe_allow_html=True)
            if row['media_type'] == 'IMAGE':
                st.image(row['source'], width=MEDIA_WIDTH)
            elif row['media_type'] == 'VIDEO':
                st.video(row['source'], start_time=0, format="video/mp4")
            st.markdown('</div>', unsafe_allow_html=True)
    
        st.markdown("---")  # Divider between posts

if __name__ == "__main__":
    main()
