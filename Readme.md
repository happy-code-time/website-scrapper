# Website scrapper

Get all links from a website, extract new links and save websites response to an mysql database. 

# Requirements 

Required programms to be installed locally:

- docker
- docker-compose 

# Docker container build

    docker-compose -f docker-compose.yaml up --build

# Docker silent startup

    docker-compose -f docker-compose.yaml up -d

# Connet to python container

    docker exec -it website-scrapper_python /bin/bash

# Execute scan from inside the docker container

    # You have to be inside the container
    docker exec -it website-scrapper_python /bin/bash
    
    # Get only the website`s content an extract urls from it
    python index.py

    # Execute the callback method/function defined inside the "ws_root" table (from "db" database) in the column "function_type"
    python index.py execute-callback=1

# Services

Open your browser to view the saved result inside the database. 

    http://127.0.0.1:9999
    
Credentials are:

- host: 127.0.0.1 or "your local ip address"
- username: website_scrapper
- password: website_scrapper

Find out your local ip:

    # Execute in the terminal the command
    ifconfig | grep 192
