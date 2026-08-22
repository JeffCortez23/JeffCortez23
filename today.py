import datetime
from dateutil import relativedelta
import requests
import os
import re

# Configuration
USER_NAME = os.environ.get('USER_NAME', 'JeffCortez23')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
HEADERS = {'authorization': f'token {ACCESS_TOKEN}'} if ACCESS_TOKEN else {}
BIRTHDAY = datetime.datetime(2001, 5, 23)

def format_plural(unit):
    return 's' if unit != 1 else ''

def get_uptime(birthday):
    diff = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    years_str = f"{diff.years} year{format_plural(diff.years)}"
    months_str = f"{diff.months} month{format_plural(diff.months)}"
    days_str = f"{diff.days} day{format_plural(diff.days)}"
    birthday_emoji = " 🎂" if (diff.months == 0 and diff.days == 0) else ""
    return f"{years_str}, {months_str}, {days_str}{birthday_emoji}"

def simple_request(query, variables):
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=HEADERS)
    if request.status_code == 200:
        return request.json()
    return None

def fetch_stats(username):
    query = """
    query($login: String!) {
        user(login: $login) {
            repositories(first: 100, ownerAffiliations: OWNER) {
                totalCount
                edges {
                    node {
                        stargazers {
                            totalCount
                        }
                    }
                }
            }
            repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
                totalCount
            }
            contributionsCollection {
                totalCommitContributions
                restrictedContributionsCount
            }
            followers {
                totalCount
            }
        }
    }
    """
    data = simple_request(query, {'login': username})
    if not data or 'data' not in data or not data['data']['user']:
        return None
    
    user = data['data']['user']
    repos = user['repositories']['totalCount']
    stars = sum(repo['node']['stargazers']['totalCount'] for repo in user['repositories']['edges'])
    commits = user['contributionsCollection']['totalCommitContributions'] + user['contributionsCollection']['restrictedContributionsCount']
    followers = user['followers']['totalCount']
    contribs = user['repositoriesContributedTo']['totalCount']
    
    return {
        'repos': repos,
        'stars': stars,
        'commits': commits,
        'followers': followers,
        'contribs': contribs
    }

def make_tspan_row(y, key, value, value_id=None, total_len=74):
    if "." in key:
        parts = key.split(".")
        key_html = ".".join([f'<tspan class="key">{p}</tspan>' for p in parts])
    else:
        key_html = f'<tspan class="key">{key}</tspan>'
        
    raw_val = str(value).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    raw_val_len = len(raw_val)
    if "👻" in raw_val or "🚀" in raw_val:
        raw_val_len += 1
        
    num_dots = total_len - len(key) - raw_val_len - 5
    if num_dots < 1:
        num_dots = 1
        
    dots_str = "." * num_dots
    dots_id_str = f' id="{value_id}_dots"' if value_id else ''
    val_id_str = f' id="{value_id}"' if value_id else ''
    
    return f'<tspan x="390" y="{y}" class="cc">. </tspan>{key_html}:<tspan class="cc"{dots_id_str}> {dots_str} </tspan><tspan class="value"{val_id_str}>{value}</tspan>'

