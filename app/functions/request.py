import requests
from functions.printer import printer;

def request(url):
    response = requests.get(url);
    html = None;

    if response.ok:
        html = response.text;
    else:
        printer(f'Root response invalid for: {url}', 'error');

    return html;