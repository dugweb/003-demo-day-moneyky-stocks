-- MySQL Script generated by MySQL Workbench
-- 08/30/15 14:05:44
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema moneyky
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema moneyky
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `moneyky` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `moneyky` ;

-- -----------------------------------------------------
-- Table `moneyky`.`spx_companies`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moneyky`.`spx_companies` ;

CREATE TABLE IF NOT EXISTS `moneyky`.`spx_companies` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
  `companyname` VARCHAR(75) NOT NULL COMMENT '',
  `ticker` VARCHAR(12) NULL COMMENT '',
  `sector` VARCHAR(45) NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moneyky`.`portfolios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moneyky`.`portfolios` ;

CREATE TABLE IF NOT EXISTS `moneyky`.`portfolios` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
  `date` DATE NULL COMMENT '',
  `performance` INT NULL COMMENT '',
  `benchmark` INT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moneyky`.`portfolio_holding`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moneyky`.`portfolio_holding` ;

CREATE TABLE IF NOT EXISTS `moneyky`.`portfolio_holding` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
  `company_id` INT UNSIGNED NULL COMMENT '',
  `portfolio_id` INT UNSIGNED NULL COMMENT '',
  `performance_ytd` INT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '',
  INDEX `company_id_idx` (`company_id` ASC)  COMMENT '',
  INDEX `portfolio_id_idx` (`portfolio_id` ASC)  COMMENT '',
  CONSTRAINT `company_id`
    FOREIGN KEY (`company_id`)
    REFERENCES `moneyky`.`spx_companies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `portfolio_id`
    FOREIGN KEY (`portfolio_id`)
    REFERENCES `moneyky`.`portfolios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
