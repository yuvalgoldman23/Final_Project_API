-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: final_project_db
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `ID` varchar(12) NOT NULL,
  `User_ID` varchar(100) DEFAULT NULL,
  `Comment` varchar(255) DEFAULT NULL,
  `Parent_ID` varchar(20) DEFAULT NULL,
  `Spoiler` tinyint(1) DEFAULT NULL,
  `timestamp_column` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `befobefore_insert_comments` BEFORE INSERT ON `comments` FOR EACH ROW BEGIN
    DECLARE random_id CHAR(12);
  
    
    -- Generate a unique random string for `id`
    SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    WHILE EXISTS (SELECT 1 FROM `final_project_db`.`watch_lists_names` WHERE ID = random_id) DO
        SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    END WHILE;
    SET NEW.ID = random_id;
    
   
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `feed_items`
--

DROP TABLE IF EXISTS `feed_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feed_items` (
  `ID` varchar(12) NOT NULL,
  `User_ID` varchar(100) DEFAULT NULL,
  `TEXT` varchar(255) DEFAULT NULL,
  `timestamp_column` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feed_items`
--

LOCK TABLES `feed_items` WRITE;
/*!40000 ALTER TABLE `feed_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `feed_items` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `befobefore_insert_feed` BEFORE INSERT ON `feed_items` FOR EACH ROW BEGIN
    DECLARE random_id CHAR(12);
  
    
    -- Generate a unique random string for `id`
    SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    WHILE EXISTS (SELECT 1 FROM `final_project_db`.`watch_lists_names` WHERE ID = random_id) DO
        SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    END WHILE;
    SET NEW.ID = random_id;
    
   
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `likes` (
  `ID` varchar(12) NOT NULL,
  `User_ID` varchar(100) DEFAULT NULL,
  `Target_ID` varchar(12) DEFAULT NULL,
  `Targer_Kind` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `befobefore_insert_likes` BEFORE INSERT ON `likes` FOR EACH ROW BEGIN
    DECLARE random_id CHAR(12);
  
    
    -- Generate a unique random string for `id`
    SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    WHILE EXISTS (SELECT 1 FROM `final_project_db`.`watch_lists_names` WHERE ID = random_id) DO
        SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    END WHILE;
    SET NEW.ID = random_id;
    
   
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `message_text` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,'hello'),(2,'hello'),(7,'hefe'),(8,'hefe');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rating`
--

DROP TABLE IF EXISTS `rating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rating` (
  `ID` varchar(12) NOT NULL,
  `media_ID` varchar(15) NOT NULL,
  `is_movie` tinyint(1) NOT NULL,
  `User_ID` varchar(50) DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `rating_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rating`
--

LOCK TABLES `rating` WRITE;
/*!40000 ALTER TABLE `rating` DISABLE KEYS */;
INSERT INTO `rating` VALUES ('55f6b7f292d7','sdwda',1,'fsfsefs',5,'2024-06-25 15:04:53'),('598e182d72e7','dfsefsef',1,'gergregreg',6,'2024-06-23 15:23:44');
/*!40000 ALTER TABLE `rating` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `befobefore_insert_ratingobject` BEFORE INSERT ON `rating` FOR EACH ROW BEGIN
    DECLARE random_id CHAR(12);
  
    
    -- Generate a unique random string for `id`
    SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    WHILE EXISTS (SELECT 1 FROM `final_project_db`.`rating` WHERE ID = random_id) DO
        SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    END WHILE;
    SET NEW.ID = random_id;
    
   
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

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
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `befobefore_insert_Review` BEFORE INSERT ON `reviews` FOR EACH ROW BEGIN
    DECLARE random_id CHAR(12);
  
    
    -- Generate a unique random string for `id`
    SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    WHILE EXISTS (SELECT 1 FROM `final_project_db`.`watch_lists_names` WHERE ID = random_id) DO
        SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    END WHILE;
    SET NEW.ID = random_id;
    
   
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` varchar(500) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `google_auth` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('1','dani020799','yanovsky','yanovslo1@gmail.com','Daniel','Yanovsky',0),('343423','gregdfe','343423','gregdfe@gmail.com',NULL,NULL,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `watch_list`
--

DROP TABLE IF EXISTS `watch_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `watch_list` (
  `ID` char(12) NOT NULL,
  `Media_ID` varchar(1000) DEFAULT NULL,
  `Owner_ID` char(100) DEFAULT NULL,
  `Is_Movie` tinyint(1) DEFAULT NULL,
  `Watched` tinyint(1) DEFAULT NULL,
  `Rating` float DEFAULT NULL,
  `Comment` varchar(255) DEFAULT NULL,
  `Progress` varchar(20) DEFAULT NULL,
  `Time_Updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `watch_list`
--

LOCK TABLES `watch_list` WRITE;
/*!40000 ALTER TABLE `watch_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `watch_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `watch_lists_names`
--

DROP TABLE IF EXISTS `watch_lists_names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `watch_lists_names` (
  `ID` varchar(120) NOT NULL,
  `User_ID` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `Main` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `watch_lists_names`
--

LOCK TABLES `watch_lists_names` WRITE;
/*!40000 ALTER TABLE `watch_lists_names` DISABLE KEYS */;
INSERT INTO `watch_lists_names` VALUES ('01b2f2e91bfa','543534','fsefe',1),('12345','543534','fsefe',1),('321218876ce8','543534','two',0),('39e2a5d60507','113749586527602021810',NULL,0),('428fe4a2984e','5645','fesf',0),('44c51dd73e52','113749586527602021810',NULL,0),('4b528d2637a8','113749586527602021810',NULL,0),('60bcbc428c76','113749586527602021810',NULL,0),('724651fbb2b5','113749586527602021810',NULL,0),('811cfb2a1d3d','113749586527602021810',NULL,0),('94a159e09303','432423','Main',1),('aeae73d5a54f','113749586527602021810',NULL,0),('b697c90446aa','113749586527602021810',NULL,0),('de09799d1b19','113749586527602021810',NULL,0),('de783625ff61','113749586527602021810',NULL,0),('e30eef47eba1','113749586527602021810',NULL,0),('f11735a4694c','113749586527602021810',NULL,0),('f95ef1aad369','543534','two',0);
/*!40000 ALTER TABLE `watch_lists_names` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `befobefore_insert_watch_lists_names` BEFORE INSERT ON `watch_lists_names` FOR EACH ROW BEGIN
    DECLARE random_id CHAR(12);
  
    
    -- Generate a unique random string for `id`
    SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    WHILE EXISTS (SELECT 1 FROM `final_project_db`.`watch_lists_names` WHERE ID = random_id) DO
        SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    END WHILE;
    SET NEW.ID = random_id;
    
   
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `watch_lists_objects`
--

DROP TABLE IF EXISTS `watch_lists_objects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `watch_lists_objects` (
  `ID` varchar(12) NOT NULL,
  `Parent_ID` varchar(12) DEFAULT NULL,
  `TMDB_ID` varchar(50) DEFAULT NULL,
  `User_ID` varchar(100) DEFAULT NULL,
  `is_movie` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `watch_lists_objects`
--

LOCK TABLES `watch_lists_objects` WRITE;
/*!40000 ALTER TABLE `watch_lists_objects` DISABLE KEYS */;
INSERT INTO `watch_lists_objects` VALUES ('1e313b3a2a17','01b2f2e91bfa','13363-the-man-from-earth','543534',1),('abe2f0b08eda','01b2f2e91bfa','13363-the-man-from-earth','543534',1),('c2e310a3da8a','01b2f2e91bfa','13363-the-man-from-earth','543534',1),('fb98b53d3c93','123','457','83479',NULL);
/*!40000 ALTER TABLE `watch_lists_objects` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `befobefore_insert_watch_list_objects` BEFORE INSERT ON `watch_lists_objects` FOR EACH ROW BEGIN
    DECLARE random_id CHAR(12);
  
    
    -- Generate a unique random string for `id`
    SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    WHILE EXISTS (SELECT 1 FROM `final_project_db`.`watch_lists_names` WHERE ID = random_id) DO
        SET random_id = SUBSTRING(SHA1(RAND()), 1, 12);
    END WHILE;
    SET NEW.ID = random_id;
    
   
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-25 18:15:58
