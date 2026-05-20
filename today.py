import datetime
from dateutil import relativedelta
import requests
import os
from lxml import etree
import hashlib

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

def update_svg(filename, stats):
    uptime = get_uptime(BIRTHDAY)
    tree = etree.parse(filename)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    
    # Map of ID to value and desired "dots" length
    updates = [
        ('age_data', uptime, 48),
        ('repo_data', stats['repos'], 21),
        ('star_data', stats['stars'], 21),
        ('commit_data', f"{stats['commits']:,}", 19),
        ('follower_data', stats['followers'], 17),
        ('contrib_data', stats['contribs'], 15),
    ]
    
    for element_id, value, dot_len in updates:
        # Search with namespace
        element = root.find(f".//{{{root.nsmap.get(None, '')}}}*[@id='{element_id}']") if root.nsmap.get(None) else root.find(f".//*[@id='{element_id}']")
        if element is not None:
            element.text = str(value)
        
        # Update dots if id_dots exists
        dots_id = f"{element_id}_dots"
        dots_element = root.find(f".//{{{root.nsmap.get(None, '')}}}*[@id='{dots_id}']") if root.nsmap.get(None) else root.find(f".//*[@id='{dots_id}']")
        if dots_element is not None:
            just_len = max(1, dot_len - len(str(value)))
            dots_element.text = " " + ("." * just_len) + " "
                
    tree.write(filename, encoding='utf-8', xml_declaration=True)

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
