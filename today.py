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

def get_uptime(birthday):
    diff = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    return f"{diff.years} years, {diff.months} months, {diff.days} days"

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
    if not data:
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
        
    # Calculate visual length of value (handling HTML entities)
    raw_val = str(value).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
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

def generate_right_side(uptime, stats, is_dark=True):
    fill_color = "#c9d1d9" if is_dark else "#24292f"
    rows = []
    
    # 1. Header (elyefris@omarchy ---------------------------------------------------------)
    # len("elyefris@omarchy ") = 17 chars. To reach 74, we add 74 - 17 = 57 dashes.
    rows.append(f'<tspan x="390" y="80" class="title">elyefris@omarchy </tspan><tspan class="cc">---------------------------------------------------------</tspan>')
    
    # 2. Core info
    rows.append(make_tspan_row(105, "OS", "Arch Linux (Omarchy), Android 16 (SM-A566E)"))
    rows.append(make_tspan_row(125, "Uptime", uptime, "age_data"))
    rows.append(make_tspan_row(145, "Host", "Software Developer &amp; AR Student"))
    rows.append(make_tspan_row(165, "Kernel", "Linux (BTW), Hyprland, Ghostty 👻"))
    rows.append(make_tspan_row(185, "IDE", "Neovim, VSCode, Unity, Blender"))
    
    # Spacer
    rows.append(f'<tspan x="390" y="205" class="cc">.</tspan>')
    
    # Languages
    rows.append(make_tspan_row(225, "Languages.Programming", "Python, SQL, Kotlin, JavaScript, TS, C#"))
    rows.append(make_tspan_row(245, "Languages.Computer", "HTML, CSS, JSON, SQL"))
    rows.append(make_tspan_row(265, "Languages.Real", "Spanish, English"))
    
    # Spacer
    rows.append(f'<tspan x="390" y="285" class="cc">.</tspan>')
    
    # Hobbies
    rows.append(make_tspan_row(305, "Hobbies.Software", "Linux Ricing, Studying AR (Unity, Blender)"))
    rows.append(make_tspan_row(325, "Hobbies.Hardware", "Arduino, Robotics, Electronics"))
    
    # Spacer
    rows.append(f'<tspan x="390" y="345" class="cc">.</tspan>')
    
    # Contact Header (- Contact ----------------------------------------------------------------)
    # len("- Contact ") = 10 chars. To reach 74, we add 74 - 10 = 64 dashes.
    rows.append(f'<tspan x="390" y="365" class="section">- Contact </tspan><tspan class="cc">----------------------------------------------------------------</tspan>')
    
    # Contact Info
    rows.append(make_tspan_row(390, "Email.Personal", "jeffcortez2305@gmail.com"))
    rows.append(make_tspan_row(410, "LinkedIn", "Jeff Cortez"))
    rows.append(make_tspan_row(430, "Discord", "elyefris"))
    rows.append(make_tspan_row(450, "ORCID", "0009-0003-3692-7916"))
    
    # Spacer
    rows.append(f'<tspan x="390" y="470" class="cc">.</tspan>')
    
    # GitHub Stats Header (- GitHub Stats -----------------------------------------------------------)
    # len("- GitHub Stats ") = 15 chars. To reach 74, we add 74 - 15 = 59 dashes.
    rows.append(f'<tspan x="390" y="490" class="stats-title">- GitHub Stats </tspan><tspan class="cc">-----------------------------------------------------------</tspan>')
    
    # GitHub Stats Info
    rows.append(make_tspan_row(515, "Repos", str(stats['repos']), "repo_data"))
    rows.append(make_tspan_row(535, "Contributed", str(stats['contribs']), "contrib_data"))
    rows.append(make_tspan_row(555, "Stars", str(stats['stars']), "star_data"))
    rows.append(make_tspan_row(575, "Commits", f"{stats['commits']:,}", "commit_data"))
    rows.append(make_tspan_row(595, "Followers", str(stats['followers']), "follower_data"))
    
    return f'<!-- Right Side Terminal Content -->\n<text x="390" y="80" fill="{fill_color}">\n' + "\n".join(rows) + "\n</text>"

def update_svg(filename, stats):
    is_dark = "dark" in filename
    uptime = get_uptime(BIRTHDAY)
    
    right_side = generate_right_side(uptime, stats, is_dark=is_dark)
    
    with open(filename, "r") as f:
        content = f.read()
        
    # Replace from <!-- Right Side Terminal Content --> to </svg>
    pattern = r'<!-- Right Side Terminal Content -->.*?</svg>'
    replacement = f'{right_side}\n</svg>'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(filename, "w") as f:
        f.write(new_content)

if __name__ == '__main__':
    print(f"Updating profile for {USER_NAME}...")
    stats = fetch_stats(USER_NAME)
    if not stats:
        print("Failed to fetch stats, using defaults.")
        stats = {'repos': 9, 'stars': 3, 'commits': 107, 'followers': 1, 'contribs': 12}
    
    print(f"Stats: {stats}")
    update_svg('dark_mode.svg', stats)
    update_svg('light_mode.svg', stats)
    print("Profile SVGs updated successfully.")
