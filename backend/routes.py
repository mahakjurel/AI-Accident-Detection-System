"""
API Routes for Accident Detection System
All endpoints for video processing, accident detection, and alerts
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import os
import shutil

from model import AccidentDetectionModel
from location import get_location_from_ip
from alert import send_emergency_alerts
from database import insert_accident, get_all_accidents

# =========================
# Router & Model Init
# =========================

router = APIRouter()
detector = AccidentDetectionModel()

# =========================
# Upload Directory (SAFE)
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================
# VIDEO UPLOAD & DETECTION
# =========================

@router.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    """
    Upload video for accident detection
    """

    try:
        # Validate file type safely
        if not file.content_type or not file.content_type.startswith("video/"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload a video file."
            )

        # Save uploaded video
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = f"{timestamp}_{file.filename}"
        video_path = os.path.join(UPLOAD_DIR, video_filename)

        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"📹 Video saved: {video_path}")

        # Run accident detection
        print("🔍 Analyzing video for accidents...")
        result = detector.detect_accident_from_video(video_path)

        # Accident detected
        if result.get("accident"):
            print("🚨 ACCIDENT DETECTED!")

            # Get location
            location_data = get_location_from_ip()

            # Send alerts
            alert_status = send_emergency_alerts(
                location=location_data["city"],
                severity=result["severity"]
            )

            # Store in database
            accident_id = insert_accident(
                latitude=location_data["latitude"],
                longitude=location_data["longitude"],
                confidence=result["confidence"],
                severity=result["severity"]
            )

            return JSONResponse(content={
                "accident": True,
                "confidence": result["confidence"],
                "severity": result["severity"],
                "location": location_data,
                "alerts": alert_status,
                "accident_id": accident_id,
                "timestamp": datetime.now().isoformat()
            })

        # No accident
        return JSONResponse(content={
            "accident": False,
            "confidence": result["confidence"],
            "message": "No accident detected. Traffic normal.",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        print(f"❌ Error processing video: {e}")
        raise HTTPException(status_code=500, detail="Error processing video")


# =========================
# FRAME / IMAGE DETECTION
# =========================

@router.post("/upload-frame")
async def upload_frame(file: UploadFile = File(...)):
    """
    Upload single image/frame for accident detection
    """

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        frame_path = os.path.join(UPLOAD_DIR, f"frame_{timestamp}.jpg")

        with open(frame_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = detector.detect_accident_from_image(frame_path)

        return JSONResponse(content={
            "accident": result["accident"],
            "confidence": result["confidence"],
            "severity": result["severity"],
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing frame")


# =========================
# ACCIDENT RECORDS (ADMIN)
# =========================

@router.get("/accidents")
async def get_accidents():
    """
    Fetch all accident records for admin dashboard
    """

    try:
        accidents = get_all_accidents()
        return JSONResponse(content={
            "success": True,
            "count": len(accidents),
            "accidents": accidents
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching accidents")


# =========================
# LOCATION API
# =========================

@router.get("/location")
async def get_current_location():
    """
    Get current location using IP
    """

    try:
        return JSONResponse(content=get_location_from_ip())
    except Exception:
        raise HTTPException(status_code=500, detail="Error fetching location")


# =========================
# SIMULATE ACCIDENT (TEST)
# =========================

@router.post("/simulate-accident")
async def simulate_accident():
    """
    Simulate accident for testing/demo
    """

    try:
        location_data = get_location_from_ip()

        alert_status = send_emergency_alerts(
            location=location_data["city"],
            severity="High"
        )

        accident_id = insert_accident(
            latitude=location_data["latitude"],
            longitude=location_data["longitude"],
            confidence=0.95,
            severity="High"
        )

        return JSONResponse(content={
            "accident": True,
            "confidence": 0.95,
            "severity": "High",
            "location": location_data,
            "alerts": alert_status,
            "accident_id": accident_id,
            "timestamp": datetime.now().isoformat()
        })

    except Exception:
        raise HTTPException(status_code=500, detail="Simulation failed")


# =========================
# SYSTEM STATISTICS
# =========================

@router.get("/stats")
async def get_statistics():
    """
    System statistics for dashboard
    """

    try:
        accidents = get_all_accidents()

        stats = {
            "total": len(accidents),
            "high": sum(1 for a in accidents if a["severity"] == "High"),
            "medium": sum(1 for a in accidents if a["severity"] == "Medium"),
            "low": sum(1 for a in accidents if a["severity"] == "Low"),
        }

        return JSONResponse(content={
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        })

    except Exception:
        raise HTTPException(status_code=500, detail="Error fetching statistics")
