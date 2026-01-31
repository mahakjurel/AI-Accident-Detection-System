"""
AI Model for Accident Detection
Uses CNN for frame-by-frame accident classification

Note: This includes a placeholder model structure.
In production, replace with trained model weights.
"""

import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os


class AccidentDetectionModel:
    """
    Accident Detection Model using CNN
    Processes video frames to detect accidents
    """
    
    def __init__(self):
        """Initialize model"""
        self.model = self._build_model()
        self.img_size = (224, 224)  # Standard input size
        print("✅ AI Model initialized")
    
    def _build_model(self):
        """
        Build CNN model architecture
        
        In production: Load pre-trained weights here
        For now: Using placeholder model structure
        """
        
        model = keras.Sequential([
            # Convolutional layers
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            
            # Flatten and Dense layers
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(64, activation='relu'),
            
            # Output layer (binary classification)
            layers.Dense(2, activation='softmax')  # 0: No Accident, 1: Accident
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # TODO: Load pre-trained weights
        # model.load_weights('accident_detection_weights.h5')
        
        return model
    
    def preprocess_frame(self, frame):
        """
        Preprocess frame for model input
        
        Steps:
        1. Resize to model input size
        2. Normalize pixel values
        3. Add batch dimension
        """
        
        # Resize frame
        frame_resized = cv2.resize(frame, self.img_size)
        
        # Normalize to [0, 1]
        frame_normalized = frame_resized.astype('float32') / 255.0
        
        # Add batch dimension
        frame_batch = np.expand_dims(frame_normalized, axis=0)
        
        return frame_batch
    
    def predict_frame(self, frame):
        """
        Predict if frame contains accident
        
        Returns:
            dict: {
                'accident': bool,
                'confidence': float,
                'probabilities': list
            }
        """
        
        # Preprocess
        processed_frame = self.preprocess_frame(frame)
        
        # Predict
        # NOTE: Since model is not trained, using rule-based detection
        # In production, use: predictions = self.model.predict(processed_frame)
        
        # Placeholder: Detect based on image characteristics
        # This simulates accident detection for demo purposes
        accident_score = self._detect_accident_features(frame)
        
        # Threshold
        is_accident = accident_score > 0.7
        confidence = accident_score if is_accident else (1 - accident_score)
        
        return {
            'accident': is_accident,
            'confidence': round(float(confidence), 2),
            'probabilities': [1 - accident_score, accident_score]
        }
    
    def _detect_accident_features(self, frame):
        """
        Feature-based accident detection (placeholder)
        
        In real scenario: Use trained CNN
        For demo: Use image analysis heuristics
        
        Checks for:
        - Motion blur (indicates high speed/collision)
        - Color distribution (fire, smoke detection)
        - Edge patterns (vehicle deformation)
        """
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate variance of Laplacian (blur detection)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Calculate color variance (unusual colors like fire/smoke)
        color_var = np.std(frame)
        
        # Edge detection
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges) / (edges.shape[0] * edges.shape[1])
        
        # Combine features (simple heuristic)
        # Lower blur + high color variance + high edge density = potential accident
        score = 0.0
        
        if laplacian_var < 100:  # Blurred (motion)
            score += 0.3
        
        if color_var > 80:  # Unusual colors
            score += 0.3
        
        if edge_density > 0.15:  # Many edges (damage/debris)
            score += 0.4
        
        # Add randomness for demo (remove in production)
        score += np.random.uniform(-0.1, 0.1)
        
        return min(max(score, 0.0), 1.0)
    
    def detect_accident_from_video(self, video_path):
        """
        Process entire video and detect accidents
        
        Process:
        1. Extract frames
        2. Analyze each frame
        3. Aggregate predictions
        4. Return final result
        """
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError("Unable to open video file")
        
        frame_predictions = []
        frame_count = 0
        skip_frames = 5  # Process every 5th frame for efficiency
        
        print(f"📹 Processing video: {video_path}")
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Skip frames for efficiency
            if frame_count % skip_frames == 0:
                prediction = self.predict_frame(frame)
                frame_predictions.append(prediction)
            
            frame_count += 1
        
        cap.release()
        
        print(f"✅ Processed {frame_count} frames ({len(frame_predictions)} analyzed)")
        
        if not frame_predictions:
            return {
                "accident": False,
                "confidence": 0.0,
                "severity": "None"
            }
        
        # Aggregate predictions
        accident_count = sum(1 for p in frame_predictions if p['accident'])
        accident_ratio = accident_count / len(frame_predictions)
        
        # Average confidence of accident predictions
        accident_confidences = [p['confidence'] for p in frame_predictions if p['accident']]
        avg_confidence = np.mean(accident_confidences) if accident_confidences else 0.0
        
        # Determine if accident occurred
        is_accident = accident_ratio > 0.3  # At least 30% frames show accident
        
        # Determine severity
        if avg_confidence > 0.85:
            severity = "High"
        elif avg_confidence > 0.65:
            severity = "Medium"
        else:
            severity = "Low"
        
        return {
            "accident": is_accident,
            "confidence": round(float(avg_confidence), 2),
            "severity": severity if is_accident else "None",
            "frames_analyzed": len(frame_predictions),
            "accident_frames": accident_count
        }
    
    def detect_accident_from_image(self, image_path):
        """
        Detect accident from single image
        """
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Read image
        frame = cv2.imread(image_path)
        
        if frame is None:
            raise ValueError("Unable to read image")
        
        # Predict
        prediction = self.predict_frame(frame)
        
        # Determine severity
        if prediction['confidence'] > 0.85:
            severity = "High"
        elif prediction['confidence'] > 0.65:
            severity = "Medium"
        else:
            severity = "Low"
        
        return {
            "accident": prediction['accident'],
            "confidence": prediction['confidence'],
            "severity": severity if prediction['accident'] else "None"
        }


# For testing model independently
if __name__ == "__main__":
    print("Testing Accident Detection Model...")
    
    detector = AccidentDetectionModel()
    print("Model loaded successfully!")
    
    # Test with dummy frame
    dummy_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    result = detector.predict_frame(dummy_frame)
    
    print(f"Test prediction: {result}")