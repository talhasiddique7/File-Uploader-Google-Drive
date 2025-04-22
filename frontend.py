import streamlit as st
import requests
import time

st.set_page_config(page_title="Drive Uploader", layout="centered")
st.title("📂 Google Drive File Uploader")
st.markdown("Upload files directly to your Google Drive with real-time progress tracking.")

uploaded_file = st.file_uploader("Choose a file", type=None)

if uploaded_file:
    st.info(f"File ready: **{uploaded_file.name}** ({uploaded_file.size / 1024:.2f} KB)")

    if st.button("🚀 Start Upload"):
        with st.status("Uploading file to Google Drive...", expanded=True) as status_msg:
            files = {'file': (uploaded_file.name, uploaded_file.getvalue())}
            try:
                res = requests.post("http://localhost:5001/upload", files=files)
                if res.status_code != 200:
                    st.error(f"Upload failed: {res.text}")
                    st.stop()

                upload_id = res.json().get("upload_id")
                progress_bar = st.progress(0)
                progress_text = st.empty()

                while True:
                    time.sleep(1)
                    check = requests.get(f"http://localhost:5001/progress/{upload_id}")
                    progress = check.json().get("progress")

                    if isinstance(progress, str) and progress.startswith("error"):
                        st.error(f"Upload Error: {progress}")
                        break

                    progress_bar.progress(progress / 100)
                    progress_text.text(f"{progress}% uploaded")

                    if progress >= 100:
                        status_msg.update(label="✅ Upload completed successfully!", state="complete")
                        break

            except Exception as e:
                st.error(f"Error: {str(e)}")
