import streamlit as st
import google.genai as genai
import requests
import json

# --- 1. SETUP ---
# Ensure these are in your .streamlit/secrets.toml
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
N8N_WEBHOOK_URL = st.secrets["N8N_WEBHOOK_URL"]

# Initialize the Client
client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="Gemma Geospatial Orchestrator", layout="wide")
st.title("🌍 Gemma-Powered Geospatial Orchestrator")

# --- 2. STAGE 1: UPLOAD ---
st.header("Step 1: Document Upload")
uploaded_file = st.file_uploader("Upload Geospatial Report (.txt)", type=["txt"])

if uploaded_file:
    raw_text = uploaded_file.read().decode("utf-8")
    st.success("Document Loaded Successfully!")

    # --- 3. STAGE 2: GEMMA EXTRACTION ---
    st.header("Step 2: Gemma Data Extraction")
    user_query = st.text_input("Analysis Query:", value="Analyze flood risk and site safety.")

    if st.button("Run Gemma Analysis"):
        with st.spinner("Gemma is extracting data..."):
            prompt = f"""
            You are a specialized geospatial AI. 
            Analyze this report: {raw_text}
            Based on this query: {user_query}
            
            Return ONLY a valid JSON object with these keys:
            "project_name", "risk_level" (must be 'High' or 'Low'), "flood_zone", "summary".
            """
            
            try:
                # Calling the Gemma 2 model via the SDK
                response = client.models.generate_content(
                    model="gemma-4-31b-it", 
                    contents=prompt
                )
                
                # Parse JSON and handle Markdown formatting
                clean_json = response.text.replace("```json", "").replace("```", "").strip()
                extracted_data = json.loads(clean_json)
                
                # PERSISTENCE: Save to Session State for Step 3
                st.session_state['extracted_data'] = extracted_data
                st.session_state['raw_text'] = raw_text
                
                st.subheader("Gemma Extraction Results")
                st.table([extracted_data])
                
            except Exception as e:
                st.error(f"Gemma Error: {e}")

    # --- 4. STAGE 3: AUTOMATION TRIGGER ---
    if 'extracted_data' in st.session_state:
        st.divider()
        st.header("Step 3: Trigger n8n Automation")
        
        email = st.text_input("Alert Recipient Email:", value="user@example.com")
        
        if st.button("Send Alert via n8n"):
            payload = {
                "text": st.session_state['raw_text'],
                "json_data": st.session_state['extracted_data'],
                "recipient_email": email
            }
            
            with st.spinner("Contacting n8n..."):
                try:
                    res = requests.post(N8N_WEBHOOK_URL, json=payload)
                    
                    if res.status_code == 200:
                        n8n_data = res.json()
                        st.subheader("Workflow Output")
                        st.write(f"**Final Answer:** {n8n_data.get('final_answer')}")
                        st.success(f"**Status:** {n8n_data.get('status')}")
                    else:
                        st.error(f"n8n Webhook Error ({res.status_code}). Ensure n8n is 'Executing'.")
                
                except Exception as e:
                    st.error("JSON Error: n8n returned an empty response. Fix the connection in n8n!")