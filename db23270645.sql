-- MySQL Workbench Forward Engineering
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema dunodb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema dunodb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dunodb` DEFAULT CHARACTER SET utf8 ;
USE `dunodb` ;

-- -----------------------------------------------------
-- Table `dunodb`.`categorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`categorias` (
  `id_categorias` INT NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id_categorias`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dunodb`.`proveedores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`proveedores` (
  `id_proveedor` INT NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id_proveedor`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dunodb`.`unidad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`unidad` (
  `id_unidad` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_unidad`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dunodb`.`articulos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`articulos` (
  `codigo` CHAR(13) NOT NULL,
  `nombre` VARCHAR(70) NOT NULL,
  `precio` FLOAT NOT NULL,
  `costo` FLOAT NOT NULL,
  `existencias` INT NOT NULL,
  `reorden` VARCHAR(45) NOT NULL,
  `id_categorias` INT NOT NULL,
  `id_proveedor` INT NOT NULL,
  `id_unidad` INT NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_articulos_categorias_idx` (`id_categorias` ASC) VISIBLE,
  INDEX `fk_articulos_proveedores1_idx` (`id_proveedor` ASC) VISIBLE,
  INDEX `fk_articulos_unidad1_idx` (`id_unidad` ASC) VISIBLE,
  CONSTRAINT `fk_articulos_categorias`
    FOREIGN KEY (`id_categorias`)
    REFERENCES `dunodb`.`categorias` (`id_categorias`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulos_proveedores1`
    FOREIGN KEY (`id_proveedor`)
    REFERENCES `dunodb`.`proveedores` (`id_proveedor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulos_unidad1`
    FOREIGN KEY (`id_unidad`)
    REFERENCES `dunodb`.`unidad` (`id_unidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dunodb`.`clientes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`clientes` (
  `telefono` CHAR(10) NOT NULL,
  `nombre` VARCHAR(75) NOT NULL,
  `direccion` VARCHAR(100) NOT NULL,
  `rfc` VARCHAR(20) NULL,
  PRIMARY KEY (`telefono`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dunodb`.`empleado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`empleado` (
  `id_empleado` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `genero` ENUM('M', 'F') NOT NULL,
  `puesto` ENUM('encargado', 'cajero', 'administrador') NOT NULL,
  PRIMARY KEY (`id_empleado`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dunodb`.`venta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`venta` (
  `id_venta` INT NOT NULL,
  `fecha` DATE NOT NULL,
  `importe` FLOAT NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  `id_empleado` INT NOT NULL,
  PRIMARY KEY (`id_venta`),
  INDEX `fk_venta_clientes1_idx` (`telefono` ASC) VISIBLE,
  INDEX `fk_venta_empleado1_idx` (`id_empleado` ASC) VISIBLE,
  CONSTRAINT `fk_venta_clientes1`
    FOREIGN KEY (`telefono`)
    REFERENCES `dunodb`.`clientes` (`telefono`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_venta_empleado1`
    FOREIGN KEY (`id_empleado`)
    REFERENCES `dunodb`.`empleado` (`id_empleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dunodb`.`compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`compra` (
  `id_compra` INT NOT NULL,
  `folio` VARCHAR(20) NOT NULL,
  `tipodoc` VARCHAR(20) NOT NULL,
  `fecha` DATE NOT NULL,
  `importe` FLOAT NOT NULL,
  `id_proveedor` INT NOT NULL,
  PRIMARY KEY (`id_compra`),
  INDEX `fk_compra_proveedores1_idx` (`id_proveedor` ASC) VISIBLE,
  CONSTRAINT `fk_compra_proveedores1`
    FOREIGN KEY (`id_proveedor`)
    REFERENCES `dunodb`.`proveedores` (`id_proveedor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dunodb`.`detalles_comp`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`detalles_comp` (
  `id_compra` INT NOT NULL,
  `codigo` CHAR(13) NOT NULL,
  `cantidad` INT NOT NULL,
  `costo` FLOAT NOT NULL,
  PRIMARY KEY (`id_compra`, `codigo`),
  INDEX `fk_detalles_comp_compra1_idx` (`id_compra` ASC) VISIBLE,
  INDEX `fk_detalles_comp_articulos1_idx` (`codigo` ASC) VISIBLE,
  CONSTRAINT `fk_detalles_comp_compra1`
    FOREIGN KEY (`id_compra`)
    REFERENCES `dunodb`.`compra` (`id_compra`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_detalles_comp_articulos1`
    FOREIGN KEY (`codigo`)
    REFERENCES `dunodb`.`articulos` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dunodb`.`detalles_venta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`detalles_venta` (
  `id_venta` INT NOT NULL,
  `codigo` CHAR(13) NOT NULL,
  `cantidad` INT NOT NULL,
  `precio` FLOAT NOT NULL,
  PRIMARY KEY (`id_venta`, `codigo`),
  INDEX `fk_detalles_venta_venta1_idx` (`id_venta` ASC) VISIBLE,
  INDEX `fk_detalles_venta_articulos1_idx` (`codigo` ASC) VISIBLE,
  CONSTRAINT `fk_detalles_venta_venta1`
    FOREIGN KEY (`id_venta`)
    REFERENCES `dunodb`.`venta` (`id_venta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_detalles_venta_articulos1`
    FOREIGN KEY (`codigo`)
    REFERENCES `dunodb`.`articulos` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
