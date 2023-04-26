USE mysql;
-- 
-- DB db
--
CREATE DATABASE IF NOT EXISTS db CHARACTER SET utf8 COLLATE utf8_general_ci; 
-- 
-- Root password
--
CREATE USER IF NOT EXISTS 'website_scrapper'@'%' IDENTIFIED BY 'website_scrapper';
GRANT ALL PRIVILEGES ON * . * TO 'website_scrapper'@'%'  WITH GRANT OPTION;
ALTER USER 'website_scrapper'@'%' IDENTIFIED BY 'website_scrapper';
FLUSH PRIVILEGES;

USE db;

CREATE TABLE IF NOT EXISTS `ws_root` (
    `id` int(255) NOT NULL AUTO_INCREMENT,
    `domain` varchar(255) DEFAULT NULL,
    `language` varchar(10) DEFAULT NULL,
    `function_type` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE IF NOT EXISTS `ws_target` (
    `id` int(255) NOT NULL AUTO_INCREMENT,
    `ws_root` int(255) NOT NULL,
    `domain_path` longtext NOT NULL,
    `block` int(1) DEFAULT 0,
    `content` longtext DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO ws_root (`domain`, `language`, `function_type`) VALUES ('https://www.example.com', 'en', 'callback');