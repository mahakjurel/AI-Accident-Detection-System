"""
Database Management for Accident Records
Uses SQLite for storing accident detection history
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional


# Database file path
DB_FILE = "accident_detection.db"


def get_connection():
    """Create database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def init_database():
    """
    Initialize database and create tables
    Called on server startup
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create accidents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            confidence REAL NOT NULL,
            severity TEXT NOT NULL,
            alert_sent BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create alerts table (tracks which alerts were sent)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            accident_id INTEGER NOT NULL,
            alert_type TEXT NOT NULL,
            status TEXT NOT NULL,
            sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (accident_id) REFERENCES accidents (id)
        )
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ Database tables created/verified")


def insert_accident(
    latitude: float,
    longitude: float,
    confidence: float,
    severity: str
) -> int:
    """
    Insert new accident record
    
    Args:
        latitude: GPS latitude
        longitude: GPS longitude
        confidence: Model confidence (0-1)
        severity: Low/Medium/High
    
    Returns:
        int: Accident ID
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO accidents (timestamp, latitude, longitude, confidence, severity)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, latitude, longitude, confidence, severity))
    
    accident_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    print(f"✅ Accident record saved with ID: {accident_id}")
    
    return accident_id


def insert_alert(accident_id: int, alert_type: str, status: str):
    """
    Record alert sent for an accident
    
    Args:
        accident_id: Related accident ID
        alert_type: SMS, Email, Police, Ambulance
        status: Sent/Failed
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO alerts (accident_id, alert_type, status)
        VALUES (?, ?, ?)
    """, (accident_id, alert_type, status))
    
    conn.commit()
    conn.close()


def get_all_accidents() -> List[Dict]:
    """
    Retrieve all accident records
    Used by admin dashboard
    
    Returns:
        List of accident dictionaries
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            id,
            timestamp,
            latitude,
            longitude,
            confidence,
            severity,
            alert_sent
        FROM accidents
        ORDER BY timestamp DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    accidents = []
    for row in rows:
        accidents.append({
            "id": row["id"],
            "time": row["timestamp"],
            "location": f"Lat: {row['latitude']}, Lon: {row['longitude']}",
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "confidence": row["confidence"],
            "severity": row["severity"],
            "status": "Sent" if row["alert_sent"] else "Pending"
        })
    
    return accidents


def get_accident_by_id(accident_id: int) -> Optional[Dict]:
    """
    Get specific accident by ID
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM accidents WHERE id = ?
    """, (accident_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None


def get_accidents_by_severity(severity: str) -> List[Dict]:
    """
    Filter accidents by severity level
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM accidents 
        WHERE severity = ?
        ORDER BY timestamp DESC
    """, (severity,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_recent_accidents(limit: int = 10) -> List[Dict]:
    """
    Get most recent accidents
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM accidents
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_accident_statistics() -> Dict:
    """
    Get overall statistics
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total accidents
    cursor.execute("SELECT COUNT(*) as total FROM accidents")
    total = cursor.fetchone()["total"]
    
    # By severity
    cursor.execute("""
        SELECT severity, COUNT(*) as count
        FROM accidents
        GROUP BY severity
    """)
    severity_counts = {row["severity"]: row["count"] for row in cursor.fetchall()}
    
    # Today's accidents
    cursor.execute("""
        SELECT COUNT(*) as today
        FROM accidents
        WHERE DATE(timestamp) = DATE('now')
    """)
    today = cursor.fetchone()["today"]
    
    conn.close()
    
    return {
        "total_accidents": total,
        "today": today,
        "by_severity": severity_counts
    }


def clear_all_accidents():
    """
    Clear all accident records
    ⚠️ Use with caution - for testing only
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM alerts")
    cursor.execute("DELETE FROM accidents")
    
    conn.commit()
    conn.close()
    
    print("⚠️ All accident records cleared")


# Testing
if __name__ == "__main__":
    print("Initializing database...")
    init_database()
    
    print("\nInserting test accident...")
    accident_id = insert_accident(
        latitude=28.7041,
        longitude=77.1025,
        confidence=0.92,
        severity="High"
    )
    
    print(f"\nRetrieving accidents...")
    accidents = get_all_accidents()
    print(f"Found {len(accidents)} accidents")
    
    for accident in accidents:
        print(f"  - {accident['time']}: {accident['severity']} (confidence: {accident['confidence']})")
    
    print("\nStatistics:")
    stats = get_accident_statistics()
    print(f"  Total: {stats['total_accidents']}")
    print(f"  Today: {stats['today']}")
    print(f"  By Severity: {stats['by_severity']}")