"""
Passport photo formatting utilities
"""

import logging
from PIL import Image, ImageDraw
from config.passport_formats import PassportFormats

logger = logging.getLogger(__name__)

class PassportPhotoFormatter:
    """Passport photo formatting class"""
    
    def __init__(self):
        self.formats = PassportFormats()
    
    def format_passport_photo(self, image, format_name, face_location=None, face_percentage=65.0):
        """
        Format image as passport photo
        
        Args:
            image (PIL.Image): Input image
            format_name (str): Passport format name
            face_location (tuple): Face location for alignment
            face_percentage (float): Percentage of photo height the face should occupy
            
        Returns:
            PIL.Image: Formatted passport photo
        """
        try:
            format_specs = self.formats.get_format(format_name)
            if not format_specs:
                raise ValueError(f"Unknown passport format: {format_name}")
            
            # Get dimensions in pixels
            width_px = format_specs['width_px']
            height_px = format_specs['height_px']
            
            # Crop to correct aspect ratio first
            target_ratio = width_px / height_px
            cropped_image = self._crop_to_passport_ratio(image, target_ratio, face_location, face_percentage)
            
            # Resize to exact dimensions
            formatted_image = cropped_image.resize((width_px, height_px), Image.Resampling.LANCZOS)
            
            # Apply passport photo guidelines
            formatted_image = self._apply_passport_guidelines(formatted_image, format_specs)
            
            logger.info(f"Formatted image for {format_name} passport photo with {face_percentage}% face size")
            return formatted_image
            
        except Exception as e:
            logger.error(f"Error formatting passport photo: {str(e)}")
            raise
    
    def _crop_to_passport_ratio(self, image, target_ratio, face_location=None, face_percentage=65.0):
        """
        Crop image to passport photo ratio with face percentage positioning
        
        Args:
            image (PIL.Image): Input image
            target_ratio (float): Target aspect ratio
            face_location (tuple): Face location (top, right, bottom, left)
            face_percentage (float): Percentage of photo height the face should occupy
            
        Returns:
            PIL.Image: Cropped image
        """
        try:
            width, height = image.size
            current_ratio = width / height
            
            if face_location:
                # Use face location to guide cropping with proper face positioning
                top, right, bottom, left = face_location
                face_center_x = (left + right) // 2
                face_center_y = (top + bottom) // 2
                face_width = right - left
                face_height = bottom - top
                
                if current_ratio > target_ratio:
                    # Image is too wide, crop sides around face
                    new_width = int(height * target_ratio)
                    
                    # Center crop around face horizontally
                    left_crop = max(0, min(face_center_x - new_width // 2, width - new_width))
                    cropped_image = image.crop((left_crop, 0, left_crop + new_width, height))
                else:
                    # Image is too tall, crop top/bottom with face positioned properly
                    new_height = int(width / target_ratio)
                    
                    # Use the face percentage parameter from user input
                    desired_face_height_percentage = face_percentage / 100.0  # Convert percentage to decimal
                    desired_face_top_percentage = 0.25  # Face starts at 25% from top
                    
                    # Calculate desired face dimensions in new crop
                    desired_face_height_in_crop = new_height * desired_face_height_percentage
                    scale_factor = desired_face_height_in_crop / face_height
                    
                    # If face needs to be scaled, adjust crop size accordingly
                    if scale_factor < 1:
                        # Face is too big, need to include more area
                        new_height = int(face_height / desired_face_height_percentage)
                        new_height = min(new_height, height)  # Don't exceed original height
                    
                    # Position crop so face is at desired location
                    desired_face_top_in_crop = new_height * desired_face_top_percentage
                    top_crop = max(0, min(face_center_y - int(desired_face_top_in_crop + face_height/2), 
                                         height - new_height))
                    
                    cropped_image = image.crop((0, top_crop, width, top_crop + new_height))
            else:
                # Standard center crop when no face detected
                if current_ratio > target_ratio:
                    new_width = int(height * target_ratio)
                    left_crop = (width - new_width) // 2
                    cropped_image = image.crop((left_crop, 0, left_crop + new_width, height))
                else:
                    new_height = int(width / target_ratio)
                    top_crop = (height - new_height) // 2
                    cropped_image = image.crop((0, top_crop, width, top_crop + new_height))
            
            return cropped_image
            
        except Exception as e:
            logger.error(f"Error cropping to passport ratio: {str(e)}")
            return image
    
    def _apply_passport_guidelines(self, image, format_specs):
        """
        Apply passport photo guidelines (brightness, contrast, etc.)
        
        Args:
            image (PIL.Image): Input image
            format_specs (dict): Format specifications
            
        Returns:
            PIL.Image: Enhanced image
        """
        try:
            # Apply standard enhancements for passport photos
            from utils.image_utils import ImageProcessor
            
            enhanced_image = ImageProcessor.enhance_image(
                image,
                brightness=1.05,  # Slightly brighter
                contrast=1.1,     # Slightly more contrast
                saturation=0.95,  # Slightly less saturation
                sharpness=1.1     # Slightly sharper
            )
            
            return enhanced_image
            
        except Exception as e:
            logger.error(f"Error applying passport guidelines: {str(e)}")
            return image
    
    def create_print_layout(self, passport_image, layout_type="2x2"):
        """
        Create print layout with multiple passport photos
        
        Args:
            passport_image (PIL.Image): Single passport photo
            layout_type (str): Layout type ("2x2", "4x6", etc.)
            
        Returns:
            PIL.Image: Print layout image
        """
        try:
            layouts = {
                "2x2": {"grid": (2, 2), "size": (600, 600), "spacing": 10},
                "4x6": {"grid": (4, 6), "size": (1200, 1800), "spacing": 15},
                "wallet": {"grid": (2, 4), "size": (600, 900), "spacing": 10}
            }
            
            if layout_type not in layouts:
                layout_type = "2x2"
            
            layout = layouts[layout_type]
            grid_cols, grid_rows = layout["grid"]
            layout_size = layout["size"]
            spacing = layout["spacing"]
            
            # Calculate photo size within layout
            photo_width = (layout_size[0] - (spacing * (grid_cols + 1))) // grid_cols
            photo_height = (layout_size[1] - (spacing * (grid_rows + 1))) // grid_rows
            
            # Resize passport photo to fit layout
            resized_photo = passport_image.resize((photo_width, photo_height), Image.Resampling.LANCZOS)
            
            # Create layout image
            layout_image = Image.new('RGB', layout_size, 'white')
            
            # Place photos in grid
            for row in range(grid_rows):
                for col in range(grid_cols):
                    x = spacing + col * (photo_width + spacing)
                    y = spacing + row * (photo_height + spacing)
                    layout_image.paste(resized_photo, (x, y))
            
            logger.info(f"Created {layout_type} print layout")
            return layout_image
            
        except Exception as e:
            logger.error(f"Error creating print layout: {str(e)}")
            return passport_image
    
    def get_available_formats(self):
        """
        Get list of available passport photo formats
        
        Returns:
            list: List of format names
        """
        return self.formats.get_all_format_names()
    
    def get_format_info(self, format_name):
        """
        Get information about a specific format
        
        Args:
            format_name (str): Format name
            
        Returns:
            dict: Format specifications
        """
        return self.formats.get_format(format_name)
