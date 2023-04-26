from termcolor import * 

def executePrint(prefix, msg, color):
    text = colored(f'[{prefix}] ' + msg, color)
    print(text);

def printer(msg, msgType = 'success'):
    prefix = '+'
    color = 'green';

    if msgType == 'warning':
        prefix = '*'
        color = 'yellow';
        
    if msgType == 'error':
        prefix = '-'
        color = 'red';

    if msgType == 'blue':
        color = 'blue';

    if msgType == 'cyan':
        color = 'cyan';

    if msgType == 'magenta':
        color = 'magenta';

    if msgType == 'white':
        color = 'white';

    if type(msg) == type([]):
        for x in msg:
            executePrint(prefix, x, color);
    else:
        executePrint(prefix, msg, color);

