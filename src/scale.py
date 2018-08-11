from PIL import Image


def scale_up(input_file: str, output_file: str, scale: int):
    try:
        if scale >= 1:
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
        print("Error: File not found")
    except ValueError as e:
        print("Error: Scale < 1")
    except TypeError as e:
        print("Error: Scale must be a whole number")