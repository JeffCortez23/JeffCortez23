from PIL import Image, ImageEnhance, ImageOps
import sys

def convert_photo_to_ascii(image_path, width=40, height=35):
    # Load image
    img = Image.open(image_path)
    
    # Auto-orient the image (if it has EXIF rotation tags)
    img = ImageOps.exif_transpose(img)
    
    # Convert to grayscale
    img_gray = img.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img_gray)
    img_contrast = enhancer.enhance(1.6)
    
    # Enhance sharpness
    sharpness = ImageEnhance.Sharpness(img_contrast)
    img_sharp = sharpness.enhance(1.5)
    
    # Resize to target width and height
    img_resized = img_sharp.resize((width, height), Image.Resampling.LANCZOS)
    
    # ASCII character ramp (from dark to light)
    # Simple, high-contrast ramp that renders extremely well in SVGs
    chars = ["@", "%", "#", "*", "+", "=", "-", ":", ".", " "]
    
    ascii_rows = []
    for y in range(height):
        row = ""
        for x in range(width):
            pixel = img_resized.getpixel((x, y))
            # Map pixel values (0-255) to character list index (0-9)
            idx = min(int(pixel / 25.6), len(chars) - 1)
            row += chars[idx]
        ascii_rows.append(row)
        
    return ascii_rows

if __name__ == '__main__':
    img_path = "/home/elyefris/.gemini/antigravity/brain/badd9b7d-9449-4d6c-a8cc-604a9ee6a84d/media__1779309636416.jpg"
    print(f"Generating ASCII for {img_path}...")
    
    # Let's try 40x35 as it matches the aspect ratio of the portrait image
    rows = convert_photo_to_ascii(img_path, width=40, height=35)
    
    # Print preview
    for row in rows:
        print(row)
        
    # Also write to user_ascii_preview.txt
    with open("user_ascii_preview.txt", "w") as f:
        for row in rows:
            f.write(row + "\n")
            
    print("\nSaved preview to user_ascii_preview.txt")
