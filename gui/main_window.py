"""
Main application window
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import threading
from PIL import Image, ImageTk

from gui.image_panel import ImagePanel
from gui.control_panel import ControlPanel
from utils.face_utils import FaceDetector
from utils.background_utils import BackgroundRemover
from utils.passport_utils import PassportPhotoFormatter
from utils.image_utils import ImageProcessor
from utils.print_utils import PrintManager
from config.settings import Settings

logger = logging.getLogger(__name__)

class PassportPhotoApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.settings = Settings()
        
        # Initialize components
        self.face_detector = FaceDetector()
        self.bg_remover = BackgroundRemover()
        self.passport_formatter = PassportPhotoFormatter()
        self.print_manager = PrintManager()
        
        # Application state
        self.current_image = None
        self.processed_image = None
        self.passport_image = None
        self.face_locations = []
        self.face_landmarks = []
        
        # Setup GUI
        self.setup_gui()
        self.setup_menu()
        
        logger.info("Application initialized")
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Configure root window
        self.root.configure(bg='#f0f0f0')
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left panel for images
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Create right panel for controls
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # Setup image panels
        self.setup_image_panels(left_frame)
        
        # Setup control panel
        self.control_panel = ControlPanel(right_frame, self)
        
        # Setup status bar
        self.setup_status_bar()
    
    def setup_image_panels(self, parent):
        """Setup image display panels"""
        # Create notebook for tabbed image display
        self.image_notebook = ttk.Notebook(parent)
        self.image_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Original image panel
        self.original_panel = ImagePanel(self.image_notebook, "Original Image")
        self.image_notebook.add(self.original_panel, text="Original")
        
        # Processed image panel
        self.processed_panel = ImagePanel(self.image_notebook, "Processed Image")
        self.image_notebook.add(self.processed_panel, text="Processed")
        
        # Passport photo panel
        self.passport_panel = ImagePanel(self.image_notebook, "Passport Photo")
        self.image_notebook.add(self.passport_panel, text="Passport")
    
    def setup_menu(self):
        """Setup application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image...", command=self.open_image, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save Passport Photo...", command=self.save_passport_photo, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Print...", command=self.print_image, accelerator="Ctrl+P")
        file_menu.add_command(label="Print Preview", command=self.print_preview)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Process menu
        process_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Process", menu=process_menu)
        process_menu.add_command(label="Detect Faces", command=self.detect_faces)
        process_menu.add_command(label="Remove Background", command=self.remove_background)
        process_menu.add_command(label="Format as Passport Photo", command=self.format_passport_photo)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_image())
        self.root.bind('<Control-s>', lambda e: self.save_passport_photo())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_as())
        self.root.bind('<Control-p>', lambda e: self.print_image())
    
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        self.progress_bar = ttk.Progressbar(self.status_frame, mode='indeterminate')
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def show_progress(self, show=True):
        """Show/hide progress bar"""
        if show:
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
    
    def open_image(self):
        """Open image file dialog"""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=file_types
        )
        
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, file_path):
        """Load image from file path"""
        try:
            self.update_status("Loading image...")
            self.show_progress(True)
            
            # Load image
            self.current_image = ImageProcessor.load_image(file_path)
            
            # Display in original panel
            self.original_panel.display_image(self.current_image)
            
            # Reset other panels
            self.processed_panel.clear()
            self.passport_panel.clear()
            
            # Reset state
            self.processed_image = None
            self.passport_image = None
            self.face_locations = []
            self.face_landmarks = []
            
            # Update control panel
            self.control_panel.on_image_loaded()
            
            self.update_status(f"Loaded: {file_path}")
            
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
            self.update_status("Error loading image")
        finally:
            self.show_progress(False)
    
    def detect_faces(self):
        """Detect faces in current image"""
        if not self.current_image:
            messagebox.showwarning("No Image", "Please load an image first.")
            return
        
        try:
            self.update_status("Detecting faces...")
            self.show_progress(True)
            
            # Run face detection in thread
            def detect_thread():
                try:
                    # Save current image temporarily
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                        self.current_image.save(temp_file.name, 'JPEG')
                        temp_path = temp_file.name
                    
                    # Detect faces
                    self.face_locations, self.face_landmarks, _ = self.face_detector.detect_faces(temp_path)
                    
                    # Clean up temp file
                    import os
                    os.unlink(temp_path)
                    
                    # Update UI in main thread
                    self.root.after(0, self.on_faces_detected)
                    
                except Exception as e:
                    logger.error(f"Error in face detection thread: {str(e)}")
                    self.root.after(0, lambda: self.on_face_detection_error(str(e)))
            
            threading.Thread(target=detect_thread, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Error starting face detection: {str(e)}")
            messagebox.showerror("Error", f"Failed to detect faces:\n{str(e)}")
            self.update_status("Face detection failed")
            self.show_progress(False)
    
    def on_faces_detected(self):
        """Handle face detection completion"""
        try:
            # Highlight faces in image
            highlighted_image = self.face_detector.highlight_faces(self.current_image, self.face_locations)
            
            # Display in processed panel
            self.processed_panel.display_image(highlighted_image)
            self.processed_image = highlighted_image
            
            # Switch to processed tab
            self.image_notebook.select(1)
            
            # Update control panel
            self.control_panel.on_faces_detected(len(self.face_locations))
            
            self.update_status(f"Detected {len(self.face_locations)} face(s)")
            
        except Exception as e:
            logger.error(f"Error processing face detection results: {str(e)}")
            self.update_status("Error processing faces")
        finally:
            self.show_progress(False)
    
    def on_face_detection_error(self, error_msg):
        """Handle face detection error"""
        messagebox.showerror("Face Detection Error", f"Failed to detect faces:\n{error_msg}")
        self.update_status("Face detection failed")
        self.show_progress(False)
    
    def remove_background(self):
        """Remove background from current image"""
        if not self.current_image:
            messagebox.showwarning("No Image", "Please load an image first.")
            return
        
        try:
            self.update_status("Removing background...")
            self.show_progress(True)
            
            # Run background removal in thread
            def remove_bg_thread():
                try:
                    # Remove background
                    bg_removed_image = self.bg_remover.remove_background(self.current_image)
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self.on_background_removed(bg_removed_image))
                    
                except Exception as e:
                    logger.error(f"Error in background removal thread: {str(e)}")
                    self.root.after(0, lambda: self.on_background_removal_error(str(e)))
            
            threading.Thread(target=remove_bg_thread, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Error starting background removal: {str(e)}")
            messagebox.showerror("Error", f"Failed to remove background:\n{str(e)}")
            self.update_status("Background removal failed")
            self.show_progress(False)
    
    def on_background_removed(self, bg_removed_image):
        """Handle background removal completion"""
        try:
            # Apply selected background color
            bg_color = self.control_panel.get_background_color()
            self.processed_image = self.bg_remover.apply_background_color(bg_removed_image, bg_color)
            
            # Display in processed panel
            self.processed_panel.display_image(self.processed_image)
            
            # Switch to processed tab
            self.image_notebook.select(1)
            
            # Update control panel
            self.control_panel.on_background_removed()
            
            self.update_status("Background removed successfully")
            
        except Exception as e:
            logger.error(f"Error processing background removal results: {str(e)}")
            self.update_status("Error processing background removal")
        finally:
            self.show_progress(False)
    
    def on_background_removal_error(self, error_msg):
        """Handle background removal error"""
        messagebox.showerror("Background Removal Error", f"Failed to remove background:\n{error_msg}")
        self.update_status("Background removal failed")
        self.show_progress(False)
    
    def format_passport_photo(self):
        """Format image as passport photo"""
        source_image = self.processed_image if self.processed_image else self.current_image
        
        if not source_image:
            messagebox.showwarning("No Image", "Please load an image first.")
            return
        
        try:
            self.update_status("Formatting passport photo...")
            self.show_progress(True)
            
            # Get format and face percentage from control panel
            format_name = self.control_panel.get_passport_format()
            face_percentage = self.control_panel.get_face_percentage()
            
            # Use first face location if available
            face_location = self.face_locations[0] if self.face_locations else None
            
            # Format passport photo
            self.passport_image = self.passport_formatter.format_passport_photo(
                source_image, format_name, face_location, face_percentage
            )
            
            # Display in passport panel
            self.passport_panel.display_image(self.passport_image)
            
            # Switch to passport tab
            self.image_notebook.select(2)
            
            # Update control panel
            self.control_panel.on_passport_formatted()
            
            self.update_status(f"Formatted as {format_name} passport photo")
            
        except Exception as e:
            logger.error(f"Error formatting passport photo: {str(e)}")
            messagebox.showerror("Error", f"Failed to format passport photo:\n{str(e)}")
            self.update_status("Passport formatting failed")
        finally:
            self.show_progress(False)
    
    def save_passport_photo(self):
        """Save passport photo with auto-numbering"""
        if not self.passport_image:
            messagebox.showwarning("No Passport Photo", "Please format a passport photo first.")
            return
        
        try:
            # Get next available filename
            output_dir = self.settings.get_output_directory()
            file_path = ImageProcessor.get_next_filename(output_dir, "passport_photo", ".jpg")
            
            # Save image
            ImageProcessor.save_image(self.passport_image, file_path, quality=95, dpi=(300, 300))
            
            messagebox.showinfo("Saved", f"Passport photo saved as:\n{file_path}")
            self.update_status(f"Saved: {file_path}")
            
        except Exception as e:
            logger.error(f"Error saving passport photo: {str(e)}")
            messagebox.showerror("Error", f"Failed to save passport photo:\n{str(e)}")
    
    def save_as(self):
        """Save passport photo with custom filename"""
        if not self.passport_image:
            messagebox.showwarning("No Passport Photo", "Please format a passport photo first.")
            return
        
        file_types = [
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.asksaveasfilename(
            title="Save Passport Photo",
            defaultextension=".jpg",
            filetypes=file_types
        )
        
        if file_path:
            try:
                ImageProcessor.save_image(self.passport_image, file_path, quality=95, dpi=(300, 300))
                messagebox.showinfo("Saved", f"Passport photo saved as:\n{file_path}")
                self.update_status(f"Saved: {file_path}")
            except Exception as e:
                logger.error(f"Error saving passport photo: {str(e)}")
                messagebox.showerror("Error", f"Failed to save passport photo:\n{str(e)}")
    
    def print_image(self):
        """Print passport photo"""
        if not self.passport_image:
            messagebox.showwarning("No Passport Photo", "Please format a passport photo first.")
            return
        
        try:
            # Get print layout
            layout_type = self.control_panel.get_print_layout()
            print_image = self.passport_formatter.create_print_layout(self.passport_image, layout_type)
            
            # Get selected printer
            printer_name = self.control_panel.get_selected_printer()
            
            # Print image
            success = self.print_manager.print_image(print_image, printer_name)
            
            if success:
                messagebox.showinfo("Print", "Print job sent successfully!")
                self.update_status("Print job sent")
            else:
                messagebox.showerror("Print Error", "Failed to send print job.")
                self.update_status("Print failed")
        
        except Exception as e:
            logger.error(f"Error printing: {str(e)}")
            messagebox.showerror("Error", f"Failed to print:\n{str(e)}")
    
    def print_preview(self):
        """Show print preview"""
        if not self.passport_image:
            messagebox.showwarning("No Passport Photo", "Please format a passport photo first.")
            return
        
        try:
            layout_type = self.control_panel.get_print_layout()
            print_image = self.passport_formatter.create_print_layout(self.passport_image, layout_type)
            
            self.print_manager.show_print_preview(print_image)
            self.update_status("Print preview opened")
            
        except Exception as e:
            logger.error(f"Error showing print preview: {str(e)}")
            messagebox.showerror("Error", f"Failed to show print preview:\n{str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """AI Passport Photo Creator
        
A desktop application for creating professional passport photos with AI-powered features:

• Face detection and alignment
• Background removal
• Passport photo formatting
• Direct printing support
• Auto-save with sequential numbering

Built with Python, Tkinter, and computer vision libraries.
        """
        
        messagebox.showinfo("About", about_text)
