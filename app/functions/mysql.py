import os
import time
from dotenv import load_dotenv
from mysql.connector import connect
from functions.printer import printer
load_dotenv()

def getDatbaseConnection():
    try:
        connection = connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_DATABASE'),
            port=os.getenv('DATABASE_PORT'),
        );

        return connection;
    except:
        printer('Connection to Database failed!', 'error');
        time.sleep(2);

        return getDatbaseConnection();

def executeQuerySelect(query):
    connection = getDatbaseConnection();
    cursor = connection.cursor();
    cursor.execute(query)
    data = cursor.fetchall();
    cursor.close();

    return data;

def executeQueryWithCommit(query):
    connection = getDatbaseConnection();
    cursor = connection.cursor();
    cursor.execute(f"{query}; COMMIT;")
    # connection.commit();
    cursor.close();

def getUrlTargets():
    '''
    Get the root url with childrens as dict.
    {
        "root": (id, domain ,language, function_type),
        "childrens": [
            (id, ws_root, domain_path, block, content),
            (id, ws_root, domain_path, block, content),
            ...
        ]
    }
    
    root:
        id - row id
        domain - root url where the scrapper starts
        lanuage - websites language
        function_type - after a website has been requested, and the response saved in the db, executed this function

    childrens:
        id - row id
        ws_root - root row id
        domain_path - link found inside some website
        block - on other status then "ok" (200), block the website an ignore for further scans
        content - base64 encoded html content
    '''
    roots = executeQuerySelect("SELECT * FROM ws_root");
    
    if 0 == len(roots):
        return [];

    targetItems = [];
    
    for root in roots:
        root_id = root[0]
        childrens = executeQuerySelect(f"SELECT * FROM ws_target WHERE block = 0 AND ws_root = {root_id}");
        #
        # From url extragt domain names
        #
        targetItems.append(
            {
                "root": root,
                "childrens": childrens
            }
        );

    return targetItems;

def getTargetWithEmptyContent(root_id):
    return executeQuerySelect(f"SELECT * FROM ws_target WHERE block = 0 AND ws_root = {root_id} AND content IS NULL;");

def saveWebsitesContent(target_id, base64Code):
    executeQueryWithCommit(f'UPDATE ws_target SET `content` = "{base64Code}" WHERE id = {target_id}');

def blockTarget(target_id):
    executeQueryWithCommit(f"UPDATE ws_target SET `block` = 1 WHERE id = {target_id}");