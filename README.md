# 🏙️ Real Estate Analysis Chatbot

A full-stack web application that analyzes real-estate localities using an Excel dataset.  
Users can type natural language queries like **“Analyze Wakad”**, and the system returns:

- 📄 Summary of the locality  
- 📊 Price & demand trend charts  
- 📋 Filtered table from Excel  
- 💬 Chat-style interface for queries  

🌐 **Live Project:**  
https://sigmavalue-assignment.onrender.com/

---

## ⭐ Features

### 🔍 NLP-Based Query Handling
- Analyze single locality (e.g., “Analyze Aundh”)
- Multi-locality comparison (e.g., “Compare Wakad and Akurdi”)
- Best investment suggestions

### 📊 Charts & Trends
- Price trend (2020–2024)
- Demand / units sold
- Multi-area comparison chart

### 📁 Excel Data Processing
- Loads static Excel file using pandas
- Cleans data (NaN, missing values, formatting)
- JSON-safe response for the frontend

### 🧾 Clean UI
- React + Bootstrap chat interface  
- Auto-scroll chat  
- Chart + table rendering  

---

## 🛠️ Tech Stack

### **Frontend**
- React  
- Bootstrap  
- Recharts (charts)

### **Backend**
- Django  
- Django REST Framework  
- Pandas  
- Openpyxl  

### **Deployment**
- Render (Backend + Frontend together)
- GitHub (Version control)

---

## 📂 Project Structure
sigmavalue-assignment/
│
├── backend/
│   ├── api/
│   ├── realestate_chatbot/
│   ├── frontend_build/   ← React production build
│   ├── requirements.txt
│   └── manage.py
│
└── frontend/
    ├── src/
    ├── public/
    └── build/            ← generated locally
```

---
```
## 🚀 How to Run Locally

### **1️⃣ Backend Setup**
```bash
cd backend
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
python manage.py runserver
```

### **2️⃣ Frontend Setup**
```bash
cd frontend
npm install
npm start
```

### **3️⃣ Build Frontend for Production**

During deployment, the React app must be built and copied into the backend so Django can serve it.

To create the production build:

```bash
cd frontend
npm run build
```

This generates a `build/` folder inside `frontend/`.

Copy the entire build folder into:

```
backend/frontend_build/
```

Final structure must include:

```
backend/frontend_build/index.html
backend/frontend_build/static/js/
backend/frontend_build/static/css/
```

## 📌 API Endpoint

### POST `/api/analyze/`

**Request**
```json
{
  "query": "Analyze Wakad"
}
```
