# 🚦 AI Accident Detection System - Backend

A production-ready FastAPI backend for real-time accident detection using computer vision and deep learning.

---

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI server entry point
├── routes.py            # API endpoints
├── model.py             # AI accident detection model
├── database.py          # SQLite database operations
├── location.py          # IP-based location detection
├── alert.py             # Emergency alert system
├── requirements.txt     # Python dependencies
├── uploads/             # Uploaded videos (auto-created)
└── accident_detection.db # SQLite database (auto-created)
```

---

## 🚀 Quick Start

### Step 1: Install Python
Ensure Python 3.8+ is installed:
```bash
python --version
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Server
```bash
python main.py
```

Server will start at: **http://localhost:8000**

---

## 📚 API Endpoints

### 1. **Upload Video for Detection**
```bash
POST /api/upload-video
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/upload-video" \
  -F "file=@accident_video.mp4"
```

**Response:**
```json
{
  "accident": true,
  "confidence": 0.87,
  "severity": "High",
  "location": {
    "city": "New Delhi",
    "latitude": 28.6139,
    "longitude": 77.2090
  },
  "alerts": {
    "ambulance": "sent",
    "police": "sent"
  }
}
```

---

### 2. **Upload Single Frame**
```bash
POST /api/upload-frame
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/upload-frame" \
  -F "file=@frame.jpg"
```

---

### 3. **Get All Accidents (Dashboard)**
```bash
GET /api/accidents
```

**Example:**
```bash
curl "http://localhost:8000/api/accidents"
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "accidents": [
    {
      "id": 1,
      "time": "2026-01-26 10:45:00",
      "location": "Lat: 28.61, Lon: 77.20",
      "severity": "High",
      "confidence": 0.92
    }
  ]
}
```

---

### 4. **Get Current Location**
```bash
GET /api/location
```

---

### 5. **Simulate Accident (Testing)**
```bash
POST /api/simulate-accident
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/simulate-accident"
```

---

### 6. **Get Statistics**
```bash
GET /api/stats
```

---

## 🧠 How It Works

### System Flow:
```
1. Frontend uploads video → FastAPI endpoint
2. Video saved to uploads/
3. Video → extracted frames (OpenCV)
4. Frames → CNN model → prediction
5. If accident detected:
   ├── Get location (IP → lat/lon)
   ├── Send SMS alerts (Twilio)
   ├── Send email alerts (SMTP)
   └── Store in SQLite database
6. Return response to frontend
```

---

## 🤖 AI Model

### Current Implementation:
- **Architecture**: CNN (Convolutional Neural Network)
- **Layers**: Conv2D → MaxPooling → Dense
- **Input**: 224x224 RGB images
- **Output**: Binary classification (Accident/Normal)

### Feature Detection:
The placeholder model analyzes:
- **Motion blur** (indicates collision/high speed)
- **Color variance** (fire, smoke)
- **Edge density** (vehicle damage, debris)

### Upgrading to Real Model:
Replace placeholder in `model.py`:
```python
# Load your trained model
model.load_weights('accident_model_weights.h5')
```

---

## 🗄️ Database Schema

### `accidents` Table:
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| timestamp | DATETIME | When accident occurred |
| latitude | REAL | GPS latitude |
| longitude | REAL | GPS longitude |
| confidence | REAL | Model confidence (0-1) |
| severity | TEXT | Low/Medium/High |

### `alerts` Table:
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| accident_id | INTEGER | Foreign key |
| alert_type | TEXT | SMS/Email/Push |
| status | TEXT | Sent/Failed |
| sent_at | DATETIME | When alert was sent |

---

## 📧 Alert Configuration

### Email Setup (Gmail):
1. Enable 2FA on your Google account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Update in `alert.py`:
```python
EMAIL_SENDER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"
```

### SMS Setup (Twilio):
1. Sign up at: https://www.twilio.com
2. Get credentials from dashboard
3. Update in `alert.py`:
```python
TWILIO_ACCOUNT_SID = "your_sid"
TWILIO_AUTH_TOKEN = "your_token"
TWILIO_PHONE_NUMBER = "+1234567890"
```

