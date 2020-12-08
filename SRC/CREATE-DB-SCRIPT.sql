-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema DbMysql15
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema DbMysql15
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `DbMysql15` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `DbMysql15` ;

-- -----------------------------------------------------
-- Table `DbMysql15`.`actors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DbMysql15`.`actors` (
  `id` INT(11) NOT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `gender` TINYINT(1) NULL DEFAULT NULL,
  `popularity` FLOAT NULL DEFAULT NULL,
  `profile_path` VARCHAR(64) NULL DEFAULT NULL,
  `rnd_token` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `rnd_token` (`rnd_token` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `DbMysql15`.`corpus_movies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DbMysql15`.`corpus_movies` (
  `id` VARCHAR(7) NOT NULL,
  `title` VARCHAR(150) NULL DEFAULT NULL,
  `release_year` INT(11) NULL DEFAULT NULL,
  `imdb_rating` FLOAT NULL DEFAULT NULL,
  `votes_count` INT(11) NULL DEFAULT NULL,
  `rnd_token` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `rnd_token_UNIQUE` (`rnd_token` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `DbMysql15`.`corpus_lines`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DbMysql15`.`corpus_lines` (
  `id` VARCHAR(7) NOT NULL,
  `character_id` VARCHAR(7) NULL DEFAULT NULL,
  `movie_id` VARCHAR(7) NULL DEFAULT NULL,
  `character_name` VARCHAR(100) NULL DEFAULT NULL,
  `line` VARCHAR(3050) NULL DEFAULT NULL,
  `rnd_token` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `rnd_token_UNIQUE` (`rnd_token` ASC) VISIBLE,
  INDEX `movie_id_idx` (`movie_id` ASC) VISIBLE,
  CONSTRAINT `corpus_movie_id_FK`
    FOREIGN KEY (`movie_id`)
    REFERENCES `DbMysql15`.`corpus_movies` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `DbMysql15`.`genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DbMysql15`.`genres` (
  `id` INT(11) NOT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `rnd_token` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `rnd_token` (`rnd_token` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `DbMysql15`.`movies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DbMysql15`.`movies` (
  `id` INT(11) NOT NULL,
  `imdb_id` VARCHAR(10) NULL DEFAULT NULL,
  `title` VARCHAR(150) NULL DEFAULT NULL,
  `original_title` VARCHAR(150) NULL DEFAULT NULL,
  `overview` VARCHAR(1000) NULL DEFAULT NULL,
  `runtime` INT(11) NULL DEFAULT NULL,
  `popularity` FLOAT NULL DEFAULT NULL,
  `poster_path` VARCHAR(64) NULL DEFAULT NULL,
  `release_date` DATE NULL DEFAULT NULL,
  `status` VARCHAR(45) NULL DEFAULT NULL,
  `tagline` VARCHAR(250) NULL DEFAULT NULL,
  `vote_average` FLOAT NULL DEFAULT NULL,
  `vote_count` INT(11) NULL DEFAULT NULL,
  `rnd_token` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `rnd_token` (`rnd_token` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'list of movies';


-- -----------------------------------------------------
-- Table `DbMysql15`.`movie_actors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DbMysql15`.`movie_actors` (
  `movie_id` INT(11) NOT NULL,
  `actor_id` INT(11) NOT NULL,
  `character_name` VARCHAR(450) NULL DEFAULT NULL,
  `actor_rank` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`movie_id`, `actor_id`),
  INDEX `actor_id_idx` (`actor_id` ASC) VISIBLE,
  CONSTRAINT `actor_id`
    FOREIGN KEY (`actor_id`)
    REFERENCES `DbMysql15`.`actors` (`id`),
  CONSTRAINT `movie_id`
    FOREIGN KEY (`movie_id`)
    REFERENCES `DbMysql15`.`movies` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `DbMysql15`.`movie_genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DbMysql15`.`movie_genres` (
  `movie_id` INT(11) NOT NULL,
  `genre_id` INT(11) NOT NULL,
  PRIMARY KEY (`movie_id`, `genre_id`),
  INDEX `genre_id_idx` (`genre_id` ASC) VISIBLE,
  CONSTRAINT `FK_genre_id`
    FOREIGN KEY (`genre_id`)
    REFERENCES `DbMysql15`.`genres` (`id`),
  CONSTRAINT `FK_movie_id`
    FOREIGN KEY (`movie_id`)
    REFERENCES `DbMysql15`.`movies` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
