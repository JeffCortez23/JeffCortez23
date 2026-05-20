from PIL import Image, ImageEnhance, ImageOps
import sys

def convert_photo_to_ascii(image_path, width=40, height=35):
    # Load image
    img = Image.open(image_path)
    
    # Auto-orient the image (if it has EXIF rotation tags)
    img = ImageOps.exif_transpose(img)
    
    # Convert to grayscale
    img_gray = img.convert('L')
    
    # Enhance contrast (Optimized Option 4: 1.4)
    enhancer = ImageEnhance.Contrast(img_gray)
    img_contrast = enhancer.enhance(1.4)
    
    # Enhance sharpness (Optimized Option 4: 1.2)
    sharpness = ImageEnhance.Sharpness(img_contrast)
    img_sharp = sharpness.enhance(1.2)
    
    # Resize to target width and height
    img_resized = img_sharp.resize((width, height), Image.Resampling.LANCZOS)
    
    # Sigmoid thresholding ramp with 100% transparent background (spaces)
    bg_thresh = 130
    ramps = [45, 80, 110]
    
    ascii_rows = []
    for y in range(height):
        row = ""
        for x in range(width):
            pixel = img_resized.getpixel((x, y))
            if pixel > bg_thresh:
                row += " "
            elif pixel < ramps[0]:
                row += "@"
            elif pixel < ramps[1]:
                row += "#"
            elif pixel < ramps[2]:
                row += "*"
            else:
                row += "-"
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
