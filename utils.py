import requests
from bs4 import BeautifulSoup

# Possible valid url prefixes
all_prefix  = [
    "https://github.com",
    "https://www.github.com",
    "http://github.com",
    "http://www.github.com",
    "github.com",
    "www.github.com"
]

def startswith_any(all_prefix, url):
    """Check if `url` is a valid github link"""

    for prefix in all_prefix:
        if url.startswith(prefix):
            return prefix
    
    return False

def get(url):
    # prepare headers
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

    # fetching the url, raising error if operation fails
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        return 

    if response.ok and response.status_code == 200:
        return response.text 

def _get_repo_info(url):
    if not startswith_any(all_prefix, url):
        return 

    html = get(url)

    soup = None if not html else BeautifulSoup(html, features="lxml")

    if soup:
        repo_path = soup.find("meta", attrs={"property" : "og:title"})
        repo_url = soup.find("meta", attrs={"property" : "og:url"})
        repo_description = soup.find("meta", attrs={"property" : "og:description"})

        if repo_path and repo_url and repo_description:
            repo_path = repo_path.get("content", "")
            repo_url = repo_url.get("content", "")
            repo_description = repo_description.get("content", "")

            author, repo = repo_path.split("/", 1)
            author = author.split("-", 1)
            author = " ".join(author[1:])
            title = " ".join((x for x in repo.split("-"))).strip()

            tags = soup.find_all("a", attrs={"class" : "topic-tag" })

            _readme = soup.select("#readme .Box-title a")
            readme = None

            for r in _readme:
                text = r.text.strip()
                if text.startswith("README"):
                    readme = text
            

            repo_tags = [ t.text.strip() for t in tags ]

            return {
                "repo_title"       : title,
                "repo_path"        : repo_path,
                "repo_author"      : author,
                "repo"             : repo,
                "repo_url"         : repo_url,
                "repo_description" : repo_description,
                "repo_readme_"     : readme,
                "repo_tags"        : repo_tags,
                "repo_readme"      : None
            }

    return None


def get_rawdata_link(path, readme_file_name):
    """Returns the README.md file link"""

    raw_data_link = f"https://raw.githubusercontent.com/{path}/master/{readme_file_name}"
    return raw_data_link

def get_repo_info(url):
    """Return README.md file raw data"""
    repo_data = _get_repo_info(url)

    if repo_data:

        if repo_data["repo_readme_"]:
            raw_data_link = get_rawdata_link(repo_data["repo_path"], repo_data["repo_readme_"])
            readme = get(raw_data_link)

            repo_data["repo_readme"] = readme

    return repo_data