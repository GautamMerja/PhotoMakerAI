"""
Common image processing utilities
"""

import os
import logging
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Image processing utilities class"""
    
    SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')
    
    @staticmethod
    def load_image(file_path):
        """
        Load image from file path
        
        Args:
            file_path (str): Path to image file
            
        Returns:
            PIL.Image: Loaded image
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Image file not found: {file_path}")
            
            # Check file extension
            ext = os.path.splitext(file_path)[1].lower()
            if ext not in ImageProcessor.SUPPORTED_FORMATS:
                raise ValueError(f"Unsupported file format: {ext}")
            
            image = Image.open(file_path)
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[-1])
                else:
                    background.paste(image, mask=image.split()[-1])
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            logger.info(f"Loaded image: {file_path} ({image.size})")
            return image
            
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            raise
    
    @staticmethod
    def save_image(image, file_path, quality=95, dpi=(300, 300)):
        """
        Save image to file
        
        Args:
            image (PIL.Image): Image to save
            file_path (str): Output file path
            quality (int): JPEG quality (1-100)
            dpi (tuple): DPI for saved image
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Determine format from file extension
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext in ('.jpg', '.jpeg'):
                # Convert to RGB if saving as JPEG
                if image.mode in ('RGBA', 'LA'):
                    rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = rgb_image
                
                image.save(file_path, 'JPEG', quality=quality, dpi=dpi, optimize=True)
            else:
                image.save(file_path, dpi=dpi, optimize=True)
            
            logger.info(f"Saved image: {file_path}")
            
        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            raise
    
    @staticmethod
    def resize_image(image, size, resample=Image.Resampling.LANCZOS):
        """
        Resize image to specified size
        
        Args:
            image (PIL.Image): Input image
            size (tuple): Target size (width, height)
            resample: Resampling algorithm
            
        Returns:
            PIL.Image: Resized image
        """
        try:
            resized_image = image.resize(size, resample)
            logger.info(f"Resized image from {image.size} to {size}")
            return resized_image
            
        except Exception as e:
            logger.error(f"Error resizing image: {str(e)}")
            return image
    
    @staticmethod
    def crop_to_ratio(image, ratio):
        """
        Crop image to specific aspect ratio
        
        Args:
            image (PIL.Image): Input image
            ratio (float): Target aspect ratio (width/height)
            
        Returns:
            PIL.Image: Cropped image
        """
        try:
            width, height = image.size
            current_ratio = width / height
            
            if current_ratio > ratio:
                # Image is too wide, crop sides
                new_width = int(height * ratio)
                left = (width - new_width) // 2
                cropped_image = image.crop((left, 0, left + new_width, height))
            else:
                # Image is too tall, crop top/bottom
                new_height = int(width / ratio)
                top = (height - new_height) // 2
                cropped_image = image.crop((0, top, width, top + new_height))
            
            logger.info(f"Cropped image to ratio {ratio:.2f}")
            return cropped_image
            
        except Exception as e:
            logger.error(f"Error cropping image: {str(e)}")
            return image
    
    @staticmethod
    def enhance_image(image, brightness=1.0, contrast=1.0, saturation=1.0, sharpness=1.0):
        """
        Enhance image properties
        
        Args:
            image (PIL.Image): Input image
            brightness (float): Brightness factor (1.0 = no change)
            contrast (float): Contrast factor (1.0 = no change)
            saturation (float): Saturation factor (1.0 = no change)
            sharpness (float): Sharpness factor (1.0 = no change)
            
        Returns:
            PIL.Image: Enhanced image
        """
        try:
            enhanced_image = image
            
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(enhanced_image)
                enhanced_image = enhancer.enhance(brightness)
            
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(enhanced_image)
                enhanced_image = enhancer.enhance(contrast)
            
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(enhanced_image)
                enhanced_image = enhancer.enhance(saturation)
            
            if sharpness != 1.0:
                enhancer = ImageEnhance.Sharpness(enhanced_image)
                enhanced_image = enhancer.enhance(sharpness)
            
            return enhanced_image
            
        except Exception as e:
            logger.error(f"Error enhancing image: {str(e)}")
            return image
    
    @staticmethod
    def apply_gaussian_blur(image, radius=1):
        """
        Apply Gaussian blur to image
        
        Args:
            image (PIL.Image): Input image
            radius (float): Blur radius
            
        Returns:
            PIL.Image: Blurred image
        """
        try:
            blurred_image = image.filter(ImageFilter.GaussianBlur(radius=radius))
            return blurred_image
            
        except Exception as e:
            logger.error(f"Error applying blur: {str(e)}")
            return image
    
    @staticmethod
    def get_next_filename(directory, base_name="passport_photo", extension=".jpg"):
        """
        Get next available filename with sequential numbering
        
        Args:
            directory (str): Output directory
            base_name (str): Base filename
            extension (str): File extension
            
        Returns:
            str: Next available filename
        """
        try:
            os.makedirs(directory, exist_ok=True)
            
            counter = 1
            while True:
                filename = f"{base_name}_{counter:03d}{extension}"
                file_path = os.path.join(directory, filename)
                
                if not os.path.exists(file_path):
                    return file_path
                
                counter += 1
                
                # Prevent infinite loop
                if counter > 9999:
                    raise ValueError("Too many files in directory")
            
        except Exception as e:
            logger.error(f"Error generating filename: {str(e)}")
            raise
    
    @staticmethod
    def create_thumbnail(image, size=(150, 150)):
        """
        Create thumbnail of image
        
        Args:
            image (PIL.Image): Input image
            size (tuple): Thumbnail size
            
        Returns:
            PIL.Image: Thumbnail image
        """
        try:
            thumbnail = image.copy()
            thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
            return thumbnail
            
        except Exception as e:
            logger.error(f"Error creating thumbnail: {str(e)}")
            return image
