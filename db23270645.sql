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
-- Table `dunodb`.`categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`categoria` (
  `id_categoria` INT NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id_categoria`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dunodb`.`proveedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`proveedor` (
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
-- Table `dunodb`.`articulo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`articulo` (
  `codigo` CHAR(13) NOT NULL,
  `nombre` VARCHAR(70) NOT NULL,
  `precio` FLOAT NOT NULL,
  `costo` FLOAT NOT NULL,
  `existencias` INT NOT NULL,
  `reorden` VARCHAR(45) NOT NULL,
  `id_categoria` INT NOT NULL,
  `id_proveedor` INT NOT NULL,
  `id_unidad` INT NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_articulos_categorias_idx` (`id_categoria` ASC) VISIBLE,
  INDEX `fk_articulos_proveedores1_idx` (`id_proveedor` ASC) VISIBLE,
  INDEX `fk_articulos_unidad1_idx` (`id_unidad` ASC) VISIBLE,
  CONSTRAINT `fk_articulos_categorias`
    FOREIGN KEY (`id_categoria`)
    REFERENCES `dunodb`.`categoria` (`id_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulos_proveedores1`
    FOREIGN KEY (`id_proveedor`)
    REFERENCES `dunodb`.`proveedor` (`id_proveedor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulos_unidad1`
    FOREIGN KEY (`id_unidad`)
    REFERENCES `dunodb`.`unidad` (`id_unidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dunodb`.`cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dunodb`.`cliente` (
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
  `forma_pago` ENUM('Efectivo', 'Targeta') NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  `id_empleado` INT NOT NULL,
  PRIMARY KEY (`id_venta`),
  INDEX `fk_venta_clientes1_idx` (`telefono` ASC) VISIBLE,
  INDEX `fk_venta_empleado1_idx` (`id_empleado` ASC) VISIBLE,
  CONSTRAINT `fk_venta_clientes1`
    FOREIGN KEY (`telefono`)
    REFERENCES `dunodb`.`cliente` (`telefono`)
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
    REFERENCES `dunodb`.`proveedor` (`id_proveedor`)
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
    REFERENCES `dunodb`.`articulo` (`codigo`)
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
    REFERENCES `dunodb`.`articulo` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


INSERT INTO unidad (id_unidad, nombre) VALUES 
(1, 'pieza'),
(2, 'litro'),
(3, 'gramo'),
(4, 'kilogramo'),
(5, 'mililitro'),
(6, 'sobre'),
(7, 'unidad');

INSERT INTO categoria (id_categoria, nombre) VALUES
(1, 'Lacteos'),
(2, 'Salsas y Aderezos'),
(3, 'Bebidas'),
(4, 'Panaderia y Pasteleria'),
(5, 'Cafe y Te'),
(6, 'Harinas y Cereales'),
(7, 'Snacks y Dulces'),
(9, 'Condimentos'),
(10, 'Galletas y Snacks'),
(11,'Limpieza'),
(12, 'Embutidos');

INSERT INTO proveedor (id_proveedor, nombre, telefono) VALUES
(1, 'Grupo Lala', '5551234567'),
(2, 'Clemente Jacques', '5552345678'),
(3, 'Danone México', '5553456789'),
(4, 'Gamesa', '5554567890'),
(5, 'Pisa Farmacéutica', '5555678901'),
(6, 'Nestlé México', '5556789012'),
(7, 'Maseca', '5557890123'),
(8, 'Herdez', '5558901234'),
(9, 'Great Value', '5559012345'),
(10, 'Sabritas', '5550123456'),
(11, 'Insumos de limpieza', '5556541234');

INSERT INTO articulo (codigo, nombre, precio, costo, existencias, reorden, id_categoria, id_proveedor, id_unidad) VALUES
('7501020565959', 'Leche semidescremada Lala 1 lt', 22.50, 18.00, 50, 10, 1, 1, 2),
('7501052472195', 'Catsup Clemente Jacques 220g', 18.00, 12.50, 100, 20, 2, 2, 3),
('7501040090028', 'Yoghurt Yoplait Batido Natural 1Kg', 35.00, 28.00, 60, 15, 1, 1, 4),
('7501032398477', 'Vitalinea sin azucar sabor Manzana Verde - Danone', 24.00, 20.00, 40, 10, 1, 3, 3),
('7501000630363', 'Mini Mamut Gamesa 12 g', 6.00, 4.00, 120, 30, 7, 3, 3),
('7501125149221', 'Electrolit sabor Fresa/Kiwi 625 ml', 28.00, 22.00, 80, 20, 3, 5, 5),
('7506495020224', 'Media crema 252gr', 26.00, 20.00, 70, 15, 1, 1, 3),
('7501079016235', 'Italpasta pasta tallarin largo 200 gr', 14.00, 11.00, 90, 25, 6, 6, 3),
('7501005110242', 'Harina Maizena Natural 95Gr', 16.00, 12.00, 75, 20, 6, 6, 3),
('7501052474076', 'Mermelada Clemente Jacques Fresa 470g', 38.00, 30.00, 55, 15, 2, 2, 3),
('7501007445557', 'Jabon Ace 250 gr', 20.00, 15.00, 50, 20, 11, 11,3),
('7501032398071', 'Yogurt Activia 225gr', 15.00, 10.00, 60, 20, 1, 1, 3),
('7501086801046', 'Agua Epura 1l', 15.00, 11.00, 100, 20, 3, 6, 2),
('7501055330690', 'Jugo Del Valle 1l', 30.00, 24.00, 150, 30, 3, 6, 2),
('7500478005833', 'Galletas Bombitos 150gr', 18.00, 14.00, 150, 30, 10, 4, 3),
('7501000140855', 'Galletas Triki-Trakets 85gr', 20.00, 15.00, 90, 20, 10, 4, 3),
('7501000157075', 'Tostadas MilpaReal 360gr', 25.00, 20.00, 100, 15, 6, 7, 3),
('7501011159266', 'Sabritas Receta Crujiente Flaming Hot 70gr', 20.00, 15.00, 300, 50, 7, 10, 3),
('7503028643431', 'Galletas Tartinas Fresa 100gr', 18.00, 15.00, 200, 50, 10, 4, 3),
('7501295600126', 'Leche Santa Clara 1l', 25.00, 23.00, 150, 60, 1, 6, 2),
('7501040027499', 'Salchicha Great Value 500gr', 40.00, 33.00, 150, 20, 12, 9, 3);


INSERT INTO cliente (telefono, nombre, direccion, rfc) VALUES
('999', 'CLIENTE GENERAL', 'Local','RFC1'),
('9611234567', 'María González', 'Tuxtla Gutierrez','RFC2'),
('9612345678', 'Juan Martínez', 'San Cristobal', 'RFC3');

INSERT INTO empleado (id_empleado, nombre, genero, puesto) VALUES
(1, 'Roberto Mendoza Jiménez', 'M', 'administrador'),
(2, 'Adriana López García', 'F', 'encargado'),
(3, 'Fernando Castro Ruiz', 'M', 'cajero');

