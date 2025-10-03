# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from Models.text_model import TextModel
from Models.image_model import ImageModel
from oop_explanations import explanations

class App(tk.Tk):
    """
    Main application class for the Tkinter AI GUI.
    Provides interface for loading and running text and image models.
    Inherits from tk.Tk to create the main window.
    """
    
    def __init__(self):
        """
        Initialize the application window and all GUI components.
        Sets up models, creates menu bar, input/output sections, and information displays.
        """
        super().__init__()
        self.title("Tkinter AI GUI")
        self.geometry("800x600")

        # Initialize AI models for text and image processing
        self.text_model = TextModel()
        self.image_model = ImageModel()

        # ===== Menu =====
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # ===== Model Selection =====
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Model Selection:").pack(side="left")
        self.model_choice = tk.StringVar(value="Text")
        self.dropdown = tk.OptionMenu(top_frame, self.model_choice, "Text", "Image")
        self.dropdown.pack(side="left", padx=5)

        tk.Button(top_frame, text="Load Model", command=self.load_model).pack(side="left")

        # ===== User Input Section =====
        self.input_frame = tk.LabelFrame(self, text="User Input Section")
        self.input_frame.pack(fill="x", padx=10, pady=5)

        # Radio button container
        radio_container = tk.Frame(self.input_frame)
        radio_container.pack(anchor="w", padx=5, pady=5)

        self.input_type = tk.StringVar(value="Text")
        
        # Create radio buttons dynamically using a loop
        radio_options = ["Text", "Image"]
        for option in radio_options:
            tk.Radiobutton(
                radio_container, 
                text=option, 
                variable=self.input_type, 
                value=option,
                command=self.update_input_section  # Dynamic update on selection
            ).pack(side="left", padx=5)

        # Container for dynamic input widgets
        self.dynamic_input_container = tk.Frame(self.input_frame)
        self.dynamic_input_container.pack(fill="x", padx=5, pady=5)

        # Initialize input widgets (will be shown/hidden dynamically)
        self.text_input_entry = None
        self.browse_button = None
        self.file_path_label = None

        # Create initial input section based on default selection
        self.update_input_section()

        # ===== Model Output Section =====
        output_frame = tk.LabelFrame(self, text="Model Output Section")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.output_display = tk.Text(output_frame, height=6, wrap="word")
        self.output_display.pack(fill="both", expand=True)

        # ===== Buttons =====
        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)
        
        # Create buttons dynamically using a loop (demonstrates effective loop usage)
        button_configs = [
            ("Run Text Model", self.run_text_model),
            ("Run Image Model", self.run_image_model),
            ("Clear", self.clear_output)
        ]
        
        for button_text, button_command in button_configs:
            tk.Button(
                button_frame, 
                text=button_text, 
                command=button_command
            ).pack(side="left", padx=5)

        # ===== Info & Explanations =====
        info_frame = tk.LabelFrame(self, text="Model Information & Explanation")
        info_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Configure grid: 2 columns, each takes 50% width
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)

        # Left side: Model Info
        self.model_info_var = tk.StringVar()
        self.model_info = tk.Label(
            info_frame, textvariable=self.model_info_var,
            justify="left", anchor="nw", wraplength=350
        )
        self.model_info.grid(row=0, column=0, sticky="nw", padx=10, pady=5)

        # Right side: OOP Explanations with Scrollbar
        oop_frame = tk.Frame(info_frame)
        oop_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        # Text widget for displaying OOP explanations
        self.oop_info = tk.Text(
            oop_frame, wrap="word", height=15, width=50
        )
        self.oop_info.insert("1.0", explanations)
        self.oop_info.config(state="disabled")  # Make it read-only to prevent editing
        self.oop_info.pack(side="left", fill="both", expand=True)

        # Scrollbar for OOP explanations
        scrollbar = tk.Scrollbar(oop_frame, command=self.oop_info.yview)
        scrollbar.pack(side="right", fill="y")
        self.oop_info.config(yscrollcommand=scrollbar.set)

    # ===== Functions =====
    def update_input_section(self):
        """
        Dynamically update the input section based on selected input type.
        Shows text entry field for Text input, or browse button for Image input.
        This provides better UX by only displaying relevant input controls.
        """
        # Clear all existing widgets in the dynamic container
        for widget in self.dynamic_input_container.winfo_children():
            widget.destroy()

        input_type = self.input_type.get()

        if input_type == "Text":
            # Create text input field for text model
            tk.Label(
                self.dynamic_input_container, 
                text="Enter your text:"
            ).pack(side="left", padx=5)
            
            self.text_input_entry = tk.Entry(
                self.dynamic_input_container, 
                width=60
            )
            self.text_input_entry.pack(side="left", padx=5, fill="x", expand=True)

        elif input_type == "Image":
            # Create browse button and file path display for image model
            self.browse_button = tk.Button(
                self.dynamic_input_container, 
                text="Browse Image File", 
                command=self.browse_file,
                width=15
            )
            self.browse_button.pack(side="left", padx=5)
            
            self.file_path_label = tk.Label(
                self.dynamic_input_container, 
                text="No file selected", 
                anchor="w",
                relief="sunken",
                bg="white"
            )
            self.file_path_label.pack(side="left", padx=5, fill="x", expand=True)

    def load_model(self):
        """
        Load the selected model and display its information.
        Retrieves model metadata (name, category, description) and updates the info display.
        Uses dynamic attribute retrieval to build the information text.
        """
        choice = self.model_choice.get()
        # Select the appropriate model based on user's choice
        model = self.text_model if choice == "Text" else self.image_model

        # Build model information dynamically using a loop
        info_lines = ["Selected Model Info:"]
        attributes = [
            ('model_name', 'Model Name'),
            ('category', 'Category'),
            ('description', 'Description')
        ]
        
        # Loop through attributes and retrieve their values from the model
        for attr_name, display_name in attributes:
            if hasattr(model, attr_name):
                value = getattr(model, attr_name)
                info_lines.append(f"• {display_name}: {value}")
        
        # Join all lines and update the display
        self.model_info_var.set('\n'.join(info_lines))

    def browse_file(self):
        """
        Open a file dialog for the user to select an image file.
        Updates the file path label with the selected file path.
        Supports common image formats.
        """
        file_path = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            # Update the label to show the selected file path
            self.file_path_label.config(text=file_path)

    def run_text_model(self):
        """
        Execute the text model with user-provided text input.
        Validates that text input type is selected and input is not empty.
        Displays the model's output in the output section.
        """
        # Validate that the correct input type is selected
        if self.input_type.get() != "Text":
            self.output_display.insert(tk.END, "⚠ Please select 'Text' input type first.\n")
            return

        # Get text from the text input entry field
        if not self.text_input_entry:
            self.output_display.insert(tk.END, "⚠ Text input field not available.\n")
            return
            
        text = self.text_input_entry.get()
        
        # Validate that input is not empty or just whitespace
        if not text or all(char.isspace() for char in text):
            self.output_display.insert(tk.END, "⚠ Please enter valid text.\n")
            return

        # Run the model and display the result
        result = self.text_model.run(text)
        self.output_display.insert(tk.END, f"✓ Text Model Output: {result}\n")

    def run_image_model(self):
        """
        Execute the image model with a user-selected image file.
        Validates that image input type is selected and a file path is provided.
        Displays the model's output in the output section.
        """
        # Validate that the correct input type is selected
        if self.input_type.get() != "Image":
            self.output_display.insert(tk.END, "Please select 'Image' input type first.\n")
            return

        # Get file path from the label
        if not self.file_path_label:
            self.output_display.insert(tk.END, "File path label not available.\n")
            return
            
        file_path = self.file_path_label.cget("text")
        
        # Validate that a file has been selected
        if file_path == "No file selected" or not file_path:
            self.output_display.insert(tk.END, "Please select an image file first.\n")
            return

        # Run the model and display the result
        result = self.image_model.run(file_path)
        self.output_display.insert(tk.END, f" Image Model Output: {result}\n")

    def clear_output(self):
        """
        Clear all text from the output display area.
        Removes all previous model outputs to provide a clean slate.
        """
        self.output_display.delete("1.0", tk.END)