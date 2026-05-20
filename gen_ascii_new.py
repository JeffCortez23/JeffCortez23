from PIL import Image, ImageEnhance
import sys

def image_to_ascii(image_path, width=40):
    img = Image.open(image_path)
    # Enhance contrast to make features (glasses, eyes) pop
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    # Calculate height to maintain aspect ratio
    aspect_ratio = img.height / img.width
    height = 25 # Force 25 lines to match SVG template
    
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

image_path = "/home/elyefris/Downloads/Imágenes/unnamed (1).jpg"
ascii_art = image_to_ascii(image_path)
with open("user_ascii.txt", "w") as f:
    f.write(ascii_art)
print(ascii_art)
