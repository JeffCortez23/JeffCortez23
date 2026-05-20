import os

with open("user_ascii.txt", "r") as f:
    lines = f.readlines()

tspan_block = ""
y_start = 30
for i, line in enumerate(lines):
    if i >= 25: break
    y = y_start + (i * 20)
    clean_line = line.strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Ensure line is 40 chars long with spaces if needed
    clean_line = clean_line.ljust(40)
    tspan_block += f'<tspan x="15" y="{y}">{clean_line}</tspan>\n'

with open("tspan_block.txt", "w") as f:
    f.write(tspan_block)
