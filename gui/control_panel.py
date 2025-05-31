"""
Control panel component for application controls
"""

import tkinter as tk
from tkinter import ttk
import logging

logger = logging.getLogger(__name__)

class ControlPanel(ttk.Frame):
    """Control panel for passport photo processing"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)
        
        self.setup_ui()
        self.load_initial_data()
    
    def setup_ui(self):
        """Setup the control panel UI"""
        # Title
        title_label = ttk.Label(self, text="Controls", font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # File operations section
        self.create_file_section()
        
        # Image processing section
        self.create_processing_section()
        
        # Background section
        self.create_background_section()
        
        # Passport format section
        self.create_passport_section()
        
        # Print section
        self.create_print_section()
        
        # Status section
        self.create_status_section()
    
    def create_file_section(self):
        """Create file operations section"""
        file_frame = ttk.LabelFrame(self, text="File Operations", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(file_frame, text="Open Image", command=self.app.open_image, width=20).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="Save Passport Photo", command=self.app.save_passport_photo, width=20).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="Save As...", command=self.app.save_as, width=20).pack(fill=tk.X, pady=2)
    
    def create_processing_section(self):
        """Create image processing section"""
        process_frame = ttk.LabelFrame(self, text="Image Processing", padding=10)
        process_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(process_frame, text="Detect Faces", command=self.app.detect_faces, width=20).pack(fill=tk.X, pady=2)
        
        # Face detection status
        self.face_status_label = ttk.Label(process_frame, text="No faces detected", foreground="gray")
        self.face_status_label.pack(fill=tk.X, pady=2)
        
        ttk.Button(process_frame, text="Remove Background", command=self.app.remove_background, width=20).pack(fill=tk.X, pady=2)
    
    def create_background_section(self):
        """Create background options section"""
        bg_frame = ttk.LabelFrame(self, text="Background Color", padding=10)
        bg_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Background color selection
        ttk.Label(bg_frame, text="Select Background:").pack(fill=tk.X)
        
        self.bg_color_var = tk.StringVar(value="White")
        self.bg_color_combo = ttk.Combobox(bg_frame, textvariable=self.bg_color_var, 
                                          state="readonly", width=18)
        self.bg_color_combo.pack(fill=tk.X, pady=2)
        
        # Load background colors
        bg_colors = self.app.bg_remover.get_background_colors()
        self.bg_color_combo['values'] = list(bg_colors.keys())
    
    def create_passport_section(self):
        """Create passport format section"""
        passport_frame = ttk.LabelFrame(self, text="Passport Format", padding=10)
        passport_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Format selection
        ttk.Label(passport_frame, text="Photo Format:").pack(fill=tk.X)
        
        self.format_var = tk.StringVar(value="US Passport")
        self.format_combo = ttk.Combobox(passport_frame, textvariable=self.format_var, 
                                        state="readonly", width=18)
        self.format_combo.pack(fill=tk.X, pady=2)
        
        # Face percentage control
        ttk.Label(passport_frame, text="Face Size (%):").pack(fill=tk.X, pady=(5, 0))
        
        face_frame = ttk.Frame(passport_frame)
        face_frame.pack(fill=tk.X, pady=2)
        
        self.face_percentage_var = tk.DoubleVar(value=65.0)
        self.face_percentage_scale = ttk.Scale(face_frame, from_=50.0, to=80.0, 
                                             variable=self.face_percentage_var, 
                                             orient=tk.HORIZONTAL)
        self.face_percentage_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.face_percentage_label = ttk.Label(face_frame, text="65%", width=5)
        self.face_percentage_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Update label when scale changes
        self.face_percentage_scale.bind("<Motion>", self.on_face_percentage_changed)
        self.face_percentage_scale.bind("<ButtonRelease-1>", self.on_face_percentage_changed)
        
        # Format passport photo button
        ttk.Button(passport_frame, text="Format Photo", command=self.app.format_passport_photo, width=20).pack(fill=tk.X, pady=2)
        
        # Format info
        self.format_info_label = ttk.Label(passport_frame, text="", foreground="blue", font=('Arial', 8))
        self.format_info_label.pack(fill=tk.X, pady=2)
        
        # Bind format selection change
        self.format_combo.bind('<<ComboboxSelected>>', self.on_format_changed)
    
    def create_print_section(self):
        """Create print options section"""
        print_frame = ttk.LabelFrame(self, text="Print Options", padding=10)
        print_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Print layout
        ttk.Label(print_frame, text="Print Layout:").pack(fill=tk.X)
        
        self.layout_var = tk.StringVar(value="2x2")
        layout_combo = ttk.Combobox(print_frame, textvariable=self.layout_var, 
                                   state="readonly", width=18)
        layout_combo['values'] = ["2x2", "4x6", "wallet"]
        layout_combo.pack(fill=tk.X, pady=2)
        
        # Printer selection
        ttk.Label(print_frame, text="Printer:").pack(fill=tk.X, pady=(5, 0))
        
        self.printer_var = tk.StringVar()
        self.printer_combo = ttk.Combobox(print_frame, textvariable=self.printer_var, 
                                         state="readonly", width=18)
        self.printer_combo.pack(fill=tk.X, pady=2)
        
        # Print buttons
        ttk.Button(print_frame, text="Print Preview", command=self.app.print_preview, width=20).pack(fill=tk.X, pady=2)
        ttk.Button(print_frame, text="Print", command=self.app.print_image, width=20).pack(fill=tk.X, pady=2)
    
    def create_status_section(self):
        """Create status section"""
        status_frame = ttk.LabelFrame(self, text="Status", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.processing_status_label = ttk.Label(status_frame, text="Ready", foreground="green")
        self.processing_status_label.pack(fill=tk.X)
    
    def load_initial_data(self):
        """Load initial data for comboboxes"""
        # Load passport formats
        formats = self.app.passport_formatter.get_available_formats()
        self.format_combo['values'] = formats
        if formats:
            self.format_var.set(formats[0])
            self.on_format_changed()
        
        # Load printers
        printers = self.app.print_manager.get_available_printers()
        self.printer_combo['values'] = printers
        if printers:
            self.printer_var.set(printers[0])
    
    def on_format_changed(self, event=None):
        """Handle passport format selection change"""
        format_name = self.format_var.get()
        format_info = self.app.passport_formatter.get_format_info(format_name)
        
        if format_info:
            info_text = f"{format_info['width_mm']}x{format_info['height_mm']}mm, {format_info['dpi']} DPI"
            self.format_info_label.config(text=info_text)
    
    def on_face_percentage_changed(self, event=None):
        """Handle face percentage scale change"""
        percentage = int(self.face_percentage_var.get())
        self.face_percentage_label.config(text=f"{percentage}%")
    
    def on_image_loaded(self):
        """Handle image loaded event"""
        self.processing_status_label.config(text="Image loaded", foreground="blue")
        self.face_status_label.config(text="No faces detected", foreground="gray")
    
    def on_faces_detected(self, face_count):
        """Handle faces detected event"""
        if face_count > 0:
            self.face_status_label.config(text=f"{face_count} face(s) detected", foreground="green")
            self.processing_status_label.config(text="Faces detected", foreground="green")
        else:
            self.face_status_label.config(text="No faces detected", foreground="orange")
            self.processing_status_label.config(text="No faces found", foreground="orange")
    
    def on_background_removed(self):
        """Handle background removed event"""
        self.processing_status_label.config(text="Background removed", foreground="green")
    
    def on_passport_formatted(self):
        """Handle passport photo formatted event"""
        self.processing_status_label.config(text="Passport photo ready", foreground="green")
    
    def get_background_color(self):
        """Get selected background color"""
        return self.bg_color_var.get()
    
    def get_passport_format(self):
        """Get selected passport format"""
        return self.format_var.get()
    
    def get_print_layout(self):
        """Get selected print layout"""
        return self.layout_var.get()
    
    def get_selected_printer(self):
        """Get selected printer"""
        return self.printer_var.get() if self.printer_var.get() else None
    
    def get_face_percentage(self):
        """Get selected face percentage"""
        return self.face_percentage_var.get()
