import streamlit as st
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔑 Load API key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 📊 Connect Google Sheets
def connect_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(st.secrets["SHEET_ID"]).sheet1
    return sheet

st.title("🤖 Tyson Foods AI Helper")
st.write("This is a demo AI assistant to help with supply tracking, time logs, and incident reports.")

# Input
user_input = st.text_area("Ask me something about supply, time logs, or incidents:")

if st.button("Run AI"):
    if user_input:
        # Call OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are an AI assistant for Tyson Foods maintenance and supply tracking."},
                      {"role": "user", "content": user_input}]
        )
        answer = response["choices"][0]["message"]["content"]
        st.success(answer)

        # Save to Google Sheets
        try:
            sheet = connect_sheets()
            sheet.append_row([user_input, answer])
            st.info("Saved to log ✅")
        except Exception as e:
            st.error(f"Could not save to Google Sheets: {e}")
