CREATE TABLE members (
    name varchar(20) NOT NULL PRIMARY KEY,
    pass varchar(128) NOT NULL
);

CREATE TABLE records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(20) NOT NULL, 
    text varchar(256) NOT NULL,
    CONSTRAINT fk_name
    FOREIGN KEY (name) 
    REFERENCES members (name)
    ON DELETE RESTRICT ON UPDATE RESTRICT    
);

