#!/usr/bin/env python3
"""
AI-Powered Passport Photo Creator
Main application entry point
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import PassportPhotoApp

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('passport_photo_app.log'),
            logging.StreamHandler()
        ]
    )

def check_dependencies():
    """Check if all required dependencies are available"""
    required_modules = [
        'PIL', 'cv2', 'face_recognition', 'rembg', 'numpy'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = f"Missing required modules: {', '.join(missing_modules)}\n"
        error_msg += "Please install them using:\n"
        error_msg += "pip install pillow opencv-python face-recognition rembg numpy"
        messagebox.showerror("Missing Dependencies", error_msg)
        return False
    
    return True

def main():
    """Main application entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Create and run the application
        logger.info("Starting Passport Photo Creator application")
        
        root = tk.Tk()
        app = PassportPhotoApp(root)
        
        # Set window properties
        root.title("AI Passport Photo Creator")
        root.geometry("1200x800")
        root.minsize(1000, 600)
        
        # Center the window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Start the main loop
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        messagebox.showerror("Application Error", f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
