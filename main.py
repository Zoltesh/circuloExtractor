"""
@author: Zoltesh
"""
import tkinter.filedialog
import customtkinter
from pathlib import Path
import Processor


class App(customtkinter.CTk):
    def __init__(self):
        # The result after running the run_button_function
        self.run_result = {'input_folder_path': "", 'output_folder_path': ""}
        self.BUTTON_SETTINGS = {'width': 100, 'font_and_size': ("Calibri", 18), 'anchor': 'center'}
        super().__init__()

        # Draw window
        self.default_window_size = "600x250"
        self.geometry(self.default_window_size)
        # Launch window in center of the screen
        self.eval('tk::PlaceWindow . center')
        self.title("Credit Report Summary")
        # Lock window to 600x250
        self.minsize(600, 250)
        self.maxsize(600, 250)

        # create 5x3 grid system
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # Title label
        self.title_label = customtkinter.CTkLabel(master=self, text="Credit Report Summary", anchor='center',
                                                  font=("Calibri", 24))
        self.title_label.grid(row=0, column=0, padx=10, columnspan=3)

        # ------------------------------------- Input Widgets ----------------------------------------------------------
        # Input folder title
        self.input_folder_label = customtkinter.CTkLabel(master=self, text="Select folder to process:",
                                                         font=("Calibri", 16))
        self.input_folder_label.grid(row=1, column=0, padx=10, sticky='w')
        # Input textfield for the input folder
        self.input_folder_textfield = customtkinter.CTkEntry(master=self, placeholder_text="Enter Input Folder Path",
                                                             font=("Calibri", 14), text_color="#EEEEEE")
        self.input_folder_textfield.grid(row=2, column=0, padx=10, sticky='ew', columnspan=2)

        # Browse button for the input folder
        self.input_browse_button = customtkinter.CTkButton(master=self, text="Browse",
                                                           anchor=self.BUTTON_SETTINGS['anchor'],
                                                           font=(self.BUTTON_SETTINGS['font_and_size']),
                                                           width=self.BUTTON_SETTINGS['width'],
                                                           command=self.browse_input
                                                           )
        self.input_browse_button.grid(row=2, column=2, columnspan=1, sticky='w')
        # --------------------------------------------------------------------------------------------------------------
        # ------------------------------------- Output Widgets ---------------------------------------------------------
        # Output folder title
        self.output_folder_label = customtkinter.CTkLabel(master=self, text="Destination folder:", anchor='w',
                                                          font=("Calibri", 16))
        self.output_folder_label.grid(row=3, column=0, padx=10, sticky='w')
        # Output textfield for the output folder
        self.output_folder_textfield = customtkinter.CTkEntry(master=self, placeholder_text="Enter Output Folder Path",
                                                              font=("Calibri", 14), text_color="#EEEEEE")
        self.output_folder_textfield.grid(row=4, column=0, pady=0, padx=10, columnspan=2, sticky='ew')

        # Browse button for the output folder
        self.output_browse_button = customtkinter.CTkButton(master=self, text="Browse",
                                                            anchor=self.BUTTON_SETTINGS['anchor'],
                                                            font=(self.BUTTON_SETTINGS['font_and_size']),
                                                            width=self.BUTTON_SETTINGS['width'],
                                                            command=self.browse_output
                                                            )
        self.output_browse_button.grid(row=4, column=2, columnspan=1, sticky='w')
        # --------------------------------------------------------------------------------------------------------------
        # ------------------------------------- Run Widgets ------------------------------------------------------------
        self.run_button = customtkinter.CTkButton(master=self, text="Run", anchor=self.BUTTON_SETTINGS['anchor'],
                                                  font=(self.BUTTON_SETTINGS['font_and_size']),
                                                  width=self.BUTTON_SETTINGS['width'], command=self.run_button_function
                                                  )
        self.run_button.grid(row=5, column=0, padx=10, pady=20, columnspan=2, sticky='e')
        # --------------------------------------------------------------------------------------------------------------
        # ------------------------------------- Run Widgets ------------------------------------------------------------
        self.exit_button = customtkinter.CTkButton(master=self, text="Exit", anchor=self.BUTTON_SETTINGS['anchor'],
                                                   font=(self.BUTTON_SETTINGS['font_and_size']),
                                                   width=self.BUTTON_SETTINGS['width'],
                                                   command=self.exit_button_function
                                                   )
        self.exit_button.grid(row=5, column=2, pady=20, columnspan=1, sticky='w')
        # --------------------------------------------------------------------------------------------------------------

    # -------------------------------------- Functions -------------------------------------------------------------
    # Method to obtain all files inside the chosen directory
    def browse_input(self):
        # Directory for the input folder
        input_folder = tkinter.filedialog.askdirectory()
        input_folder.join(input_folder)
        files = []
        # Get all files inside the chosen directory and append to list of files
        self.input_folder_textfield.delete(0, "end")
        self.input_folder_textfield.insert(0, input_folder)

    # Browse output button calls the browse_output method to prompt user for output directory
    def browse_output(self):
        # Directory for the output folder
        output_folder = tkinter.filedialog.askdirectory()
        output_folder.join(output_folder)

        # Set the output_folder_textfield to the output_folder path
        self.output_folder_textfield.delete(0, "end")
        self.output_folder_textfield.insert(0, output_folder)

    def run_button_function(self):
        text_fields = {'input_folder_path': self.input_folder_textfield,
                       'output_folder_path': self.output_folder_textfield}
        # If the textfields are not empty or invalid, set the run_result to the valid path
        for key, value in text_fields.items():
            text = value.get().split('\n')[0]  # Get the text field value
            if text:
                if Path(text).is_dir():
                    print(f"{key} folder is valid!")
                    self.run_result[key] = text  # Set the valid path to run_result
                else:
                    print(f"{key} folder is invalid!")
                    self.run_result[key] = ""  # Clear the run_result value for this field
            else:
                print(f"{key} folder cannot be empty!")
                self.run_result[key] = ""  # Clear the run_result value for this field

        # Check if both input and output folder paths are valid
        if all(path for path in self.run_result.values()):
            input_folder = self.run_result['input_folder_path']
            output_folder = self.run_result['output_folder_path']

            # Call the process_all_pdfs function with the input and output folders
            Processor.process_all_pdfs(input_folder, output_folder)
        else:
            print("Please provide valid input and output folder paths.")

    def exit_button_function(self):
        self.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()
