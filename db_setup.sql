CREATE DATABASE IF NOT EXISTS `TaggerBot`
    CHARACTER SET utf8
    COLLATE utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS `TaggerBot`.`BlacklistedTags` (
    `Id` INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `TagName` UNIQUE VARCHAR(20) NOT NULL,
    `SiteName` VARCHAR(50) NOT NULL
) ENGINE MyISAM CHARACTER SET utf8 COLLATE utf8_unicode_ci AUTO_INCREMENT 0;

INSERT INTO `TaggerBot`.`BlacklistedTags` (`Id`, `TagName`, `SiteName`) VALUES
    (DEFAULT, 'function', 'stackoverflow'),
    (DEFAULT, 'return', 'stackoverflow'),
    (DEFAULT, 'class', 'stackoverflow'),
    (DEFAULT, 'string', 'stackoverflow'),
    (DEFAULT, 'static', 'stackoverflow'),
    (DEFAULT, 'object', 'stackoverflow'),
    (DEFAULT, 'table', 'stackoverflow'),
    (DEFAULT, 'fuzzy', 'stackoverflow'),
    (DEFAULT, 'java-server', 'stackoverflow'),
    (DEFAULT, 'advertising', 'stackoverflow'),
    (DEFAULT, 'spam', 'stackoverflow'),
    (DEFAULT, 'option', 'stackoverflow'),
    (DEFAULT, 'delivery', 'stackoverflow'),
    (DEFAULT, 'pod', 'stackoverflow'),
    (DEFAULT, 'xmlns', 'stackoverflow'),
    (DEFAULT, 'google hangouts', 'stackoverflow'),
    (DEFAULT, 'scraper', 'stackoverflow'),
    (DEFAULT, 'history', 'stackoverflow'),
    (DEFAULT, 'scrape', 'stackoverflow'),
    (DEFAULT, 'conflict', 'stackoverflow'),
    (DEFAULT, 'stylesheet', 'stackoverflow'),
    (DEFAULT, 'http status code 500', 'stackoverflow'),
    (DEFAULT, 'styles', 'stackoverflow'),
    (DEFAULT, 'positioning', 'stackoverflow'),
    (DEFAULT, 'apache tomee', 'stackoverflow'),
    (DEFAULT, 'code smell', 'stackoverflow'),
    (DEFAULT, 'microsoft', 'stackoverflow'),
    (DEFAULT, 'data', 'stackoverflow'),
    (DEFAULT, 'adf faces', 'stackoverflow'),
    (DEFAULT, 'acm icpc', 'stackoverflow'),
    (DEFAULT, 'tutorials', 'stackoverflow'),
    (DEFAULT, 'yahoo', 'stackoverflow'),
    (DEFAULT, 'code review', 'stackoverflow'),
    (DEFAULT, 'apple', 'stackoverflow'),
    (DEFAULT, 'godaddy', 'stackoverflow'),
    (DEFAULT, 'file', 'stackoverflow'),
    (DEFAULT, 'image', 'stackoverflow'),
    (DEFAULT, 'background', 'stackoverflow'),
    (DEFAULT, 'build', 'stackoverflow'),
    (DEFAULT, 'merge', 'stackoverflow'),
    (DEFAULT, 'text', 'stackoverflow'),
    (DEFAULT, 'get', 'stackoverflow');