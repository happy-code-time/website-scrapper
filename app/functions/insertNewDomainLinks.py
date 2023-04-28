import sys
from functions.printer import printer
from functions.replaceDomainNameWithEmptyString import replaceDomainNameWithEmptyString 
from functions.isInternalLink import isInternalLink 
from functions.isExternalLink import isExternalLink 
from functions.isLinkAFile import isLinkAFile
from functions.isValidHref import isValidHref
from functions.mysql import executeQuerySelect, executeQueryWithCommit
from functions.request import request;

def insertNewDomainLinks(root, soup):
    http = 'http://www.'
    https = 'https://www.'
    root_id = root[0]
    root_domain = root[1]
    all_tags_a = soup.find_all('a')
    validDomainLinks = [];
    
    if root_domain[0:len(http)] != http and root_domain[0:len(https)] != https:
        printer('Root domain does not include a valid protocol https/http. All urls should be full qualified urls and start with https://www or http://www', 'error');
        sys.exit();

    for a in all_tags_a:
        href = replaceDomainNameWithEmptyString(root_domain, a['href'])

        if isValidHref(href) and True == isInternalLink(root_domain, href) and False == isExternalLink(root_domain, href) and '' == isLinkAFile(href):
            validDomainLinks.append(href);

    if len(validDomainLinks):
        printer('Saving new domain paths to the database', 'blue');
        written_entries = 0;

        for path in validDomainLinks:
            addSlash = '/';

            if '/' == path[0]:
                addSlash = '';

            domain_path = f'{root_domain}{addSlash}{path}';
            
            if 0 == len(executeQuerySelect(f'SELECT * from ws_target WHERE domain_path = "{domain_path}"')):
                written_entries += 1
                printer(f'Inserting new path: {path}', 'blue')
                executeQueryWithCommit(f'INSERT INTO ws_target (`ws_root`, `domain_path`, `block`) VALUES ({root_id},"{domain_path}", 0)');
    
        printer(f'Wrote new domain paths to database: {written_entries}', 'blue');
    else:
        printer('0 new links', 'warning');

    return validDomainLinks;