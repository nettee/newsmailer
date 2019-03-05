CREATE TABLE jokes (
    id int NOT NULL AUTO_INCREMENT,
    link varchar(255) NOT NULL,
    text varchar(999) NOT NULL,
    votes int,
    comments int,
    PRIMARY KEY (id)
);

CREATE TABLE images (
    id int NOT NULL AUTO_INCREMENT,
    url varchar(255) NOT NULL,
    joke_id int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (joke_id) REFERENCES jokes(id)
);