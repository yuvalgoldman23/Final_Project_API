-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: final_project_db
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `ID` char(12) NOT NULL,
  `User_ID` varchar(20) DEFAULT NULL,
  `TText` varchar(255) DEFAULT NULL,
  `Parent_ID` char(12) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES ('023a2fa3b04a','43534543534','grdrgdr','fdgdrfgdr','2024-06-04 14:15:20'),('04f6fb09717c','43534543534','grdrgdr','fdgdrfgdr','2024-06-04 14:13:57'),('061fa692e695','43534543534','grdrgdr','fdgdrfgdr','2024-06-04 14:20:55'),('43cf94a89388','43534543534','grdrgdr','fdgdrfgdr','2024-06-04 14:19:16'),('4de248c8aad3','43534543534','grdrgdr','fdgdrfgdr','2024-06-04 14:11:06'),('55595e2612fc','43534543534','grdrgdr','fdgdrfgdr','2024-06-04 14:08:10'),('73ab7c8570a1','gergr','gergreg','543543534','2024-05-20 19:40:46'),('75c4e37b2a49','43534543534','grdrgdr','fdgdrfgdr','2024-06-04 14:12:35'),('85558c6ed260','645654yfth','fesfesf','fesfesfse','2024-06-16 17:57:21'),('9b6df38b75ab','43534543534','grdrgdr','fdgdrfgdr','2024-06-04 14:09:56'),('b657b20a1341','43534543534','grdrgdr','fdgdrfgdr','2024-06-04 14:09:19'),('babb82451855','fesfesf','fesfesf','fesfesfse','2024-06-16 17:56:16'),('ce5c1ef1eb92','43534543534','grdrgdr','fdgdrfgdr','2024-06-04 14:16:24'),('cf418ad845c1','123','234','345','2024-06-16 17:08:17'),('e6e8fc7410b0','43534543534','grdrgdr','fdgdrfgdr','2024-05-28 13:40:44'),('fbce9341e612','43534543534','grdrgdr','fdgdrfgdr','2024-06-04 14:17:13');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-16 23:14:42
