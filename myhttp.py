from json import dumps, loads
from urllib.request import urlopen, Request

from constants import gat, gid

def get(url):
    req = Request(url)
    with urlopen(Request(url)) as res:
        return res.read().decode()

def get_file(file: str) -> str:
    url = loads(get(f'https://api.github.com/gists/{gid}'))['files'][f'{file}.md']['raw_url']
    return get(url)

def update_file(file: str, content: str) -> bool:
    req = Request(f"https://api.github.com/gists/{gid}", bytes(dumps({
        "files": {
            f"{file}.md": {
                "content": content
            }
        }
    }), "utf8"), method="PATCH", headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gat}",
        "X-GitHub-Api-Version": "2022-11-28"
    })
    with urlopen(req) as res:
        return res.status == 200