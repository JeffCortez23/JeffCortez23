from PIL import Image
import sys

def image_to_ascii(image_path, width=40):
    img = Image.open(image_path)
    # Calculate height to maintain aspect ratio (Andrew's is approx 40 chars wide, 25 high)
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.5) # 0.5 because chars are taller than wide
    height = 25 # Force 25 lines to match template
    
    img = img.resize((width, height)).convert('L')
    
    # Andrew's style chars (from dark to light)
    chars = ["@", "%", "#", "*", "+", "=", "-", ":", ".", " "]
    
    ascii_str = ""
    for y in range(height):
        line = ""
        for x in range(width):
            pixel = img.getpixel((x, y))
            char = chars[pixel // 26] if pixel < 255 else " "
            line += char
        ascii_str += line + "\n"
    return ascii_str

image_path = "/home/elyefris/Downloads/Imágenes/renzo cortez.jpg"
ascii_art = image_to_ascii(image_path)
with open("user_ascii.txt", "w") as f:
    f.write(ascii_art)
