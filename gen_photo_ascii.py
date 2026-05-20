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
    img_contrast = enhancer.enhance(1.3)
    
    # Enhance sharpness
    sharpness = ImageEnhance.Sharpness(img_contrast)
    img_sharp = sharpness.enhance(1.3)
    
    # Resize to target width and height
    img_resized = img_sharp.resize((width, height), Image.Resampling.LANCZOS)
    
    # 1. Flood fill to find contiguous background starting from borders
    bg_mask = [[False for _ in range(width)] for _ in range(height)]
    bg_threshold = 120
    
    # Seeds for BFS: all border coordinates (top, bottom, left, right)
    seeds = []
    for x in range(width):
        seeds.append((x, 0))
        seeds.append((x, height - 1))
    for y in range(height):
        seeds.append((0, y))
        seeds.append((width - 1, y))
        
    # Queue for BFS flood fill
    queue = []
    for sx, sy in seeds:
        val = img_resized.getpixel((sx, sy))
        if val > bg_threshold:
            bg_mask[sy][sx] = True
            queue.append((sx, sy))
            
    # Breadth-First Search (BFS) to flood connected light pixels
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        cx, cy = queue.pop(0)
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height:
                if not bg_mask[ny][nx]:
                    pixel_val = img_resized.getpixel((nx, ny))
                    if pixel_val > bg_threshold:
                        bg_mask[ny][nx] = True
                        queue.append((nx, ny))
                        
    # 2. Render ASCII using a beautiful detailed character ramp for the subject
    chars = ["@", "%", "#", "*", "+", "=", "-", ":", ".", " "]
    
    ascii_rows = []
    for y in range(height):
        row = ""
        for x in range(width):
            if bg_mask[y][x]:
                row += " "
            else:
                pixel = img_resized.getpixel((x, y))
                # Map the pixel value (0-255) to character list index
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
