from extensions.getAvailableExtensions import getAvailableExtensions

def isLinkAFile(link):
    match = '';
    extensions = getAvailableExtensions();

    for item in extensions:
        extension = '.'+item;

        if extension == link[(len(link))-len(extension):len(link)]:
            match = extension;
            break;

    return match;