"""
Face detection and alignment utilities
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw
import logging

logger = logging.getLogger(__name__)

class FaceDetector:
    """Face detection and alignment class using OpenCV"""
    
    def __init__(self):
        self.face_locations = []
        self.face_landmarks = []
        # Load OpenCV's pre-trained face detection model
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def detect_faces(self, image_path):
        """
        Detect faces in an image using OpenCV
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            tuple: (face_locations, face_landmarks, processed_image)
        """
        try:
            # Load image with OpenCV
            cv_image = cv2.imread(image_path)
            if cv_image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Convert to RGB for PIL
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            
            # Convert to grayscale for face detection
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray_image, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            
            # Convert OpenCV format (x, y, w, h) to face_recognition format (top, right, bottom, left)
            self.face_locations = []
            for (x, y, w, h) in faces:
                top = y
                right = x + w
                bottom = y + h
                left = x
                self.face_locations.append((top, right, bottom, left))
            
            # No landmarks for OpenCV detection (simplified)
            self.face_landmarks = [{}] * len(self.face_locations)
            
            logger.info(f"Detected {len(self.face_locations)} face(s) in image")
            
            # Convert to PIL Image for processing
            pil_image = Image.fromarray(rgb_image)
            
            return self.face_locations, self.face_landmarks, pil_image
            
        except Exception as e:
            logger.error(f"Error detecting faces: {str(e)}")
            raise
    
    def highlight_faces(self, image, face_locations):
        """
        Draw rectangles around detected faces
        
        Args:
            image (PIL.Image): Input image
            face_locations (list): List of face location tuples
            
        Returns:
            PIL.Image: Image with face rectangles drawn
        """
        try:
            # Create a copy of the image
            highlighted_image = image.copy()
            draw = ImageDraw.Draw(highlighted_image)
            
            for (top, right, bottom, left) in face_locations:
                # Draw rectangle around face
                draw.rectangle([(left, top), (right, bottom)], 
                             outline="red", width=3)
                
                # Add face number
                face_num = face_locations.index((top, right, bottom, left)) + 1
                draw.text((left, top - 20), f"Face {face_num}", 
                         fill="red")
            
            return highlighted_image
            
        except Exception as e:
            logger.error(f"Error highlighting faces: {str(e)}")
            return image
    
    def get_face_center(self, face_location):
        """
        Calculate the center point of a face
        
        Args:
            face_location (tuple): Face location (top, right, bottom, left)
            
        Returns:
            tuple: (center_x, center_y)
        """
        top, right, bottom, left = face_location
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
        return center_x, center_y
    
    def get_eye_positions(self, face_landmarks_dict):
        """
        Get eye positions from face landmarks
        
        Args:
            face_landmarks_dict (dict): Face landmarks dictionary
            
        Returns:
            tuple: (left_eye_center, right_eye_center)
        """
        try:
            if 'left_eye' in face_landmarks_dict and 'right_eye' in face_landmarks_dict:
                left_eye = face_landmarks_dict['left_eye']
                right_eye = face_landmarks_dict['right_eye']
                
                # Calculate eye centers
                left_eye_center = np.mean(left_eye, axis=0).astype(int)
                right_eye_center = np.mean(right_eye, axis=0).astype(int)
                
                return tuple(left_eye_center), tuple(right_eye_center)
            
            return None, None
            
        except Exception as e:
            logger.error(f"Error getting eye positions: {str(e)}")
            return None, None
    
    def align_face(self, image, face_landmarks_dict):
        """
        Align face based on eye positions
        
        Args:
            image (PIL.Image): Input image
            face_landmarks_dict (dict): Face landmarks dictionary
            
        Returns:
            PIL.Image: Aligned image
        """
        try:
            left_eye, right_eye = self.get_eye_positions(face_landmarks_dict)
            
            if left_eye is None or right_eye is None:
                logger.warning("Could not find eye positions for alignment")
                return image
            
            # Calculate angle between eyes
            dx = right_eye[0] - left_eye[0]
            dy = right_eye[1] - left_eye[1]
            angle = np.degrees(np.arctan2(dy, dx))
            
            # Rotate image to align eyes horizontally
            rotated_image = image.rotate(-angle, expand=True, fillcolor='white')
            
            logger.info(f"Face aligned with rotation angle: {angle:.2f} degrees")
            return rotated_image
            
        except Exception as e:
            logger.error(f"Error aligning face: {str(e)}")
            return image
    
    def crop_face_area(self, image, face_location, padding=50):
        """
        Crop image around face area with padding
        
        Args:
            image (PIL.Image): Input image
            face_location (tuple): Face location (top, right, bottom, left)
            padding (int): Padding around face in pixels
            
        Returns:
            PIL.Image: Cropped face area
        """
        try:
            top, right, bottom, left = face_location
            
            # Add padding
            left = max(0, left - padding)
            top = max(0, top - padding)
            right = min(image.width, right + padding)
            bottom = min(image.height, bottom + padding)
            
            # Crop the image
            cropped_image = image.crop((left, top, right, bottom))
            
            return cropped_image
            
        except Exception as e:
            logger.error(f"Error cropping face area: {str(e)}")
            return image
