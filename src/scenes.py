from tkinter import *


class MainScene:

    def __init__(self, master, controller):
        self.frame = Frame(master)
        left_frame = Frame(self.frame)
        right_frame = Frame(self.frame)

        left_frame.pack(side=LEFT, fill=Y)
        right_frame.pack(side=RIGHT, fill=Y)

        # Labels
        label_solve = Label(left_frame, text="--- Solve ---")
        label_input_file = Label(left_frame, text="Input file:")
        label_output_directory_s = Label(left_frame, text="Output Folder")
        label_filename_s = Label(left_frame, text="Filename:")

        label_generate = Label(left_frame, text="--- Generate ---")
        label_width = Label(left_frame, text="Width:")
        label_height = Label(left_frame, text="Height:")
        label_output_directory_g = Label(left_frame, text="Output Folder:")
        label_filename_g = Label(left_frame, text="Filename:")
        label_method = Label(left_frame, text="Method:")

        # Entries
        entry_input_file = Entry(left_frame)
        entry_output_directory_s = Entry(left_frame)
        entry_filename_s = Entry(left_frame)

        vcmd_integer = (master.register(self.validate_integer),
                        '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        entry_width = Entry(left_frame, validate='key', validatecommand=vcmd_integer)
        entry_height = Entry(left_frame, validate='key', validatecommand=vcmd_integer)
        entry_output_directory_g = Entry(left_frame)
        entry_filename_g = Entry(left_frame)

        method_var = StringVar()
        method_var.set("braid")  # default value

        menu_method = OptionMenu(left_frame, method_var, "braid", "perfect")

        # Check boxes
        print_path_var = IntVar()
        paint_visited_var = IntVar()
        paint_visited = Checkbutton(left_frame, text="Paint visited", variable=paint_visited_var)
        print_path = Checkbutton(left_frame, text="Print path", variable=print_path_var)

        # Console area
        scrollbar_y = Scrollbar(right_frame, orient=VERTICAL)
        text_area = Text(right_frame, height=25, width=80, state='disabled')
        scrollbar_y.config(command=text_area.yview)
        text_area.config(yscrollcommand=scrollbar_y.set)
        clear_button = Button(right_frame, text="Clear",
                              command=lambda: controller.clear_text(text_area))

        text_area.pack(side=LEFT, fill=Y)
        scrollbar_y.pack(side=LEFT, fill=Y)
        clear_button.pack(side=BOTTOM)

        # Buttons
        solve_button = Button(left_frame, text="Solve",
                              command=lambda: controller.solve(text_area, entry_input_file, entry_output_directory_s,
                                                               entry_filename_s, print_path_var, paint_visited_var))

        generate_button = Button(left_frame, text="Generate",
                                 command=lambda: controller.generate(text_area, entry_width, entry_height,
                                                                     entry_output_directory_g, entry_filename_g,
                                                                     method_var))

        browse_for_input = Button(left_frame, text="...", font=('Tahoma', 8),
                                  command=lambda: controller.browse_file(entry_input_file))

        browse_for_output_s = Button(left_frame, text="...", font=('Tahoma', 8),
                                     command=lambda: controller.browse_directory(entry_output_directory_s))

        browse_for_output_g = Button(left_frame, text="...", font=('Tahoma', 8),
                                     command=lambda: controller.browse_directory(entry_output_directory_g))

        # Grid locations
        label_solve.grid(row=0, column=0, columnspan=3)
        label_input_file.grid(row=1, column=0, sticky=E)
        label_output_directory_s.grid(row=2, column=0, sticky=E)
        label_filename_s.grid(row=3, column=0, sticky=E)
        entry_input_file.grid(row=1, column=1, sticky=E)
        entry_output_directory_s.grid(row=2, column=1, sticky=E)
        entry_filename_s.grid(row=3, column=1, sticky=E)
        browse_for_input.grid(row=1, column=2, sticky=W)
        browse_for_output_s.grid(row=2, column=2, sticky=W)
        paint_visited.grid(row=4, column=1, sticky=W)
        print_path.grid(row=5, column=1, sticky=W)
        solve_button.grid(row=4, column=1, sticky=E, columnspan=2)

        label_generate.grid(row=6, column=0, columnspan=3)
        label_width.grid(row=7, column=0, sticky=E)
        label_height.grid(row=8, column=0, sticky=E)
        label_output_directory_g.grid(row=9, column=0, sticky=E)
        label_filename_g.grid(row=10, column=0, sticky=E)
        label_method.grid(row=11, column=0, sticky=E)
        entry_width.grid(row=7, column=1, sticky=E)
        entry_height.grid(row=8, column=1, sticky=E)
        entry_output_directory_g.grid(row=9, column=1, sticky=E)
        entry_filename_g.grid(row=10, column=1, sticky=E)
        menu_method.grid(row=11, column=1, sticky=W)
        browse_for_output_g.grid(row=9, column=2, sticky=W)
        generate_button.grid(row=11, column=1, sticky=E, columnspan=2)

    def validate_integer(self, action, index, value_if_allowed,
                         prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.-+':
            try:
                if not value_if_allowed == "":
                    int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False


class TestScene:

    def __init__(self, master, controller):
        self.frame = Frame(master)
        label = Label(self.frame, text="Test Scene!")
        label.pack()
