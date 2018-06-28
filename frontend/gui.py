from tkinter import *
from tkinter import filedialog
from frontend.scene import MainScene, TestScene
import generator
import solver


class Application:

    def __init__(self):
        self.scenes = {}

        self.root = Tk()
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
        output_file = output_directory.get() + "/" + filename.get()
        input_file = input_file.get()
        print_path = print_path.get()
        paint_visited = paint_visited.get()
        solver.main(text_area, input_file, output_file, paint_visited, print_path)

    def generate(self, text_area: Text, width: Entry, height: Entry, output_directory: Entry, filename: Entry):
        try:
            width = int(width.get())
            height = int(height.get())
            output_file = output_directory.get() + "/" + filename.get()
            text_area.insert(END, "\nGenerating new maze:" +
                             "\n    Width: " + str(width) +
                             "\n    Height: " + str(height) +
                             "\n    Filename: " + str(output_file) +
                             "\nPlease wait ..."
                             "\n")
            generator.generate(width, height, output_file)
            text_area.insert(END, "Maze generation finished!\n")
        except FileNotFoundError as e:
            message = "\nERROR!: \n{}: {}\n"
            message = message.format(e.strerror, e.filename)
            text_area.insert(END, message)

    def browse_file(self, entry: Entry):
        previous = entry.get()
        entry.delete(0, END)
        filename = filedialog.askopenfilename()
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


if __name__ == "__main__":
    app = Application()
    app.root.mainloop()
