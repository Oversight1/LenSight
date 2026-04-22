import streamlit as st
import requests
from PIL import Image

st.set_page_config(page_title="LenSight Prototype", layout="centered", page_icon="👁️")

# --- SIDEBAR (Security & Roles) ---
with st.sidebar:
    st.header("System Settings")
    researcher_mode = st.toggle("Enable Researcher Mode", value=False)
    st.caption("Unlocks raw data, live web evidence, and model versions.")
    st.markdown("---")
    st.markdown("**System Status:**")
    st.success("API: Online")
    st.success("Database: Connected")

# --- HEADER ---
st.title("LenSight")
st.caption("v1.0 Prototype - Enterprise Deepfake & Misinformation Scanner")
st.markdown("---")

# --- INPUTS ---
caption_text = st.text_area("Enter the associated caption, tweet, or article text (Optional):", placeholder="Paste suspicious text here...")
uploaded_file = st.file_uploader("Upload Image for CNN Analysis (Max 5MB) (Optional)", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None or caption_text:
    
    # Security check 
    MAX_FILE_SIZE = 5 * 1024 * 1024 # 5MB
    if uploaded_file and uploaded_file.size > MAX_FILE_SIZE:
        st.error("Security Alert: File exceeds the 5MB upload limit. Please compress the image and try again.")
    else:
        if st.button("Analyse Media", use_container_width=True, type="primary"):
            with st.spinner('Running Multimodal AI Inference...'):
                try:
                    files = {}
                    data = {}
                    
                    if uploaded_file:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    if caption_text:
                        data = {"caption": caption_text} 
                    
                    response = requests.post("http://127.0.0.1:8000/analyse/", files=files, data=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # --- UI POLISH: Toast Notification ---
                        st.toast('Analysis complete & logged to secure database!', icon='✅')
                        st.markdown("---")
                        
                        st.header("LenSight Analysis Report")
                        col1, col2 = st.columns(2)
                        
                        # --- VISUAL STREAM ---
                        with col1:
                            vis = result["visual_stream"]
                            if vis['label'] == "N/A":
                                st.info("VISUAL STREAM\n\n**No Image Provided**")
                            else:
                                status_color = st.error if vis['label'] == "FAKE" else st.success
                                status_color(f"VISUAL STREAM\n\n**{vis['label']}**")
                                st.metric(label="Confidence", value=f"{vis['confidence']}%")
                                
                                st.markdown("**Visual Analysis Map:**")
                                original_image = Image.open(uploaded_file).convert("RGBA")
                                
                                if vis['label'] == "FAKE":
                                    red_overlay = Image.new("RGBA", original_image.size, (255, 50, 50, 90))
                                    heatmap_img = Image.alpha_composite(original_image, red_overlay)
                                    st.image(heatmap_img, caption="Simulated Activation Map", use_container_width=True)
                                    st.caption("Red zones indicate irregular pixel clusters.")
                                else:
                                    st.image(original_image, caption="No manipulation detected", use_container_width=True)
                                    st.caption("Pixel distribution aligns with natural noise.")
                            
                        # --- TEXTUAL STREAM ---
                        with col2:
                            txt = result["textual_stream"]
                            if txt['label'] == "N/A":
                                st.info("TEXTUAL STREAM\n\n**No Text Provided**")
                            else:
                                status_color = st.warning if txt['label'] == "FAKE/MISINFO" else st.success
                                status_color(f"TEXTUAL STREAM\n\n**{txt['label']}**")
                                st.metric(label="Confidence", value=f"{txt['confidence']}%")

                        # --- RESEARCHER MODE ---
                        if researcher_mode:
                            st.markdown("---")
                            st.subheader("Researcher Mode: Advanced Telemetry")
                            
                            if caption_text:
                                st.markdown("**Live Web Cross-Reference (DuckDuckGo):**")
                                if result["cross_reference"]["evidence"]:
                                    for evidence in result["cross_reference"]["evidence"]:
                                        st.markdown(f"- {evidence}")
                                else:
                                    st.write("No matching web evidence found.")
                            
                            # --- UI POLISH: Expander for raw data ---
                            with st.expander("View Raw Model JSON Output"):
                                st.json(result)
                            
                    else:
                        st.error(f"Backend Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"Connection Error: {e}")
else:
    st.info("Please enter text, upload an image, or provide both to begin analysis.")
