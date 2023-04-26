def isExternalLink(domain, link):
    return '/' != link[0] and domain != link[0:len(domain)];