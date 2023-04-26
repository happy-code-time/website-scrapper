from __future__ import print_function
import sys
import requests
import time 
from random import randint
from bs4 import BeautifulSoup
from functions.printer import printer
from functions.mysql import blockTarget, getUrlTargets, getTargetWithEmptyContent, saveWebsitesContent
from functions.b64e import b64e, b64d
from functions.getFirstLinks import getFirstLinks
from functions.insertNewDomainLinks import insertNewDomainLinks;

class ScrapperWebsiteLinks:
    def __init__(self, executeCallback, start, end):
        self.sleepTimeCount = 0;
        self.executeCallback = '1' == executeCallback;
        self.start = start;
        self.end = end;
    #
    # Run
    #
    def init(self, loop = 0):
        loop += 1;

        if 3 < loop:
            printer('Maximum recursion for empty roots reached.', 'error');
            sys.exit();
        #
        # Get root targets with attached childrens as dict
        #
        roots = getUrlTargets();

        if [] == roots:
            printer('No roots available', 'error')
            return None;

        for root in roots:
            childrens = root.get('childrens')
            root = root.get('root')
            root_id = root[0]
            root_domain = root[1]

            if 0 == len(childrens):
                links = getFirstLinks(root, root_domain)
                #
                # No childrens found inside the root page
                #
                if 0 == len(links):
                    printer(f'No childrens available for root domain: {root_domain}', 'error')
            #
            # Main loop init
            #
            if 0 != len(childrens):
                sys.setrecursionlimit(len(childrens)*2);
                self.startLoop(root, childrens, self.start)
            #
            # If some links has been token from an website
            # during the request, get it
            #
            childrensThatNotSaved = [];
            emptyContents = getTargetWithEmptyContent(root_id);
            
            if [] != emptyContents:
                for emptyContent in emptyContents:
                    childrensThatNotSaved.append(emptyContent[2])
                    
            if 0 != len(childrensThatNotSaved):
                printer(f'Propably websites thats not scanned: {len(childrensThatNotSaved)}', 'error')
                printer('Recomended to run the command again!', 'error')
            else:
                printer(f'Successfully runned website grabbing for: {root_domain}')

    def startLoop(self, root, childrens, start = 0):
        currentLoopCount = start;
        max = len(childrens);

        if 0 != self.end:
            max = start + self.end;

        maxCountToDisplay = (max-1);

        while currentLoopCount < max:
            self.loopChildrens(root, childrens[currentLoopCount], currentLoopCount, maxCountToDisplay)
            self.sleepTimeCount += 1;
            currentLoopCount += 1

    def sleep(self):
        '''
        Sleep count is default 1 and 3 seconds.
        If count reached 3 then the random time is between 5 and 12 seconds.
        If got data from database, then the sleep function is avoided.
        '''
        if -1 == self.sleepTimeCount:
            return;

        sleepTimeMin = 1;
        sleepTimeMax = 3;

        if 3 <= self.sleepTimeCount:
            self.sleepTimeCount = 0;
            sleepTimeMin = 5;
            sleepTimeMax = 12;

        a = randint(sleepTimeMin, sleepTimeMax)
        while 1 <= a:
            print (f"\rNext request in ...{str(a)}", end='')
            a -= 1
            time.sleep(1)
        print("\n")

    def loopChildrens(self, root, child, current, max):
        id = child[0];
        website = child[2];
        website_content = child[4];
        HtmlFromRequest = '';
        matched = False;

        printer(f'[{current}|{max}]', 'white')
        printer(f"Website: {website}")

        if 'None' != str(website_content):
            HtmlFromRequest = b64d(website_content)
            printer(f'Found data inside database', 'magenta');
            printer(f'Converting from base64 back into HTML', 'magenta');
            self.sleepTimeCount = -1;
            matched = True
        
        if False == matched:
            printer(f'Url request', 'cyan');
            response = requests.get(website);

            if response.ok:
                printer('Saving result to database', 'blue');
                saveWebsitesContent(id, b64e(response.text))
                HtmlFromRequest = response.text;
            else:
                printer('Response status is invalid.', 'error');
                return blockTarget(id);
        
        soup = BeautifulSoup(HtmlFromRequest, "html.parser")
        insertNewDomainLinks(root, soup);
        #
        # Random sleep mechanism
        #
        self.sleep();