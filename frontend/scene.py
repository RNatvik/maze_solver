from tkinter import *


class MainScene:

    def __init__(self):
        self.main_frame = Frame()
        left_frame = Frame(self.main_frame)
        right_frame = Frame(self.main_frame)

        left_frame.pack(side=LEFT, fill=Y)
        right_frame.pack(side=RIGHT, fill=Y)

        # Labels
        label_solve = Label(left_frame, text="--- Solve ---")
        label_input_file = Label(left_frame, text="Input file:")
        label_output_file = Label(left_frame, text="Output file:")

        label_generate = Label(left_frame, text="--- Generate ---")
        label_width = Label(left_frame, text="Width:")
        label_height = Label(left_frame, text="Height:")
        label_output_file_g = Label(left_frame, text="Output file:")

        # Entries
        self.entry_input_file = Entry(left_frame)
        self.entry_output_file_s = Entry(left_frame)

        self.entry_width = Entry(left_frame)
        self.entry_height = Entry(left_frame)
        self.entry_output_file_g = Entry(left_frame)

        # Buttons
        solve_button = Button(left_frame, text="Solve")
        generate_button = Button(left_frame, text="Generate")
        browse_for_input = Button(left_frame, text="...", font=('Tahoma', 8))
        browse_for_output = Button(left_frame, text="...", font=('Tahoma', 8))
        browse_for_output_g = Button(left_frame, text="...", font=('Tahoma', 8))

        # Check boxes
        self.show_visited = Checkbutton(left_frame, text="Show visited")
        self.print_path = Checkbutton(left_frame, text="Print path")

        # Grid locations
        label_solve.grid(row=0, column=0, columnspan=3)
        label_input_file.grid(row=1, column=0, sticky=E)
        label_output_file.grid(row=2, column=0, sticky=E)
        self.entry_input_file.grid(row=1, column=1, sticky=E)
        self.entry_output_file_s.grid(row=2, column=1, sticky=E)
        browse_for_input.grid(row=1, column=2, sticky=W)
        browse_for_output.grid(row=2, column=2, sticky=W)
        self.show_visited.grid(row=3, column=1, sticky=W)
        self.print_path.grid(row=4, column=1, sticky=W)
        solve_button.grid(row=3, column=1, sticky=E, columnspan=2)

        label_generate.grid(row=6, column=0, columnspan=3)
        label_width.grid(row=7, column=0, sticky=E)
        label_height.grid(row=8, column=0, sticky=E)
        label_output_file_g.grid(row=9, column=0, sticky=E)
        self.entry_width.grid(row=7, column=1, sticky=E)
        self.entry_height.grid(row=8, column=1, sticky=E)
        self.entry_output_file_g.grid(row=9, column=1, sticky=E)
        browse_for_output_g.grid(row=9, column=2, sticky=W)
        generate_button.grid(row=10, column=1, sticky=E, columnspan=2)

        # Console area
        scrollbar_y = Scrollbar(right_frame, orient=VERTICAL)
        text_area = Text(right_frame, height=25, width=60)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        text_area.pack(side=LEFT, fill=Y)
        scrollbar_y.config(command=text_area.yview)
        text_area.config(yscrollcommand=scrollbar_y.set)

