"""
Emergency Alert System
Sends SMS, Email, and other alerts when accident is detected
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict
import os


# ========================
# CONFIGURATION
# ========================

# Email Configuration (Gmail example)
EMAIL_SENDER = "your-email@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "your-app-password"    # Replace with app password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Emergency Contacts
EMERGENCY_CONTACTS = {
    "ambulance": "+911234567890",
    "police": "+911234567891",
    "family": "+911234567892",
    "email": "emergency@example.com"
}

# Twilio Configuration (for SMS)
# Sign up at https://www.twilio.com for credentials
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "+1234567890"


# ========================
# EMAIL ALERTS
# ========================

def send_email_alert(location: str, severity: str, confidence: float) -> Dict:
    """
    Send email alert about accident
    
    Args:
        location: Accident location
        severity: High/Medium/Low
        confidence: Model confidence
    
    Returns:
        dict: Status of email sending
    """
    
    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = EMAIL_SENDER
        message["To"] = EMERGENCY_CONTACTS["email"]
        message["Subject"] = f"🚨 URGENT: {severity} Severity Accident Detected"
        
        # Email body
        body = f"""
        EMERGENCY ALERT - ACCIDENT DETECTED
        =====================================
        
        Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        Location: {location}
        Severity: {severity}
        Confidence: {confidence * 100:.1f}%
        
        IMMEDIATE ACTION REQUIRED:
        - Ambulance has been notified
        - Police have been alerted
        - Emergency response team dispatched
        
        Location Coordinates: Available in system dashboard
        
        This is an automated alert from the AI Accident Detection System.
        Please respond immediately.
        
        ---
        AI Accident Detection System
        Emergency Response Unit
        """
        
        message.attach(MIMEText(body, "plain"))
        
        # NOTE: Email sending is commented out to prevent accidental sends
        # Uncomment and configure with real credentials in production
        
        """
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        text = message.as_string()
        server.sendmail(EMAIL_SENDER, EMERGENCY_CONTACTS["email"], text)
        server.quit()
        
        print("✅ Email alert sent successfully")
        return {"status": "sent", "method": "email"}
        """
        
        # Simulation mode
        print(f"📧 [SIMULATED] Email alert would be sent to: {EMERGENCY_CONTACTS['email']}")
        return {"status": "simulated", "method": "email"}
    
    except Exception as e:
        print(f"❌ Email alert failed: {str(e)}")
        return {"status": "failed", "method": "email", "error": str(e)}


# ========================
# SMS ALERTS
# ========================

def send_sms_alert(location: str, severity: str, phone_number: str = None) -> Dict:
    """
    Send SMS alert using Twilio
    
    Args:
        location: Accident location
        severity: High/Medium/Low
        phone_number: Optional specific phone number
    
    Returns:
        dict: Status of SMS sending
    """
    
    try:
        if phone_number is None:
            phone_number = EMERGENCY_CONTACTS["ambulance"]
        
        message = f"""
        🚨 ACCIDENT ALERT
        
        Severity: {severity}
        Location: {location}
        Time: {datetime.now().strftime("%H:%M:%S")}
        
        Immediate assistance required.
        - AI Accident Detection System
        """
        
        # NOTE: Twilio SMS is commented out to prevent accidental sends
        # Uncomment and configure with real credentials in production
        
        """
        from twilio.rest import Client
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        
        print(f"✅ SMS sent to {phone_number}")
        return {"status": "sent", "method": "sms", "sid": message.sid}
        """
        
        # Simulation mode
        print(f"📱 [SIMULATED] SMS would be sent to: {phone_number}")
        print(f"    Message: {message.strip()}")
        return {"status": "simulated", "method": "sms"}
    
    except Exception as e:
        print(f"❌ SMS alert failed: {str(e)}")
        return {"status": "failed", "method": "sms", "error": str(e)}


# ========================
# AMBULANCE ALERT
# ========================

def alert_ambulance(location: str, severity: str) -> Dict:
    """
    Alert ambulance service
    """
    
    print(f"🚑 Alerting ambulance service...")
    
    # Send SMS to ambulance
    sms_result = send_sms_alert(location, severity, EMERGENCY_CONTACTS["ambulance"])
    
    # In production, could also:
    # - Call ambulance dispatch API
    # - Send location coordinates
    # - Provide patient count estimate
    
    return {
        "service": "ambulance",
        "status": "notified",
        "method": "sms",
        "details": sms_result
    }


# ========================
# POLICE ALERT
# ========================

def alert_police(location: str, severity: str) -> Dict:
    """
    Alert police department
    """
    
    print(f"🚓 Alerting police department...")
    
    # Send SMS to police
    sms_result = send_sms_alert(location, severity, EMERGENCY_CONTACTS["police"])
    
    # In production, could also:
    # - Send to traffic control center
    # - Update digital signage
    # - Alert nearby patrol units
    
    return {
        "service": "police",
        "status": "notified",
        "method": "sms",
        "details": sms_result
    }


# ========================
# FAMILY/CONTACT ALERT
# ========================

def alert_emergency_contact(location: str, severity: str) -> Dict:
    """
    Alert emergency contact person
    """
    
    print(f"👨‍👩‍👧 Alerting emergency contact...")
    
    # Send both SMS and Email
    sms_result = send_sms_alert(location, severity, EMERGENCY_CONTACTS["family"])
    email_result = send_email_alert(location, severity, 0.9)
    
    return {
        "service": "emergency_contact",
        "status": "notified",
        "methods": ["sms", "email"],
        "details": {
            "sms": sms_result,
            "email": email_result
        }
    }


# ========================
# MASTER ALERT FUNCTION
# ========================

def send_emergency_alerts(location: str, severity: str) -> Dict:
    """
    Send all emergency alerts
    
    This is the main function called when accident is detected
    
    Args:
        location: Accident location
        severity: High/Medium/Low
    
    Returns:
        dict: Status of all alerts
    """
    
    print(f"\n{'='*50}")
    print(f"🚨 EMERGENCY ALERT SYSTEM ACTIVATED")
    print(f"{'='*50}")
    print(f"Location: {location}")
    print(f"Severity: {severity}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    # Send all alerts
    alerts_status = {
        "timestamp": datetime.now().isoformat(),
        "location": location,
        "severity": severity,
        "alerts": {}
    }
    
    # Alert ambulance (highest priority)
    alerts_status["alerts"]["ambulance"] = alert_ambulance(location, severity)
    
    # Alert police
    alerts_status["alerts"]["police"] = alert_police(location, severity)
    
    # Alert emergency contact
    alerts_status["alerts"]["emergency_contact"] = alert_emergency_contact(location, severity)
    
    print(f"\n{'='*50}")
    print(f"✅ All emergency alerts dispatched")
    print(f"{'='*50}\n")
    
    return alerts_status


# ========================
# NOTIFICATION SYSTEM
# ========================

def send_push_notification(title: str, body: str) -> Dict:
    """
    Send push notification to mobile app
    
    In production, use:
    - Firebase Cloud Messaging (FCM)
    - Apple Push Notification Service (APNS)
    """
    
    print(f"📲 [SIMULATED] Push notification: {title}")
    return {"status": "simulated", "method": "push"}


def send_webhook_alert(url: str, data: Dict) -> Dict:
    """
    Send alert to webhook URL
    Useful for integrating with other systems
    """
    
    import requests
    
    try:
        response = requests.post(url, json=data, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Webhook alert sent to {url}")
            return {"status": "sent", "method": "webhook"}
        else:
            print(f"⚠️ Webhook returned status {response.status_code}")
            return {"status": "failed", "method": "webhook"}
    
    except Exception as e:
        print(f"❌ Webhook alert failed: {str(e)}")
        return {"status": "failed", "method": "webhook", "error": str(e)}


# ========================
# TESTING
# ========================

if __name__ == "__main__":
    print("Testing Emergency Alert System...\n")
    
    # Test alert system
    result = send_emergency_alerts(
        location="NH-44, Near India Gate, New Delhi",
        severity="High"
    )
    
    print("\nAlert Status:")
    print(f"Ambulance: {result['alerts']['ambulance']['status']}")
    print(f"Police: {result['alerts']['police']['status']}")
    print(f"Emergency Contact: {result['alerts']['emergency_contact']['status']}")