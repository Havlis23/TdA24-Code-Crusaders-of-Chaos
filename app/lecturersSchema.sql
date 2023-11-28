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