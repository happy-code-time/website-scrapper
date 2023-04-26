from bs4 import BeautifulSoup
from functions.printer import printer
from functions.request import request;
from functions.insertNewDomainLinks import insertNewDomainLinks;

def getFirstLinks(root, website):
    printer(f'Making root request to: {website}', 'cyan');
    html = request(website);
    
    if None == html:
        return [];

    soup = BeautifulSoup(html, "html.parser");
    return insertNewDomainLinks(root, soup);
