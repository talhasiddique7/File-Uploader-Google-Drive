# 🚀 Google Drive File Uploader with Real-Time Progress

A web app built using **Streamlit (Frontend)** and **Flask (Backend)** to upload files directly to your Google Drive with **real-time upload progress tracking**.

---

## 📁 Features

- Upload any file to your **own Google Drive**.
- Live **progress bar** using periodic polling.
- Auto-authentication via **OAuth 2.0** (uses `credentials.json`).
- Handles errors and shows success/failure messages.
- Clean, modern UI powered by Streamlit.
- Thread-safe background file uploading on the backend.

---

## 📚 Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Flask  
- **Google Drive API:** `google-api-python-client`

---

## 🔑 Setup Instructions

### 1. 🌐 Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a **new project** (or use an existing one).
3. Go to **APIs & Services > Credentials**.
4. Click **“+ CREATE CREDENTIALS” > OAuth client ID**:
   - Application type: **Desktop App**
5. Download the `credentials.json` file.
6. Enable the **Google Drive API** under **Library**.

📌 **Place `credentials.json` in the root of your project.**

---

### 2. 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 3. 🚀 Run the App

#### Start the Flask Backend:
```bash
python backend.py
```

#### Start the Streamlit Frontend:
```bash
streamlit run frontend.py
```

> 🟢 Visit `http://localhost:8501` to access the uploader UI.

---

## 🗂️ File Structure

```
google-drive-uploader/
│
│   ├── backend.py              # Flask API to handle file upload and progress tracking
│   └── token.json              # Auto-generated after login (DO NOT COMMIT)
│   ├── frontend.py             # Streamlit app for file upload UI
│   ├── requirements.txt        # dependencies
│
├── credentials.json            # Google OAuth 2.0 credentials (GET FROM GOOGLE)
├── README.md                   # You're reading it!
```

---

## 🔐 Authentication Notes

- The **first time you upload**, you'll be prompted to log in via Google.
- It will create `token.json` which will be reused for later sessions.
- Keep `credentials.json` and `token.json` safe and **never push them to GitHub**.

---

## 💡 Customization Ideas

- Restrict file types (e.g., only images or PDFs)
- Show the uploaded file's Google Drive **link**
- Upload to a specific Drive folder
- Add user authentication (multi-user)
- Show file size limits and restrictions

---

## 🧼 .gitignore Recommendation

```gitignore
*.pyc
__pycache__/
token.json
credentials.json
temp/
```

---

## 🙌 Credits

- [Streamlit](https://streamlit.io/)
- [Flask](https://flask.palletsprojects.com/)
- [Google Drive API Docs](https://developers.google.com/drive/api)

---


