#!/usr/bin/env python3
"""
Create a simple test image with a face-like shape for testing the passport photo app
"""

from PIL import Image, ImageDraw
import os

def create_test_image():
    """Create a simple test image with a face-like oval shape"""
    # Create a 400x400 image with a light blue background
    img = Image.new('RGB', (400, 400), color=(173, 216, 230))
    draw = ImageDraw.Draw(img)
    
    # Draw a simple face-like oval (skin tone)
    face_color = (255, 220, 177)  # Light skin tone
    draw.ellipse([100, 80, 300, 280], fill=face_color, outline=(200, 180, 140), width=3)
    
    # Draw eyes
    eye_color = (50, 50, 50)
    draw.ellipse([140, 140, 170, 160], fill=eye_color)  # Left eye
    draw.ellipse([230, 140, 260, 160], fill=eye_color)  # Right eye
    
    # Draw nose (simple line)
    draw.line([200, 170, 200, 200], fill=(150, 120, 90), width=3)
    
    # Draw mouth
    draw.arc([170, 210, 230, 240], start=0, end=180, fill=(150, 100, 100), width=3)
    
    # Save the test image
    test_dir = "test_images"
    os.makedirs(test_dir, exist_ok=True)
    img_path = os.path.join(test_dir, "test_face.jpg")
    img.save(img_path, "JPEG", quality=95)
    
    print(f"Test image created: {img_path}")
    return img_path

if __name__ == "__main__":
    create_test_image()