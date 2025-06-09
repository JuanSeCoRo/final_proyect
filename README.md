# final_proyect

# EcoImpact — Climate Awareness Web App

Welcome to **EcoImpact** — an educational web application to raise awareness about climate change and help users measure and reduce their carbon footprint.

This project was built as a complete final project using Python and Flask, with a full user system and interactive features.

---

## Features

User Registration and Login  
Personalized Carbon Footprint Calculator  
Live Climate Data by City (via Open-Meteo API)  
Personal History of Footprint Results  
Ability to Clear History (per user)    
Account Settings: Log Out, Delete Account, Change Password  
Responsive, modern UI with Dark Mode toggle  
Friendly animations for smoother UX  
Custom mini confirmation tabs for Clear History and Delete Account  

---

## Purpose

EcoImpact aims to:

- Teach users about how daily choices impact climate change   
- Encourage more sustainable behaviors  
- Make learning about climate change fun and interactive 
- Provide a polished example of a full-stack web application with Flask  

---

## Technologies Used

- **Python 3.11+**
- **Flask**
- **Flask-Login**
- **Flask-SQLAlchemy**
- **HTML + CSS + Jinja2**
- **JavaScript (for animations & modals)**
- **Chart.js** (animated carbon footprint pie chart)
- **Open-Meteo API** (for real-time weather data)
- **SQLite** (local database for users and history)

---

## How to Run the Project

### 1️⃣ Clone or Download the Project

```bash
git clone https://github.com/YOUR_USERNAME/ecoimpact.git
cd ecoimpact
```

### 2️⃣ Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Initialize the Database

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...     exit()
```

### 5️⃣ Run the App

```bash
python app.py
```

### 6️⃣ Open in Browser



## 📝 How to Use

### 🚪 Register & Login

- Create your account
- Log in to access personalized features

### 📊 Calculate Your Footprint

- Go to "Calculator"
- Enter your weekly transport, meat consumption, and electricity usage
- View your total carbon footprint with a friendly pie chart and advice

### 🧾 View History

- Go to "History" to see your past results
- You can Clear History with a confirmation mini tab

### 🌤️ Live Climate Data

- Go to "Live Climate"
- Enter your city to see current weather data (powered by Open-Meteo API)

### ⚙️ Account Settings

- Log Out  
- Change Password (with mini confirmation tab)  
- Delete Account (with mini confirmation tab)  

---

## 🎨 Customization

You can easily customize the app:

- Edit tips and advice in `index.html`
- Add more features in the Settings page
- Style it even further using `styles.css`

---

## 🙏 Credits

Built by: **Juan Sebastian Corredor Romero**  
Final project for **Python + Web Development Course**  
Special thanks to all open source projects used: Flask, Chart.js, Open-Meteo.

---

## 📜 License

This project is for educational purposes.  
You are welcome to fork it and adapt it for your own learning or teaching.

---