def generate_right_side(uptime, stats, is_dark=True):
    fill_color = "#c9d1d9" if is_dark else "#24292f"
    rows = []
    
    # 1. Header
    rows.append(f'<tspan x="390" y="90" class="title">elyefris@omarchy </tspan><tspan class="cc">---------------------------------------------------------</tspan>')
    
    # 2. Core info (Arch, Omarchy, CachyOS Kernel)
    rows.append(make_tspan_row(120, "OS", "Arch Linux (Omarchy) · CachyOS Kernel"))
    rows.append(make_tspan_row(145, "Uptime", uptime, "age_data"))
    rows.append(make_tspan_row(170, "Host", "Systems &amp; Software Engineering Student"))
    rows.append(make_tspan_row(195, "Kernel", "Linux-CachyOS (Zen 2 Optimized), Hyprland 🚀"))
    rows.append(make_tspan_row(220, "IDE", "Neovim, Ghostty, VSCode, Zed"))
    
    # Spacer
    rows.append(f'<tspan x="390" y="240" class="cc">.</tspan>')
    
    # Languages (with QML & Bash)
    rows.append(make_tspan_row(265, "Languages.Programming", "Python, QML, Bash, Kotlin, TS, C#, SQL"))
    rows.append(make_tspan_row(290, "Languages.Computer", "HTML, CSS, JSON, YAML, LaTeX"))
    rows.append(make_tspan_row(315, "Languages.Real", "Spanish, English"))
    
    # Spacer
    rows.append(f'<tspan x="390" y="335" class="cc">.</tspan>')
    
    # Hobbies (Linux Ricing, Omarchy Plugins, Shell Scripting, Embedded)
    rows.append(make_tspan_row(360, "Hobbies.Software", "Linux Ricing, Omarchy Plugins, Shell Scripting"))
    rows.append(make_tspan_row(385, "Hobbies.Hardware", "Microcontrollers, Arduino, Electronics"))
    
    # Spacer
    rows.append(f'<tspan x="390" y="405" class="cc">.</tspan>')
    
    # Contact Header
    rows.append(f'<tspan x="390" y="430" class="section">- Contact </tspan><tspan class="cc">----------------------------------------------------------------</tspan>')
    
    # Contact Info
    rows.append(make_tspan_row(460, "Email.Personal", "jeffcortez2305@gmail.com"))
    rows.append(make_tspan_row(485, "LinkedIn", "Jeff Cortez"))
    rows.append(make_tspan_row(510, "Discord", "elyefris"))
    rows.append(make_tspan_row(535, "ORCID", "0009-0003-3692-7916"))
    
    # Spacer
    rows.append(f'<tspan x="390" y="555" class="cc">.</tspan>')
    
    # GitHub Stats Header
    rows.append(f'<tspan x="390" y="580" class="stats-title">- GitHub Stats </tspan><tspan class="cc">-----------------------------------------------------------</tspan>')
    
    # GitHub Stats Info
    rows.append(make_tspan_row(610, "Repos", str(stats['repos']), "repo_data"))
    rows.append(make_tspan_row(635, "Contributed", str(stats['contribs']), "contrib_data"))
    rows.append(make_tspan_row(660, "Stars", str(stats['stars']), "star_data"))
    rows.append(make_tspan_row(685, "Commits", f"{stats['commits']:,}", "commit_data"))
    rows.append(make_tspan_row(710, "Followers", str(stats['followers']), "follower_data"))
    
    return f'<!-- Right Side Terminal Content -->\n<text x="390" y="90" fill="{fill_color}" class="right-text">\n' + "\n".join(rows) + "\n</text>"

# Crisp, iconic high-resolution Arch Linux ASCII Art (36 lines, vertically centered)
ARCH_ASCII_LINES = [
    "                   -`                   ",
    "                  .o+`                  ",
    "                 `ooo/                  ",
    "                `+oooo:                 ",
    "               `+oooooo:                ",
    "               -+oooooo+:               ",
    "             `/:-:++oooo+:              ",
    "            `/++++/+++++++:             ",
    "           `/++++++++++++++:            ",
    "          `/+++ooooooooooooo/`          ",
    "         ./ooosssso++osssssso+`         ",
    "        .oossssso-````/ossssss+`        ",
    "       -osssssso.      :ssssssso.       ",
    "      :osssssss/        osssso+++.      ",
    "     /ossssssss/        +ssssooo/-      ",
    "   `/ossssso+/:-        -:/+osssso+-    ",
    "  `+sso+:-`                 `.-/+oso:   ",
    " `++:.                           `-/+/  ",
    " .`                                 `/  ",
    "                                        ",
    "       ██████╗ ██████╗  ██████╗██╗  ██╗ ",
    "      ██╔══██╗██╔══██╗██╔════╝██║  ██║ ",
    "      ███████║██████╔╝██║     ███████║ ",
    "      ██╔══██║██╔══██╗██║     ██╔══██║ ",
    "      ██║  ██║██║  ██║╚██████╗██║  ██║ ",
    "      ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ",
    "          ██╗     ██╗███╗   ██╗██╗   ██╗",
    "          ██║     ██║████╗  ██║██║   ██║",
    "          ██║     ██║██╔██╗ ██║██║   ██║",
    "          ██║     ██║██║╚██╗██║██║   ██║",
    "          ███████╗██║██║ ╚████║╚██████╔╝",
    "          ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ "
]

