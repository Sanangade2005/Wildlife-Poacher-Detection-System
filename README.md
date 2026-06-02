# 🦁 Wildlife Poacher Detection System

An AI-powered wildlife monitoring and poacher detection system that uses YOLOv8 object detection, computer vision, Gemini AI, and real-time alert generation to identify suspicious human activity in protected wildlife areas.

## 🚀 Project Overview

Wildlife poaching remains one of the biggest threats to endangered species. This project automates surveillance by analyzing video feeds and detecting human presence in protected zones.

When suspicious activity is detected, the system:

- Detects humans using YOLOv8
- Analyzes the threat using AI models
- Generates alerts automatically
- Sends email notifications to authorities
- Stores detection records for future investigation

## ✨ Features

- Real-time video analysis
- YOLOv8 object detection
- Human intrusion detection
- Gemini AI integration
- OpenAI integration
- Automated email alerts
- Detection history storage
- Database support
- FastAPI backend
- Modern React frontend

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- SQLite
- YOLOv8
- OpenCV

### AI Services
- Google Gemini API
- OpenAI API

### Frontend
- React
- Vite
- Tailwind CSS

## 📂 Project Structure

```
Wildlife-Poacher-Detection-System/
│
├── Backend/
│   ├── app.py
│   ├── detector.py
│   ├── gemini_client.py
│   ├── gpt_client.py
│   ├── email_alert.py
│   └── requirements.txt
│
├── forest-guard-ai/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Sanangade2005/Wildlife-Poacher-Detection-System.git
cd Wildlife-Poacher-Detection-System
```

### Backend Setup

```bash
cd Backend

pip install -r requirements.txt

python app.py
```

### Frontend Setup

```bash
cd forest-guard-ai

npm install

npm run dev
```

## 📸 Screenshots

Add screenshots of:

- Dashboard
- Detection Results
- Alert System
- Video Analysis Interface

## 🎯 Future Enhancements

- Live CCTV integration
- Mobile application
- GPS tracking support
- Multi-camera monitoring
- Cloud deployment
- Advanced threat prediction

## 👨‍💻 Author

Sanan Gade

GitHub:
https://github.com/Sanangade2005

## 📄 License

This project is licensed under the MIT License.
