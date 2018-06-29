from tkinter import *
from tkinter import filedialog
from scenes import MainScene, TestScene
import generator
import gui_solve


class Application:

    def __init__(self):
        self.scenes = {}

        self.root = Tk()
        self.root.title("Maze Solver 2000 TM")
        container = Frame(self.root)
        container.pack(side=TOP, fill=BOTH, expand=True)

        for s in (MainScene, TestScene):
            scene = s(master=container, controller=self)
            self.scenes[s] = scene
            scene.frame.grid(row=0, column=0, sticky=NSEW)

        self.set_scene(MainScene)

    def set_scene(self, scene_class):
        scene = self.scenes[scene_class]
        scene.frame.tkraise()

    def solve(self, text_area: Text, input_file: Entry, output_directory: Entry, filename: Entry,
              print_path: IntVar, paint_visited: IntVar):
        try:
            output_directory = output_directory.get()
            filename = filename.get()
            input_file = input_file.get()
            print_path = print_path.get()
            paint_visited = paint_visited.get()

            if input_file == "":
                raise UserError("Please specify input image before attempting solve")
            if output_directory == "":
                raise UserError("Please specify an output directory")
            if filename == "":
                raise UserError("Please specify an output filename")

            output_file = output_directory + "/" + filename
            if not output_file.endswith((".png", ".bmp")):
                output_file += ".png"
            gui_solve.main(text_area, input_file, output_file, paint_visited, print_path)

        except UserError as e:
            self.insert_text(text_area, "\n" + e.message)

    def generate(self, text_area: Text, width: Entry, height: Entry, output_directory: Entry, filename: Entry):
        try:
            output_directory = output_directory.get()
            filename = filename.get()
            width = width.get()
            height = height.get()
            if width == "":
                raise UserError("Please specify a width")
            if height == "":
                raise UserError("Please specify a height")
            if output_directory == "":
                raise UserError("Please specify an output directory")
            if filename == "":
                raise UserError("Please specify an output filename")
            width = int(width)
            height = int(height)
            output_file = output_directory + "/" + filename
            if not output_file.endswith((".png", ".bmp")):
                output_file += ".png"

            self.insert_text(text_area, "\nNote that the generated maze cannot be smaller than 3x3,"
                                        "\nand that width and height must be odd numbers."
                                        "\nEven numbers are incremented by 1\n")

            self.insert_text(text_area, "\nGenerating new maze:" +
                             "\n    Width: " + str(width) +
                             "\n    Height: " + str(height) +
                             "\n    Filename: " + str(output_file) +
                             "\nPlease wait ..."
                             "\n")
            text_area.see(END)
            generator.generate(width, height, output_file)
            self.insert_text(text_area, "\nMaze generation finished!\n")
            text_area.see(END)

        except FileNotFoundError as e:
            message = "\nERROR!: \n{}: {}\n"
            message = message.format(e.strerror, e.filename)
            self.insert_text(text_area, message)

        except UserError as e:
            self.insert_text(text_area, "\n" + e.message)

    def browse_file(self, entry: Entry):
        previous = entry.get()
        entry.delete(0, END)
        filename = filedialog.askopenfilename(filetypes=[("Image files", ".png")])
        if filename == () or filename == "":
            filename = previous
        entry.insert(0, filename)

    def browse_directory(self, entry: Entry):
        previous = entry.get()
        entry.delete(0, END)
        filename = filedialog.askdirectory()
        if filename == () or filename == "":
            filename = previous
        entry.insert(0, filename)

    def insert_text(self, text_area: Text, message: str):
        text_area.config(state='normal')
        text_area.insert(END, message)
        text_area.config(state='disabled')
        text_area.see(END)

    def clear_text(self, text_area: Text):
        text_area.config(state='normal')
        text_area.delete(1.0, END)
        text_area.config(state='disabled')
        text_area.see(END)


class UserError(Exception):

    def __init__(self, message):
        super().__init__()
        self.message = message


if __name__ == "__main__":
    app = Application()
    app.root.mainloop()