def generate_ascii_block():
    spans = [f'<tspan x="35" y="105" class="ascii">{ARCH_ASCII_LINES[0]}</tspan>']
    for line in ARCH_ASCII_LINES[1:]:
        spans.append(f'<tspan x="35" dy="17" class="ascii">{line}</tspan>')
    return "\n".join(spans)

def create_base_svg(is_dark=True):
    bg_color = "#0d1117" if is_dark else "#f6f8fa"
    border_color = "#30363d" if is_dark else "#d0d7de"
    header_text_color = "#8b949e" if is_dark else "#57606a"
    line_color = "#30363d" if is_dark else "#d0d7de"
    
    grad1 = "#7aa2f7" if is_dark else "#0969da"
    grad2 = "#89ddff" if is_dark else "#1f6feb"
    grad3 = "#bb9af3" if is_dark else "#8250df"
    
    key_color = "#ffa657" if is_dark else "#bf4b00"
    val_color = "#a5d6ff" if is_dark else "#0550ae"
    cc_color = "#444b5a" if is_dark else "#8c959f"
    title_color = "#7bb5ed" if is_dark else "#0969da"
    section_color = "#bb9af3" if is_dark else "#8250df"
    stats_color = "#ff9e64" if is_dark else "#cf222e"
    
    ascii_block = generate_ascii_block()
    
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="'JetBrains Mono', 'Fira Code', 'Consolas', monospace" width="1120px" height="750px" viewBox="0 0 1120 750" font-size="14px">
<defs>
<linearGradient id="asciiGrad" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stop-color="{grad1}"/>
  <stop offset="50%" stop-color="{grad2}"/>
  <stop offset="100%" stop-color="{grad3}"/>
</linearGradient>
</defs>
<style>
.key {{fill: {key_color}; font-weight: bold;}}
.value {{fill: {val_color};}}
.cc {{fill: {cc_color};}}
.ascii {{fill: url(#asciiGrad); font-weight: bold; font-size: 11.5px; font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;}}
.title {{fill: {title_color}; font-weight: bold;}}
.section {{fill: {section_color}; font-weight: bold;}}
.stats-title {{fill: {stats_color}; font-weight: bold;}}
.right-text {{font-size: 15.5px;}}
text, tspan {{white-space: pre;}}
</style>
<rect width="1120" height="750" fill="{bg_color}" stroke="{border_color}" stroke-width="2" rx="15"/>

<!-- Terminal Header -->
<circle cx="25" cy="25" r="6" fill="#ff5f56"/>
<circle cx="45" cy="25" r="6" fill="#ffbd2e"/>
<circle cx="65" cy="25" r="6" fill="#27c93f"/>
<text x="90" y="30" fill="{header_text_color}" font-size="13px" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">elyefris@omarchy — Terminal</text>
<line x1="15" y1="45" x2="1105" y2="45" stroke="{line_color}" stroke-width="1.5"/>

<!-- Left Side Arch Linux ASCII Art -->
<text x="35" y="105" class="ascii">
{ascii_block}
</text>

<!-- Right Side Terminal Content -->
</svg>"""

def update_svg(filename, stats):
    is_dark = "dark" in filename
    uptime = get_uptime(BIRTHDAY)
    
    base_svg = create_base_svg(is_dark=is_dark)
    right_side = generate_right_side(uptime, stats, is_dark=is_dark)
    
    new_content = base_svg.replace("<!-- Right Side Terminal Content -->", right_side)
    
    with open(filename, "w") as f:
        f.write(new_content)

if __name__ == '__main__':
    print(f"Updating profile for {USER_NAME}...")
    stats = fetch_stats(USER_NAME)
    if not stats:
        print("Failed to fetch GraphQL stats, querying REST API...")
        try:
            r = requests.get(f'https://api.github.com/users/{USER_NAME}')
            u = r.json()
            stats = {
                'repos': u.get('public_repos', 10),
                'stars': 3,
                'commits': 236,
                'followers': u.get('followers', 2),
                'contribs': 2
            }
        except:
            stats = {'repos': 10, 'stars': 3, 'commits': 236, 'followers': 2, 'contribs': 2}
            
    print(f"Stats: {stats}")
    update_svg('dark_mode.svg', stats)
    update_svg('light_mode.svg', stats)
    print("Profile SVGs updated successfully.")
