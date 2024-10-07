from PIL import Image
from collections import defaultdict

def count_all_colors(image_path):
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size

    color_count = defaultdict(int)
    for x in range(width):
        for y in range(height):
            color_count[pixels[x, y]] += 1

    return color_count

if __name__ == "__main__":
    image_path = "map/T.png"
    color_count = count_all_colors(image_path)
    for color, count in color_count.items():
        print(f"The color {color} appears {count} times in the image.")
    if color == (237, 28, 36, 255):
        print("Find the color (237, 28, 36, 255) in the image. count: ", count)