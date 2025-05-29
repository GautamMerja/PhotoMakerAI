"""
Application settings and configuration
"""

import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class Settings:
    """Application settings manager"""
    
    def __init__(self):
        self.settings_file = self._get_settings_file()
        self.default_settings = {
            "output_directory": str(Path.home() / "Documents" / "PassportPhotos"),
            "default_format": "US Passport",
            "default_background": "White",
            "default_layout": "2x2",
            "image_quality": 95,
            "auto_save": True,
            "auto_detect_faces": True,
            "window_width": 1200,
            "window_height": 800,
            "zoom_sensitivity": 1.1,
            "recent_files": [],
            "max_recent_files": 10
        }
        
        self.settings = self.load_settings()
    
    def _get_settings_file(self):
        """Get settings file path"""
        if os.name == 'nt':  # Windows
            config_dir = Path(os.environ.get('APPDATA', Path.home())) / "PassportPhotoCreator"
        else:  # Unix-like
            config_dir = Path.home() / ".config" / "PassportPhotoCreator"
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "settings.json"
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                
                # Merge with defaults
                settings = self.default_settings.copy()
                settings.update(loaded_settings)
                
                logger.info("Settings loaded successfully")
                return settings
            else:
                logger.info("No settings file found, using defaults")
                return self.default_settings.copy()
        
        except Exception as e:
            logger.error(f"Error loading settings: {str(e)}")
            return self.default_settings.copy()
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            logger.info("Settings saved successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error saving settings: {str(e)}")
            return False
    
    def get(self, key, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set setting value"""
        self.settings[key] = value
    
    def get_output_directory(self):
        """Get output directory, create if not exists"""
        output_dir = self.get("output_directory")
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    def set_output_directory(self, directory):
        """Set output directory"""
        self.set("output_directory", directory)
        self.save_settings()
    
    def get_default_format(self):
        """Get default passport format"""
        return self.get("default_format", "US Passport")
    
    def set_default_format(self, format_name):
        """Set default passport format"""
        self.set("default_format", format_name)
        self.save_settings()
    
    def get_default_background(self):
        """Get default background color"""
        return self.get("default_background", "White")
    
    def set_default_background(self, background):
        """Set default background color"""
        self.set("default_background", background)
        self.save_settings()
    
    def get_window_size(self):
        """Get window size"""
        width = self.get("window_width", 1200)
        height = self.get("window_height", 800)
        return width, height
    
    def set_window_size(self, width, height):
        """Set window size"""
        self.set("window_width", width)
        self.set("window_height", height)
        self.save_settings()
    
    def add_recent_file(self, file_path):
        """Add file to recent files list"""
        recent_files = self.get("recent_files", [])
        
        # Remove if already exists
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        # Add to beginning
        recent_files.insert(0, file_path)
        
        # Limit to max recent files
        max_files = self.get("max_recent_files", 10)
        recent_files = recent_files[:max_files]
        
        self.set("recent_files", recent_files)
        self.save_settings()
    
    def get_recent_files(self):
        """Get recent files list"""
        recent_files = self.get("recent_files", [])
        
        # Filter out non-existent files
        existing_files = [f for f in recent_files if os.path.exists(f)]
        
        if len(existing_files) != len(recent_files):
            self.set("recent_files", existing_files)
            self.save_settings()
        
        return existing_files
    
    def clear_recent_files(self):
        """Clear recent files list"""
        self.set("recent_files", [])
        self.save_settings()
    
    def get_image_quality(self):
        """Get image save quality"""
        return self.get("image_quality", 95)
    
    def set_image_quality(self, quality):
        """Set image save quality"""
        quality = max(1, min(100, quality))  # Clamp to 1-100
        self.set("image_quality", quality)
        self.save_settings()
    
    def is_auto_save_enabled(self):
        """Check if auto-save is enabled"""
        return self.get("auto_save", True)
    
    def set_auto_save(self, enabled):
        """Set auto-save enabled state"""
        self.set("auto_save", enabled)
        self.save_settings()
    
    def is_auto_detect_faces_enabled(self):
        """Check if auto face detection is enabled"""
        return self.get("auto_detect_faces", True)
    
    def set_auto_detect_faces(self, enabled):
        """Set auto face detection enabled state"""
        self.set("auto_detect_faces", enabled)
        self.save_settings()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.default_settings.copy()
        self.save_settings()
        logger.info("Settings reset to defaults")
    
    def export_settings(self, file_path):
        """Export settings to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Settings exported to {file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error exporting settings: {str(e)}")
            return False
    
    def import_settings(self, file_path):
        """Import settings from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            # Merge with current settings
            self.settings.update(imported_settings)
            self.save_settings()
            
            logger.info(f"Settings imported from {file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error importing settings: {str(e)}")
            return False
