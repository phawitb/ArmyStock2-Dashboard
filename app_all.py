import requests
import pandas as pd
import streamlit as st

# Streamlit page configuration and styling
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                .reportview-container {
		    margin-top: -2em;
		}
		#MainMenu {visibility: hidden;}
		.stDeployButton {display:none;}
		footer {visibility: hidden;}
		#stDecoration {display:none;}
        </style>
        """, unsafe_allow_html=True)

# Function to check if a URL is online
# def check_url(url):
#     try:
#         response = requests.get(url)
#         return True
#     except:
#         return False

def check_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # return "The ngrok tunnel is working."
            return True
        elif 'ERR_NGROK_3200' in response.text:
            # return "Ngrok tunnel not found (ERR_NGROK_3200)."
            return False
        else:
            # return f"The URL returned status code {response.status_code}."
            return False
    except requests.exceptions.RequestException as e:
        # return f"An error occurred: {e}"
        return False


# Function to fetch and return DataFrame from the API
def get_all_df():
    url = 'https://script.google.com/macros/s/AKfycbzuT9-Ubg4hK999BVXVenxvnSMcUDtLhYUJO17gGHRCONrx12gOc5ovfrGLUh711Kyq/exec'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        df = pd.DataFrame(data)
        return df
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# Fetch and sort data
df = get_all_df()
df = df.sort_values(by='timestamp', ascending=False)

# Check online status for each URL
onlines = []
urls = []
for index, row in df.iterrows():
    sta = check_url(row['url'])
    onlines.append(sta)

    u = None
    if row['url']:
        u = row['url'] + '/history'
    urls.append(u)
df['online'] = onlines
df['url'] = urls

# Sort DataFrame based on online status
df = df.sort_values(by='online', ascending=False)

# Header
st.header('ระบบบริหารจัดการคลังอาวุธ')

# Function to highlight rows based on the 'online' status
def highlight_online(row):
    color = 'background-color: #acffb7;' if row.online else 'background-color: #f8c8c8;'
    return [color] * len(row)

# Apply the row coloring
styled_df = df.style.apply(highlight_online, axis=1)

# Display the DataFrame with conditional formatting
# st.dataframe(styled_df)

st.dataframe(
    styled_df,
    column_config={
        "url": st.column_config.LinkColumn("url"),
        "sheet_url": st.column_config.LinkColumn("sheet_url")
    },
    hide_index=True,
)



