## FOSSEE_Project: Chemical_Equipment_Parameter_Visualizer
### This project is a Hybrid Web + Desktop Application built for visualizing and analyzing chemical equipment parameters from CSV files.

### **It includes:**

🌐 Web App → React + Chart.js

🖥 Desktop App → PyQt5 + Matplotlib

🧠 Backend API → Django + Django REST Framework

📊 Data analysis using Pandas

🗄 Storage using SQLite


### **🚀 Features:**

✔ Upload CSV file

✔ Summary statistics (count, averages)

✔ Equipment type distribution

✔ Tables & Charts

✔ History of last 5 uploads

✔ PDF report generation

✔ Basic authentication

✔ Consistent UI in Web & Desktop

### **🔧 BACKEND SETUP (Django)**

#### 1️⃣ Go to Pro folder:

cd Pro

#### 2️⃣ Create virtual environment:

python -m venv venv

venv\Scripts\activate   

#### 3️⃣ Install dependencies:

pip install -r requirements.txt

If requirements file not present:

pip install django djangorestframework pandas reportlab django-cors-headers

#### 4️⃣ Apply migrations:

python manage.py migrate

#### 5️⃣ Create superuser (for authentication): 

python manage.py createsuperuser

#### 6️⃣ Run server:

python manage.py runserver

Backend runs at:
http://127.0.0.1:8000

### **🌐 FRONTEND SETUP (React Web):**

#### 1️⃣ Go to frontend folder:

cd web

#### 2️⃣ Install dependencies:

npm install

#### 3️⃣ Start React app:

npm start

Runs at:
http://localhost:3000

### **🔐 Authentication:**

Basic Authentication is enabled.

#### 1️⃣ Set credentials in Upload.js:

const USERNAME = "mohan";

const PASSWORD = "Mohan@0407";

These should match your Django superuser.

### **🖥 DESKTOP APP SETUP:**

#### 1️⃣ Install requirements:

pip install PyQt5 matplotlib requests

#### 2️⃣ Run the app:

python desktop_app.py

The desktop app connects to the same Django backend.

### **📄 PDF REPORT GENERATION:**

Both web and desktop versions can generate a PDF containing:

✔ Summary statistics

✔ Type distribution table

### **📁 CSV FORMAT:**

Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature

Use provided: sample_equipment_data.csv

### **📊 Charts Used:**

✔ Web  - Chart.js (Bar + Pie)

✔ Desktop - Matplotlib 

### **🕒 History Feature:**
Last 5 uploaded datasets are stored and can be reloaded.

### **🧪 API Endpoints:**

/upload/	- POST	→ Upload CSV

/summary/	- GET	→ Latest summary

/history/	- GET	→ Last 5 records

/generate-pdf/	- GET	→ Download PDF

### **🧠 Technologies Used:**

→ React.js

→ Chart.js

→ Bootstrap

→ Django

→ Django REST Framework

→ Pandas

→ PyQt5

→ Matplotlib

→ SQLite

