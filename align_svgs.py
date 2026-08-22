import re

def make_tspan_row(y, key, value, value_id=None, total_len=74):
    if "." in key:
        parts = key.split(".")
        key_html = ".".join([f'<tspan class="key">{p}</tspan>' for p in parts])
    else:
        key_html = f'<tspan class="key">{key}</tspan>'
        
    # Calculate visual length of value (handling HTML entities)
    raw_val = value.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    raw_val_len = len(raw_val)
    if "👻" in raw_val:
        # 👻 is a double-width char in terminal/monospace rendering
        raw_val_len += 1
        
    num_dots = total_len - len(key) - raw_val_len - 5
    if num_dots < 1:
        num_dots = 1
        
    dots_str = "." * num_dots
    
    dots_id_str = f' id="{value_id}_dots"' if value_id else ''
    val_id_str = f' id="{value_id}"' if value_id else ''
    
    return f'<tspan x="390" y="{y}" class="cc">. </tspan>{key_html}:<tspan class="cc"{dots_id_str}> {dots_str} </tspan><tspan class="value"{val_id_str}>{value}</tspan>'

def generate_body_block(uptime="24 years, 11 months, 27 days"):
    rows = [
        make_tspan_row(120, "OS", "Arch Linux (Omarchy), Android 16 (SM-A566E)"),
        make_tspan_row(140, "Uptime", uptime, "age_data"),
        make_tspan_row(160, "Host", "Software Developer &amp; AR Student"),
        make_tspan_row(180, "Kernel", "Linux (BTW), Hyprland, Ghostty 👻"),
        make_tspan_row(200, "IDE", "Neovim, Ghostty, VSCode, Zed"),
        "",
        make_tspan_row(235, "Languages.Programming", "Python, SQL, Kotlin, JavaScript, TS, C#"),
        make_tspan_row(255, "Languages.Computer", "HTML, CSS, JSON, SQL"),
        make_tspan_row(275, "Languages.Real", "Spanish, English"),
        "",
        make_tspan_row(310, "Hobbies.Software", "Linux Ricing, Omarchy Plugins, Shell Scripting"),
        make_tspan_row(330, "Hobbies.Hardware", "Arduino, Robotics, Electronics")
    ]
    return f'<text x="390" y="120" fill="VAR_COLOR">\n' + "\n".join(rows) + "\n</text>"

def generate_contact_block():
    rows = [
        make_tspan_row(405, "Email.Personal", "jeffcortez2305@gmail.com"),
        make_tspan_row(425, "LinkedIn", "Jeff Cortez"),
        make_tspan_row(445, "Discord", "elyefris"),
        make_tspan_row(465, "ORCID", "0009-0003-3692-7916")
    ]
    return f'<text x="390" y="405" fill="VAR_COLOR">\n' + "\n".join(rows) + "\n</text>"

def generate_stats_block(repos="9", contribs="12", stars="3", commits="107", followers="1"):
    rows = [
        make_tspan_row(545, "Repos", repos, "repo_data"),
        make_tspan_row(565, "Contributed", contribs, "contrib_data"),
        make_tspan_row(585, "Stars", stars, "star_data"),
        make_tspan_row(605, "Commits", commits, "commit_data"),
        make_tspan_row(625, "Followers", followers, "follower_data")
    ]
    return f'<text x="390" y="545" fill="VAR_COLOR">\n' + "\n".join(rows) + "\n</text>"

def align_svg(svg_path, is_dark=True):
    fill_color = "#c9d1d9" if is_dark else "#24292f"
    
    with open(svg_path, "r") as f:
        content = f.read()
        
    # Extract current stats/uptime values to preserve them during alignment
    uptime_match = re.search(r'id="age_data">(.*?)</tspan>', content)
    uptime = uptime_match.group(1) if uptime_match else "24 years, 11 months, 27 days"
    
    repos_match = re.search(r'id="repo_data">(.*?)</tspan>', content)
    repos = repos_match.group(1) if repos_match else "9"
    
    contribs_match = re.search(r'id="contrib_data">(.*?)</tspan>', content)
    contribs = contribs_match.group(1) if contribs_match else "12"
    
    stars_match = re.search(r'id="star_data">(.*?)</tspan>', content)
    stars = stars_match.group(1) if stars_match else "3"
    
    commits_match = re.search(r'id="commit_data">(.*?)</tspan>', content)
    commits = commits_match.group(1) if commits_match else "107"
    
    followers_match = re.search(r'id="follower_data">(.*?)</tspan>', content)
    followers = followers_match.group(1) if followers_match else "1"
    
    # Generate new blocks
    body_block = generate_body_block(uptime).replace("VAR_COLOR", fill_color)
    contact_block = generate_contact_block().replace("VAR_COLOR", fill_color)
    stats_block = generate_stats_block(repos, contribs, stars, commits, followers).replace("VAR_COLOR", fill_color)
    
    # Replace body block
    content = re.sub(r'<text x="390" y="120" fill=".*?">.*?</text>', body_block, content, flags=re.DOTALL)
    
    # Replace contact block
    content = re.sub(r'<text x="390" y="405" fill=".*?">.*?</text>', contact_block, content, flags=re.DOTALL)
    
    # Replace stats block
    content = re.sub(r'<text x="390" y="545" fill=".*?">.*?</text>', stats_block, content, flags=re.DOTALL)
    
    with open(svg_path, "w") as f:
        f.write(content)
        
    print(f"Aligned and formatted {svg_path}")

if __name__ == '__main__':
    align_svg("dark_mode.svg", is_dark=True)
    align_svg("light_mode.svg", is_dark=False)
