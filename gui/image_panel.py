"""
Image display panel component
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import logging

logger = logging.getLogger(__name__)

class ImagePanel(ttk.Frame):
    """Image display panel with zoom and pan capabilities"""
    
    def __init__(self, parent, title="Image"):
        super().__init__(parent)
        self.title = title
        self.current_image = None
        self.display_image_tk = None
        self.zoom_factor = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the panel UI"""
        # Title label
        title_label = ttk.Label(self, text=self.title, font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 5))
        
        # Create frame for canvas and scrollbars
        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=1, 
                               highlightbackground='gray')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Control frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Zoom controls
        ttk.Button(control_frame, text="Zoom In", command=self.zoom_in, width=10).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(control_frame, text="Zoom Out", command=self.zoom_out, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Fit", command=self.fit_to_window, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="100%", command=self.actual_size, width=10).pack(side=tk.LEFT, padx=2)
        
        # Zoom level label
        self.zoom_label = ttk.Label(control_frame, text="100%")
        self.zoom_label.pack(side=tk.RIGHT)
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)  # Linux
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)  # Linux
        
        # Variables for panning
        self.last_x = 0
        self.last_y = 0
    
    def display_image(self, image):
        """
        Display image in the panel
        
        Args:
            image (PIL.Image): Image to display
        """
        try:
            self.current_image = image.copy()
            self.zoom_factor = 1.0
            self.update_display()
            
            # Fit image to window initially
            self.fit_to_window()
            
            logger.info(f"Displayed image in {self.title} panel")
            
        except Exception as e:
            logger.error(f"Error displaying image: {str(e)}")
    
    def update_display(self):
        """Update the display with current zoom level"""
        if not self.current_image:
            return
        
        try:
            # Calculate display size
            original_width, original_height = self.current_image.size
            display_width = int(original_width * self.zoom_factor)
            display_height = int(original_height * self.zoom_factor)
            
            # Resize image for display
            if self.zoom_factor == 1.0:
                display_image = self.current_image
            else:
                display_image = self.current_image.resize(
                    (display_width, display_height), 
                    Image.Resampling.LANCZOS if self.zoom_factor > 1.0 else Image.Resampling.LANCZOS
                )
            
            # Convert to PhotoImage
            self.display_image_tk = ImageTk.PhotoImage(display_image)
            
            # Clear canvas and add image
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image_tk)
            
            # Update scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Update zoom label
            zoom_percent = int(self.zoom_factor * 100)
            self.zoom_label.config(text=f"{zoom_percent}%")
            
        except Exception as e:
            logger.error(f"Error updating display: {str(e)}")
    
    def zoom_in(self):
        """Zoom in on the image"""
        if self.zoom_factor < self.max_zoom:
            self.zoom_factor = min(self.zoom_factor * 1.2, self.max_zoom)
            self.update_display()
    
    def zoom_out(self):
        """Zoom out on the image"""
        if self.zoom_factor > self.min_zoom:
            self.zoom_factor = max(self.zoom_factor / 1.2, self.min_zoom)
            self.update_display()
    
    def fit_to_window(self):
        """Fit image to window size"""
        if not self.current_image:
            return
        
        try:
            # Get canvas size
            self.canvas.update_idletasks()
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                return
            
            # Calculate zoom factor to fit
            image_width, image_height = self.current_image.size
            
            zoom_x = canvas_width / image_width
            zoom_y = canvas_height / image_height
            
            self.zoom_factor = min(zoom_x, zoom_y)
            self.zoom_factor = max(self.min_zoom, min(self.zoom_factor, self.max_zoom))
            
            self.update_display()
            
        except Exception as e:
            logger.error(f"Error fitting to window: {str(e)}")
    
    def actual_size(self):
        """Display image at 100% zoom"""
        self.zoom_factor = 1.0
        self.update_display()
    
    def on_canvas_click(self, event):
        """Handle canvas click for panning"""
        self.canvas.scan_mark(event.x, event.y)
        self.last_x = event.x
        self.last_y = event.y
    
    def on_canvas_drag(self, event):
        """Handle canvas drag for panning"""
        self.canvas.scan_dragto(event.x, event.y, gain=1)
    
    def on_mouse_wheel(self, event):
        """Handle mouse wheel for zooming"""
        if not self.current_image:
            return
        
        # Determine zoom direction
        if event.delta > 0 or event.num == 4:
            # Zoom in
            if self.zoom_factor < self.max_zoom:
                old_zoom = self.zoom_factor
                self.zoom_factor = min(self.zoom_factor * 1.1, self.max_zoom)
                
                # Zoom towards mouse position
                self.zoom_at_point(event.x, event.y, old_zoom, self.zoom_factor)
        else:
            # Zoom out
            if self.zoom_factor > self.min_zoom:
                old_zoom = self.zoom_factor
                self.zoom_factor = max(self.zoom_factor / 1.1, self.min_zoom)
                
                # Zoom towards mouse position
                self.zoom_at_point(event.x, event.y, old_zoom, self.zoom_factor)
    
    def zoom_at_point(self, x, y, old_zoom, new_zoom):
        """Zoom towards a specific point"""
        try:
            # Get current scroll position
            x_scroll = self.canvas.canvasx(0)
            y_scroll = self.canvas.canvasy(0)
            
            # Calculate mouse position in image coordinates
            mouse_x = x_scroll + x
            mouse_y = y_scroll + y
            
            # Update display
            self.update_display()
            
            # Calculate new scroll position to keep mouse point in same place
            zoom_ratio = new_zoom / old_zoom
            new_mouse_x = mouse_x * zoom_ratio
            new_mouse_y = mouse_y * zoom_ratio
            
            new_x_scroll = new_mouse_x - x
            new_y_scroll = new_mouse_y - y
            
            # Update scroll position
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if self.display_image_tk:
                img_width = self.display_image_tk.width()
                img_height = self.display_image_tk.height()
                
                scroll_x = new_x_scroll / img_width if img_width > 0 else 0
                scroll_y = new_y_scroll / img_height if img_height > 0 else 0
                
                self.canvas.xview_moveto(max(0, min(1, scroll_x)))
                self.canvas.yview_moveto(max(0, min(1, scroll_y)))
        
        except Exception as e:
            logger.error(f"Error zooming at point: {str(e)}")
            self.update_display()
    
    def clear(self):
        """Clear the panel"""
        self.current_image = None
        self.display_image_tk = None
        self.zoom_factor = 1.0
        self.canvas.delete("all")
        self.zoom_label.config(text="100%")
    
    def get_image(self):
        """Get the current image"""
        return self.current_image
