CREATE DATABASE  IF NOT EXISTS `ohana_rideshare_schema` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ohana_rideshare_schema`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: ohana_rideshare_schema
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `request_id` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `request_id_UNIQUE` (`request_id`),
  KEY `fk_bookings_users1_idx` (`user_id`),
  KEY `fk_bookings_requests1_idx` (`request_id`),
  CONSTRAINT `fk_bookings_requests` FOREIGN KEY (`request_id`) REFERENCES `requests` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_bookings_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (13,4,5,'2024-06-04 00:56:31','2024-06-04 00:56:31'),(16,1,4,'2024-06-04 01:27:17','2024-06-04 01:27:17'),(23,2,6,'2024-06-04 13:13:56','2024-06-04 13:13:56'),(24,5,7,'2024-06-04 15:26:07','2024-06-04 15:26:07');
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `booking_id` int NOT NULL,
  `user_id` int NOT NULL,
  `content` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_messages_bookings_idx` (`booking_id`),
  KEY `fk_messages_users1_idx` (`user_id`),
  CONSTRAINT `fk_messages_bookings` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_messages_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,23,2,'Still good for the 22nd?','2024-06-04 15:11:40','2024-06-04 15:11:40'),(2,23,5,'Absolutely!','2024-06-04 15:18:46','2024-06-04 15:18:46'),(3,24,2,'Y u change my pikup?','2024-06-04 15:28:44','2024-06-04 15:28:44'),(4,24,5,'I didn\'t know where that was','2024-06-04 15:29:00','2024-06-04 15:29:00'),(5,24,5,'sry','2024-06-04 15:29:09','2024-06-04 15:29:09'),(6,24,2,'its ok','2024-06-04 15:29:20','2024-06-04 15:29:20'),(7,23,2,'Maybe we should keep meeting like this!','2024-06-04 15:32:19','2024-06-04 15:32:19'),(8,23,2,'can i still post?','2024-06-05 10:08:33','2024-06-05 10:08:33'),(9,23,2,'For real tho?','2024-06-05 10:12:13','2024-06-05 10:12:13'),(10,24,2,'I\'m le tired','2024-06-05 10:15:09','2024-06-05 10:15:09'),(11,24,5,'Goodnight!','2024-06-05 10:16:20','2024-06-05 10:16:20');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `requests`
--

DROP TABLE IF EXISTS `requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `destination` varchar(255) DEFAULT NULL,
  `pickup` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `details` varchar(255) DEFAULT NULL,
  `is_booked` tinyint DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_requests_users1_idx` (`user_id`),
  CONSTRAINT `fk_requests_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requests`
--

LOCK TABLES `requests` WRITE;
/*!40000 ALTER TABLE `requests` DISABLE KEYS */;
INSERT INTO `requests` VALUES (1,1,'Miami Airport','Shady Warehouse','1999-11-11','I gotta get my boy Mike!',0,'2024-06-03 22:13:58','2024-06-03 22:13:58'),(2,1,'Abandoned Highrise ','Miami Airport','1999-02-22','Not a drug deal.',0,'2024-06-03 22:15:03','2024-06-03 22:15:03'),(4,3,'Home','Away','1999-11-11','1234567890',0,'2024-06-04 00:06:54','2024-06-04 00:06:54'),(5,3,'Too','Fro','1999-11-11','aasd;flkj;lasdkf',0,'2024-06-04 00:09:25','2024-06-04 00:09:25'),(6,5,'Babysitters Clubhouse','Boxcar Terminal','1999-02-22','Secret meeting ',0,'2024-06-04 09:57:18','2024-06-04 09:57:18'),(7,2,'Outer Space','My house','1999-03-31','Near to Far',0,'2024-06-04 11:14:03','2024-06-04 15:28:37'),(8,5,'Bob\'s Burgers','Jimmy Pesto\'s Pizzeria','2024-06-04','I need a good burger',0,'2024-06-04 15:25:43','2024-06-04 15:25:43');
/*!40000 ALTER TABLE `requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) DEFAULT NULL,
  `last_name` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Chuck','Finley','burn@notice.com','$2b$12$oiGKzz9mJiS4gUuaTU.L6uO9A348OuCgl4bIhizNl0.a.DlLDaDOS','2024-06-03 22:13:13','2024-06-03 22:13:13'),(2,'Michael','Westen','notAspy@user.com','$2b$12$DQKkaWDzoKO0c88SBIJKpuPAKYgzAkh0JPN6s1GwvesKyUDz8TBUK','2024-06-03 22:19:44','2024-06-03 22:19:44'),(3,'Test 83074','User 83074','83074@user.com','$2b$12$xAA2cd.rP5yhVGgaoj5aRevlRPGpW5biGOPIv5JWKaAZP1Y6hqhEa','2024-06-03 22:53:03','2024-06-03 22:53:03'),(4,'Test 59334','User 59334','59334@user.com','$2b$12$LjWyIeTTBJ0pIWsWW5lyd.WJCmE.EoisNatZu9lCGNPiWn4SBMQOi','2024-06-04 00:09:36','2024-06-04 00:09:36'),(5,'Nancy','Drew','mystery@email.com','$2b$12$RZG9WQL2oDpPtD2cejf6Me.NUA.SdjaK60LGkRf129y3MFOfJqZvG','2024-06-04 09:56:19','2024-06-04 09:56:19');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-05 10:18:12
