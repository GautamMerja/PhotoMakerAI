"""
Background removal utilities using rembg
"""

import logging
from PIL import Image
from rembg import remove, new_session
import io

logger = logging.getLogger(__name__)

class BackgroundRemover:
    """Background removal class using rembg"""
    
    def __init__(self, model_name='u2net'):
        """
        Initialize background remover
        
        Args:
            model_name (str): Model to use for background removal
        """
        self.model_name = model_name
        self.session = None
        self._initialize_session()
    
    def _initialize_session(self):
        """Initialize rembg session"""
        try:
            self.session = new_session(self.model_name)
            logger.info(f"Initialized rembg session with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error initializing rembg session: {str(e)}")
            self.session = None
    
    def remove_background(self, image):
        """
        Remove background from image
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            PIL.Image: Image with background removed (RGBA)
        """
        try:
            # Convert PIL image to bytes
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='PNG')
            image_bytes = image_bytes.getvalue()
            
            # Remove background
            if self.session:
                output_bytes = remove(image_bytes, session=self.session)
            else:
                output_bytes = remove(image_bytes)
            
            # Convert back to PIL Image
            output_image = Image.open(io.BytesIO(output_bytes))
            
            logger.info("Background removed successfully")
            return output_image
            
        except Exception as e:
            logger.error(f"Error removing background: {str(e)}")
            # Return original image with white background if removal fails
            return self._add_white_background(image)
    
    def _add_white_background(self, image):
        """
        Add white background to image
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            PIL.Image: Image with white background
        """
        try:
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Create white background
            white_bg = Image.new('RGBA', image.size, (255, 255, 255, 255))
            
            # Composite image onto white background
            result = Image.alpha_composite(white_bg, image)
            
            return result.convert('RGB')
            
        except Exception as e:
            logger.error(f"Error adding white background: {str(e)}")
            return image.convert('RGB')
    
    def add_colored_background(self, image, color=(255, 255, 255)):
        """
        Add colored background to transparent image
        
        Args:
            image (PIL.Image): Input image (should be RGBA)
            color (tuple): RGB color tuple for background
            
        Returns:
            PIL.Image: Image with colored background
        """
        try:
            if image.mode != 'RGBA':
                logger.warning("Image is not in RGBA mode, converting...")
                image = image.convert('RGBA')
            
            # Create colored background
            colored_bg = Image.new('RGBA', image.size, color + (255,))
            
            # Composite image onto colored background
            result = Image.alpha_composite(colored_bg, image)
            
            return result.convert('RGB')
            
        except Exception as e:
            logger.error(f"Error adding colored background: {str(e)}")
            return image.convert('RGB')
    
    def get_background_colors(self):
        """
        Get available background colors for passport photos
        
        Returns:
            dict: Dictionary of color names and RGB values
        """
        return {
            'White': (255, 255, 255),
            'Light Blue': (173, 216, 230),
            'Light Gray': (211, 211, 211),
            'Off White': (248, 248, 255),
            'Cream': (255, 253, 208)
        }
    
    def apply_background_color(self, image, color_name='White'):
        """
        Apply specific background color to image
        
        Args:
            image (PIL.Image): Input image with transparent background
            color_name (str): Name of background color
            
        Returns:
            PIL.Image: Image with specified background color
        """
        colors = self.get_background_colors()
        
        if color_name not in colors:
            logger.warning(f"Color '{color_name}' not available, using white")
            color_name = 'White'
        
        color = colors[color_name]
        return self.add_colored_background(image, color)