### Emergency Contacts:
Update in `alert.py`:
```python
EMERGENCY_CONTACTS = {
    "ambulance": "+911234567890",
    "police": "+911234567891",
    "family": "+911234567892"
}
```

---

## 🌍 Location Services

### IP-Based Location:
Uses **ipapi.co** (free, no auth required)

### Fallback Location:
If API fails, defaults to Delhi, India coordinates

### Reverse Geocoding:
Converts lat/lon to address using OpenStreetMap Nominatim

---

## 🔗 Frontend Integration

### Update Frontend JavaScript:
```javascript
// In your script.js
async function uploadVideo(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('http://localhost:8000/api/upload-video', {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    
    if (result.accident) {
        // Show alert
        document.getElementById('alertBox').classList.remove('hidden');
        document.getElementById('statusText').innerText = 'Accident Detected!';
        document.getElementById('probability').innerText = `${result.confidence * 100}%`;
        document.getElementById('locationText').innerText = result.location.city;
    }
}
```

---

## 🧪 Testing

### 1. Test Server Health:
```bash
curl http://localhost:8000/
```

### 2. Test with Sample Video:
```bash
curl -X POST "http://localhost:8000/api/upload-video" \
  -F "file=@test_video.mp4"
```

### 3. Test Simulation:
```bash
curl -X POST "http://localhost:8000/api/simulate-accident"
```

### 4. Test Dashboard Data:
```bash
curl "http://localhost:8000/api/accidents"
```

---

## 📊 API Documentation

Once server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Interactive API testing interface included!

---

## 🛠️ Customization

### Change Server Port:
In `main.py`:
```python
uvicorn.run("main:app", host="0.0.0.0", port=5000)
```

### Add CORS Origins:
In `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"]
)
```

### Adjust Confidence Threshold:
In `model.py`:
```python
is_accident = accident_score > 0.7  # Change threshold
```

---

## 🚨 Production Deployment

### Before deploying:

1. **Set Environment Variables**:
```bash
export EMAIL_SENDER="your-email@gmail.com"
export EMAIL_PASSWORD="your-password"
export TWILIO_SID="your-sid"
```

2. **Disable Debug Mode**:
```python
# In main.py
uvicorn.run("main:app", reload=False)
```

3. **Use Production Database**:
Consider PostgreSQL instead of SQLite

4. **Add Authentication**:
Implement JWT tokens for API security

5. **Use HTTPS**:
Deploy behind reverse proxy (nginx)

6. **Set Rate Limiting**:
Prevent API abuse

---

## 📝 Project Checklist

- [x] FastAPI server setup
- [x] Video upload endpoint
- [x] AI model integration
- [x] Database (SQLite)
- [x] Location detection
- [x] Alert system (SMS/Email)
- [x] Admin dashboard API
- [x] CORS enabled
- [x] Error handling
- [x] Logging
- [x] API documentation

---

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **OpenCV**: https://docs.opencv.org/
- **TensorFlow**: https://www.tensorflow.org/
- **Twilio SMS**: https://www.twilio.com/docs/sms

---

## 🤝 Contributing

This is a final year/internship project template. Feel free to:
- Add more features
- Improve AI model
- Add unit tests
- Enhance error handling
- Add authentication

---

## 📄 License

MIT License - Free to use for educational purposes

---

## 💬 Support

For issues or questions:
1. Check API docs: http://localhost:8000/docs
2. Review error logs in console
3. Verify all dependencies installed
4. Ensure Python 3.8+ is used

---

## 🎯 Next Steps

1. ✅ Backend is ready
2. Connect frontend to backend
3. Test with real videos
4. Train custom AI model
5. Deploy to cloud (AWS/GCP/Azure)
6. Add user authentication
7. Create mobile app

---

**Built with ❤️ for safer roads**