CREATE TABLE `tdapp2024`.`lecturers` (
  `uuid` INT NOT NULL,
  `title_before` VARCHAR(45) NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `middle_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `title_after` VARCHAR(45) NULL,
  `picture_url` VARCHAR(85) NULL,
  `location` VARCHAR(95) NULL,
  `claim` VARCHAR(100) NULL,
  `bio` VARCHAR(300) NULL,
  `price_per_hour` INT NULL,
  PRIMARY KEY (`uuid`));



CREATE TABLE LecturerData
(
    uuid         varchar(100) PRIMARY KEY,
    TitleBefore  VARCHAR(50),
    FirstName    VARCHAR(50),
    MiddleName   VARCHAR(50),
    LastName     VARCHAR(50),
    TitleAfter   VARCHAR(50),
    PictureURL   VARCHAR(255),
    Location     VARCHAR(50),
    Claim        TEXT,
    Bio          TEXT,
    PricePerHour DECIMAL(10, 2),
    TagID        INT,
    ContactID    INT,
    FOREIGN KEY (uuid) REFERENCES LecturerTags (uuid)
);