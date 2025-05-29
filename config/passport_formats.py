"""
Passport photo format specifications
"""

class PassportFormats:
    """Passport photo format definitions and specifications"""
    
    def __init__(self):
        self.formats = {
            "US Passport": {
                "width_mm": 51,
                "height_mm": 51,
                "width_inch": 2.0,
                "height_inch": 2.0,
                "width_px": 600,
                "height_px": 600,
                "dpi": 300,
                "description": "US Passport photo - 2x2 inches"
            },
            "UK Passport": {
                "width_mm": 35,
                "height_mm": 45,
                "width_inch": 1.38,
                "height_inch": 1.77,
                "width_px": 413,
                "height_px": 531,
                "dpi": 300,
                "description": "UK Passport photo - 35x45mm"
            },
            "EU Passport": {
                "width_mm": 35,
                "height_mm": 45,
                "width_inch": 1.38,
                "height_inch": 1.77,
                "width_px": 413,
                "height_px": 531,
                "dpi": 300,
                "description": "EU Passport photo - 35x45mm"
            },
            "Canadian Passport": {
                "width_mm": 50,
                "height_mm": 70,
                "width_inch": 1.97,
                "height_inch": 2.76,
                "width_px": 591,
                "height_px": 827,
                "dpi": 300,
                "description": "Canadian Passport photo - 50x70mm"
            },
            "Australian Passport": {
                "width_mm": 35,
                "height_mm": 45,
                "width_inch": 1.38,
                "height_inch": 1.77,
                "width_px": 413,
                "height_px": 531,
                "dpi": 300,
                "description": "Australian Passport photo - 35x45mm"
            },
            "Indian Passport": {
                "width_mm": 35,
                "height_mm": 35,
                "width_inch": 1.38,
                "height_inch": 1.38,
                "width_px": 413,
                "height_px": 413,
                "dpi": 300,
                "description": "Indian Passport photo - 35x35mm"
            },
            "Chinese Passport": {
                "width_mm": 33,
                "height_mm": 48,
                "width_inch": 1.30,
                "height_inch": 1.89,
                "width_px": 390,
                "height_px": 567,
                "dpi": 300,
                "description": "Chinese Passport photo - 33x48mm"
            },
            "Japanese Passport": {
                "width_mm": 35,
                "height_mm": 45,
                "width_inch": 1.38,
                "height_inch": 1.77,
                "width_px": 413,
                "height_px": 531,
                "dpi": 300,
                "description": "Japanese Passport photo - 35x45mm"
            },
            "Brazilian Passport": {
                "width_mm": 30,
                "height_mm": 40,
                "width_inch": 1.18,
                "height_inch": 1.57,
                "width_px": 354,
                "height_px": 472,
                "dpi": 300,
                "description": "Brazilian Passport photo - 30x40mm"
            },
            "Mexican Passport": {
                "width_mm": 39,
                "height_mm": 31,
                "width_inch": 1.54,
                "height_inch": 1.22,
                "width_px": 461,
                "height_px": 366,
                "dpi": 300,
                "description": "Mexican Passport photo - 39x31mm"
            },
            "Russian Passport": {
                "width_mm": 35,
                "height_mm": 45,
                "width_inch": 1.38,
                "height_inch": 1.77,
                "width_px": 413,
                "height_px": 531,
                "dpi": 300,
                "description": "Russian Passport photo - 35x45mm"
            },
            "South African Passport": {
                "width_mm": 35,
                "height_mm": 45,
                "width_inch": 1.38,
                "height_inch": 1.77,
                "width_px": 413,
                "height_px": 531,
                "dpi": 300,
                "description": "South African Passport photo - 35x45mm"
            },
            "US Visa": {
                "width_mm": 51,
                "height_mm": 51,
                "width_inch": 2.0,
                "height_inch": 2.0,
                "width_px": 600,
                "height_px": 600,
                "dpi": 300,
                "description": "US Visa photo - 2x2 inches"
            },
            "Schengen Visa": {
                "width_mm": 35,
                "height_mm": 45,
                "width_inch": 1.38,
                "height_inch": 1.77,
                "width_px": 413,
                "height_px": 531,
                "dpi": 300,
                "description": "Schengen Visa photo - 35x45mm"
            },
            "ID Card": {
                "width_mm": 25,
                "height_mm": 35,
                "width_inch": 0.98,
                "height_inch": 1.38,
                "width_px": 295,
                "height_px": 413,
                "dpi": 300,
                "description": "Standard ID Card photo - 25x35mm"
            }
        }
    
    def get_format(self, format_name):
        """
        Get format specifications by name
        
        Args:
            format_name (str): Name of the format
            
        Returns:
            dict: Format specifications or None if not found
        """
        return self.formats.get(format_name)
    
    def get_all_format_names(self):
        """
        Get list of all available format names
        
        Returns:
            list: List of format names
        """
        return list(self.formats.keys())
    
    def get_formats_by_region(self, region):
        """
        Get formats by region
        
        Args:
            region (str): Region name (US, EU, Asia, etc.)
            
        Returns:
            dict: Filtered formats
        """
        region_mapping = {
            "US": ["US Passport", "US Visa"],
            "EU": ["UK Passport", "EU Passport", "Schengen Visa"],
            "Asia": ["Chinese Passport", "Japanese Passport", "Indian Passport"],
            "Americas": ["Canadian Passport", "Brazilian Passport", "Mexican Passport"],
            "Other": ["Australian Passport", "Russian Passport", "South African Passport", "ID Card"]
        }
        
        format_names = region_mapping.get(region, [])
        return {name: self.formats[name] for name in format_names if name in self.formats}
    
    def add_custom_format(self, name, width_mm, height_mm, dpi=300):
        """
        Add a custom format
        
        Args:
            name (str): Format name
            width_mm (float): Width in millimeters
            height_mm (float): Height in millimeters
            dpi (int): DPI resolution
        """
        # Convert mm to inches
        width_inch = width_mm / 25.4
        height_inch = height_mm / 25.4
        
        # Calculate pixels
        width_px = int(width_inch * dpi)
        height_px = int(height_inch * dpi)
        
        self.formats[name] = {
            "width_mm": width_mm,
            "height_mm": height_mm,
            "width_inch": width_inch,
            "height_inch": height_inch,
            "width_px": width_px,
            "height_px": height_px,
            "dpi": dpi,
            "description": f"Custom format - {width_mm}x{height_mm}mm"
        }
    
    def validate_format(self, format_specs):
        """
        Validate format specifications
        
        Args:
            format_specs (dict): Format specifications
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = ["width_mm", "height_mm", "width_px", "height_px", "dpi"]
        
        for field in required_fields:
            if field not in format_specs:
                return False
            
            if not isinstance(format_specs[field], (int, float)) or format_specs[field] <= 0:
                return False
        
        return True
    
    def get_print_sizes(self):
        """
        Get common print sizes for passport photos
        
        Returns:
            dict: Print size specifications
        """
        return {
            "Wallet Size": {
                "width_inch": 2.5,
                "height_inch": 3.5,
                "description": "Standard wallet size print"
            },
            "4x6 Print": {
                "width_inch": 4.0,
                "height_inch": 6.0,
                "description": "Standard 4x6 inch print"
            },
            "5x7 Print": {
                "width_inch": 5.0,
                "height_inch": 7.0,
                "description": "Standard 5x7 inch print"
            },
            "8x10 Print": {
                "width_inch": 8.0,
                "height_inch": 10.0,
                "description": "Standard 8x10 inch print"
            }
        }
