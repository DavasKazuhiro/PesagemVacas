CREATE DATABASE  IF NOT EXISTS `vacas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `vacas`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: vacas
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alerta`
--

DROP TABLE IF EXISTS `alerta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alerta` (
  `id_alerta` int NOT NULL AUTO_INCREMENT,
  `id_vaca` int NOT NULL,
  `data_hora` datetime DEFAULT NULL,
  `tipo_alerta` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_alerta`),
  KEY `id_vaca` (`id_vaca`),
  CONSTRAINT `alerta_ibfk_1` FOREIGN KEY (`id_vaca`) REFERENCES `vaca` (`id_vaca`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alerta`
--

LOCK TABLES `alerta` WRITE;
/*!40000 ALTER TABLE `alerta` DISABLE KEYS */;
/*!40000 ALTER TABLE `alerta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medida_animal`
--

DROP TABLE IF EXISTS `medida_animal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medida_animal` (
  `id_medida` int NOT NULL AUTO_INCREMENT,
  `id_vaca` int NOT NULL,
  `data_hora` datetime DEFAULT NULL,
  `altura_cm` float DEFAULT NULL,
  `circ_peito_cm` float DEFAULT NULL,
  PRIMARY KEY (`id_medida`),
  KEY `id_vaca` (`id_vaca`),
  CONSTRAINT `medida_animal_ibfk_1` FOREIGN KEY (`id_vaca`) REFERENCES `vaca` (`id_vaca`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medida_animal`
--

LOCK TABLES `medida_animal` WRITE;
/*!40000 ALTER TABLE `medida_animal` DISABLE KEYS */;
/*!40000 ALTER TABLE `medida_animal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pesagem`
--

DROP TABLE IF EXISTS `pesagem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pesagem` (
  `id_pesagem` int NOT NULL AUTO_INCREMENT,
  `data_hora` varchar(50) DEFAULT NULL,
  `valor` float DEFAULT NULL,
  `id_vaca` int NOT NULL,
  PRIMARY KEY (`id_pesagem`),
  KEY `id_vaca` (`id_vaca`),
  CONSTRAINT `pesagem_ibfk_1` FOREIGN KEY (`id_vaca`) REFERENCES `vaca` (`id_vaca`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pesagem`
--

LOCK TABLES `pesagem` WRITE;
/*!40000 ALTER TABLE `pesagem` DISABLE KEYS */;
INSERT INTO `pesagem` VALUES (1,'2025-06-14 01:40:04',640.65,2),(2,'2025-06-14 01:42:11',542.22,2),(3,'2025-06-14 01:45:36',621.13,2);
/*!40000 ALTER TABLE `pesagem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nivel_usuario` varchar(50) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `criado_em` datetime DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vaca`
--

DROP TABLE IF EXISTS `vaca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vaca` (
  `id_vaca` int NOT NULL AUTO_INCREMENT,
  `rfid` varchar(50) DEFAULT NULL,
  `data_nascimento` date DEFAULT NULL,
  `nome` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_vaca`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vaca`
--

LOCK TABLES `vaca` WRITE;
/*!40000 ALTER TABLE `vaca` DISABLE KEYS */;
INSERT INTO `vaca` VALUES (1,'[254, 47, 127, 94, 240]','2021-03-14','Mimosa'),(2,'[134, 72, 25, 126, 169]','2020-07-22','Luzia'),(3,'[140, 55, 18, 145, 230]','2019-11-30','Estrela'),(4,'[138, 70, 20, 110, 210]','2021-01-10','Aurora'),(5,'[133, 74, 29, 120, 250]','2022-05-25','Branquinha'),(6,'[137, 68, 26, 105, 198]','2020-09-09','Pretinha'),(7,'[142, 69, 27, 130, 215]','2021-12-18','Pintada'),(8,'[135, 71, 22, 112, 199]','2018-06-03','Serena'),(9,'[139, 64, 24, 118, 205]','2019-10-16','Nuvem'),(10,'[136, 73, 28, 108, 202]','2020-02-27','Tempestade');
/*!40000 ALTER TABLE `vaca` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-14 14:04:40
