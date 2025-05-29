"""
Printing utilities for passport photos
"""

import os
import sys
import logging
import tempfile
from PIL import Image

logger = logging.getLogger(__name__)

class PrintManager:
    """Print management class"""
    
    def __init__(self):
        self.available_printers = []
        self._detect_printers()
    
    def _detect_printers(self):
        """Detect available printers on the system"""
        try:
            if sys.platform == "win32":
                self._detect_windows_printers()
            elif sys.platform == "darwin":
                self._detect_mac_printers()
            else:
                self._detect_linux_printers()
        except Exception as e:
            logger.error(f"Error detecting printers: {str(e)}")
    
    def _detect_windows_printers(self):
        """Detect Windows printers"""
        try:
            import win32print
            printers = win32print.EnumPrinters(2)
            self.available_printers = [printer[2] for printer in printers]
            logger.info(f"Found {len(self.available_printers)} Windows printers")
        except ImportError:
            logger.warning("win32print not available, using default printer detection")
            self.available_printers = ["Default Printer"]
        except Exception as e:
            logger.error(f"Error detecting Windows printers: {str(e)}")
            self.available_printers = ["Default Printer"]
    
    def _detect_mac_printers(self):
        """Detect macOS printers"""
        try:
            import subprocess
            result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                self.available_printers = [line.split()[1] for line in lines if line.startswith('printer')]
            else:
                self.available_printers = ["Default Printer"]
            logger.info(f"Found {len(self.available_printers)} macOS printers")
        except Exception as e:
            logger.error(f"Error detecting macOS printers: {str(e)}")
            self.available_printers = ["Default Printer"]
    
    def _detect_linux_printers(self):
        """Detect Linux printers"""
        try:
            import subprocess
            result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                self.available_printers = [line.split()[1] for line in lines if line.startswith('printer')]
            else:
                self.available_printers = ["Default Printer"]
            logger.info(f"Found {len(self.available_printers)} Linux printers")
        except Exception as e:
            logger.error(f"Error detecting Linux printers: {str(e)}")
            self.available_printers = ["Default Printer"]
    
    def get_available_printers(self):
        """Get list of available printers"""
        return self.available_printers
    
    def print_image(self, image, printer_name=None, copies=1, paper_size="4x6"):
        """
        Print image to specified printer
        
        Args:
            image (PIL.Image): Image to print
            printer_name (str): Printer name (None for default)
            copies (int): Number of copies
            paper_size (str): Paper size
            
        Returns:
            bool: True if print job was successful
        """
        try:
            # Save image to temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                image.save(temp_file.name, 'PNG', dpi=(300, 300))
                temp_path = temp_file.name
            
            try:
                if sys.platform == "win32":
                    success = self._print_windows(temp_path, printer_name, copies, paper_size)
                elif sys.platform == "darwin":
                    success = self._print_mac(temp_path, printer_name, copies, paper_size)
                else:
                    success = self._print_linux(temp_path, printer_name, copies, paper_size)
                
                return success
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_path)
                except:
                    pass
            
        except Exception as e:
            logger.error(f"Error printing image: {str(e)}")
            return False
    
    def _print_windows(self, file_path, printer_name, copies, paper_size):
        """Print on Windows"""
        try:
            import win32api
            import win32print
            
            if printer_name is None:
                printer_name = win32print.GetDefaultPrinter()
            
            # Print the file
            win32api.ShellExecute(
                0,
                "print",
                file_path,
                f'/d:"{printer_name}"',
                ".",
                0
            )
            
            logger.info(f"Sent print job to {printer_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error printing on Windows: {str(e)}")
            return self._fallback_print(file_path)
    
    def _print_mac(self, file_path, printer_name, copies, paper_size):
        """Print on macOS"""
        try:
            import subprocess
            
            cmd = ['lpr']
            
            if printer_name:
                cmd.extend(['-P', printer_name])
            
            cmd.extend(['-#', str(copies)])
            cmd.append(file_path)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Sent print job to printer")
                return True
            else:
                logger.error(f"Print command failed: {result.stderr}")
                return False
            
        except Exception as e:
            logger.error(f"Error printing on macOS: {str(e)}")
            return self._fallback_print(file_path)
    
    def _print_linux(self, file_path, printer_name, copies, paper_size):
        """Print on Linux"""
        try:
            import subprocess
            
            cmd = ['lpr']
            
            if printer_name:
                cmd.extend(['-P', printer_name])
            
            cmd.extend(['-#', str(copies)])
            cmd.append(file_path)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Sent print job to printer")
                return True
            else:
                logger.error(f"Print command failed: {result.stderr}")
                return False
            
        except Exception as e:
            logger.error(f"Error printing on Linux: {str(e)}")
            return self._fallback_print(file_path)
    
    def _fallback_print(self, file_path):
        """Fallback print method - open system print dialog"""
        try:
            import subprocess
            import webbrowser
            
            if sys.platform == "win32":
                os.startfile(file_path, "print")
            elif sys.platform == "darwin":
                subprocess.run(["open", "-a", "Preview", file_path])
            else:
                # Try to open with default image viewer
                subprocess.run(["xdg-open", file_path])
            
            logger.info("Opened file with system default application for printing")
            return True
            
        except Exception as e:
            logger.error(f"Fallback print method failed: {str(e)}")
            return False
    
    def show_print_preview(self, image):
        """
        Show print preview of image
        
        Args:
            image (PIL.Image): Image to preview
        """
        try:
            # Create a copy for preview
            preview_image = image.copy()
            
            # Add print guidelines/margins
            from PIL import ImageDraw
            draw = ImageDraw.Draw(preview_image)
            
            width, height = preview_image.size
            margin = 20
            
            # Draw margin lines
            draw.rectangle([margin, margin, width-margin, height-margin], 
                         outline="gray", width=2)
            
            # Save to temp file and show
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                preview_image.save(temp_file.name, 'PNG')
                
                if sys.platform == "win32":
                    os.startfile(temp_file.name)
                elif sys.platform == "darwin":
                    import subprocess
                    subprocess.run(["open", temp_file.name])
                else:
                    import subprocess
                    subprocess.run(["xdg-open", temp_file.name])
            
            logger.info("Opened print preview")
            
        except Exception as e:
            logger.error(f"Error showing print preview: {str(e)}")
