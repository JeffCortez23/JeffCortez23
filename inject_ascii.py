import re

def generate_tspan_block(ascii_file, start_y=160):
    with open(ascii_file, "r") as f:
        lines = [line.rstrip("\n") for line in f.readlines() if line.strip("\n")]
        
    tspan_lines = []
    for i, line in enumerate(lines):
        # Escape XML entities just in case
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if i == 0:
            tspan_lines.append(f'<tspan x="35" y="{start_y}">{escaped_line}</tspan>')
        else:
            tspan_lines.append(f'<tspan x="35" dy="12">{escaped_line}</tspan>')
            
    return "\n".join(tspan_lines)

def inject_into_svg(svg_path, tspan_block, start_y=160):
    with open(svg_path, "r") as f:
        content = f.read()
        
    # Regex to match the ASCII text block
    # Looks for <text x="35" y="..." class="ascii"> ... </text>
    pattern = r'(<!-- Left Side Sharp Photo ASCII Art \(Centered Vertically\) -->\s*<text x="35" y=")\d+(" class="ascii">)(.*?)(</text>)'
    
    replacement = rf'\g<1>{start_y}\g<2>\n{tspan_block}\n\g<4>'
    
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count > 0:
        with open(svg_path, "w") as f:
            f.write(new_content)
        print(f"Successfully injected ASCII art into {svg_path}")
    else:
        print(f"ERROR: Could not find target ASCII block in {svg_path}")

if __name__ == '__main__':
    ascii_file = "user_ascii_preview.txt"
    tspan_block = generate_tspan_block(ascii_file, start_y=160)
    
    inject_into_svg("dark_mode.svg", tspan_block, start_y=160)
    inject_into_svg("light_mode.svg", tspan_block, start_y=160)
