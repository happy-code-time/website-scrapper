# Website scrapper

Get all links from a website, extract new links and save it`s content to the database. 
After the website`s content saved to the database you can read its content locally without requesting it all the time.

Each root entry has an callback function specified in the "function_type" column inside the the "ws_root".

## Requirements 

Required programms to be installed locally:

- docker
- docker-compose 

## Setup

    # Execute this code only one time. After the build done press CTRL+C
    docker-compose -f docker-compose.yaml up --build

    # Run all containers in the background
    docker-compose -f docker-compose.yaml up -d

## Execute the app

    # Jump into the python container
    docker exec -it website-scrapper_python /bin/bash
    
    # Get only the website`s content an extract urls from it
    python index.py

    # Execute the callback method/function defined inside the "ws_root" table (from "db" database) in the column "function_type"
    python index.py execute-callback=1

## Services

Open your browser to view the saved result inside the database. 

    http://127.0.0.1:9999
    
Credentials are:

- host: 127.0.0.1 or "your local ip address"
- username: website_scrapper
- password: website_scrapper
    
## Find out your local ip:

    ifconfig | grep 192


Currently, all changes in the "ws_root" table must be made manually.