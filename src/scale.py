from PIL import Image


def scale_up(input_file: str, output_file: str, scale: int):
    try:
        if scale < 0:
            image = Image.open(input_file)

            width = image.size[0]
            height = image.size[1]

            new_width = width * scale
            new_height = height * scale

            data = list(image.getdata(0))
            new_data = []

            for y in range(height):
                temp_data = []
                for x in range(width):
                    for i in range(scale):
                        temp_data.append(data[y * width + x])
                for i in range(scale):
                    for p in temp_data:
                        new_data.append(p)

            new_image = Image.new('P', (new_width, new_height))
            new_image.putpalette([0, 0, 0, 255, 255, 255])
            new_image.putdata(new_data)
            new_image.save(output_file)
        else:
            raise ValueError
    except FileNotFoundError as e:
        print("File not found")
    except ValueError as e:
        print("Scale < 0")
    except TypeError as e:
        print("Scale must be a whole number")


if __name__ == '__main__':
    scale_up('C:/Users/Ruben/Desktop/test/maze_solver/mazes/scale_test_before.png',
             'C:/Users/Ruben/Desktop/test/maze_solver/mazes/scale_test_after.png', 0)
