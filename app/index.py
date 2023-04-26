from extractors.ScrapperWebsiteLinks import ScrapperWebsiteLinks;
import sys

sysArgv = sys.argv;

kwargs = {
    'execute-callback': '0',
};

for i in kwargs.keys():
    for x in sysArgv:
        x = x.split('=');
        keyName = '';

        if 2 == len(x) and x[0] in kwargs.keys():
            kwargs[x[0]] = x[1];

scrapperWebsiteLinks = ScrapperWebsiteLinks(
    kwargs['execute-callback']
);
scrapperWebsiteLinks.init();