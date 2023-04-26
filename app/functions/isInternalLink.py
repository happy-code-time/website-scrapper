def isInternalLink(domain, link):
    return '/' == link[0] or domain == link[0:len(domain)];