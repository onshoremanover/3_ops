/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.10-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: lukaspe1_my_db
-- ------------------------------------------------------
-- Server version	10.11.10-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `change_tbl`
--

DROP TABLE IF EXISTS `change_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `change_tbl` (
  `change_id` int(11) NOT NULL AUTO_INCREMENT,
  `crq_nr` varchar(30) NOT NULL,
  `timer` int(11) NOT NULL,
  `comment` varchar(70) DEFAULT NULL,
  `review` enum('good','neutral','bad') DEFAULT NULL,
  PRIMARY KEY (`change_id`),
  UNIQUE KEY `crq_nr` (`crq_nr`)
) ENGINE=MyISAM AUTO_INCREMENT=104 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `change_tbl`
--

LOCK TABLES `change_tbl` WRITE;
/*!40000 ALTER TABLE `change_tbl` DISABLE KEYS */;
/*!40000 ALTER TABLE `change_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat`
--

DROP TABLE IF EXISTS `chat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(300) NOT NULL,
  `user` varchar(30) NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`message_id`)
) ENGINE=MyISAM AUTO_INCREMENT=144 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat`
--

LOCK TABLES `chat` WRITE;
/*!40000 ALTER TABLE `chat` DISABLE KEYS */;
INSERT INTO `chat` VALUES
(112,'Hoi','Lukas','2021-10-04 19:48:07'),
(111,'Super Chat2','zchatz','2021-10-04 19:48:05'),
(110,'Super Chat','zchatz','2021-10-04 19:47:50'),
(108,'Hoi LuÂ¨','zchatz','2021-10-04 19:47:25'),
(106,'Nocheinmal ein Test','1','2021-10-04 18:05:47'),
(109,'Super Chat','zchatz','2021-10-04 19:47:48'),
(103,'Hallo Pa','Lukas','2021-10-04 16:50:45'),
(102,'','testuser','2021-10-04 16:49:04'),
(113,'Das ist eine lange Nachricht welche ich noch nicht genau bestimmen kann, ob sie auch wirklich funktioniert','','2021-10-04 23:36:48'),
(114,'Test','Lukas','2021-10-27 12:49:29'),
(115,'Test with Lynx','Lukas','2021-11-01 16:13:58'),
(116,'Test with Lxny 2','Lukas','2021-11-01 16:14:47'),
(117,'Test with Lynx 3','Lukas','2021-11-01 16:36:37'),
(118,'Test with Lynx 3','Lukas','2021-11-01 16:36:42'),
(119,'','Lukas','2021-11-01 16:36:58'),
(120,'','Lukas','2021-11-01 16:37:08'),
(121,'','Lukas','2021-11-01 16:37:14'),
(122,'Test with Lynx 4','Lukas','2021-11-01 16:37:33'),
(123,'Test with Lynx 4','Lukas','2021-11-01 16:37:41'),
(124,'','Lukas','2021-11-01 16:37:47'),
(125,'','Lukas','2021-11-01 16:37:51'),
(126,'','Lukas','2021-11-01 16:37:54'),
(127,'','Lukas','2021-11-01 16:37:54'),
(128,'Test with Lynx 5','Lukas','2021-11-01 16:41:05'),
(129,'Test with Lynx 5','Lukas','2021-11-01 16:41:10'),
(130,'Test with Mac','Lukas','2021-11-01 16:41:24'),
(131,'Test with Mac','Lukas','2021-11-01 16:41:26'),
(132,'Tested with Mac','Lukas','2021-11-01 20:05:23'),
(133,'te','Lukas','2021-11-01 20:05:40'),
(134,'boba','Lukas','2021-11-01 20:10:15'),
(135,'boba','Lukas','2021-11-01 20:10:57'),
(136,'boba','Lukas','2021-11-01 20:11:01'),
(137,'ka','Lukas','2021-11-01 20:11:21'),
(138,'test','Lukas','2021-12-09 10:35:18'),
(139,'test','testuser','2022-01-05 13:32:59'),
(140,'test','testuser','2022-01-05 13:33:01'),
(141,'test3','testuser','2022-01-05 13:33:09'),
(142,'testing','testuser','2022-02-17 11:36:26'),
(143,'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','testuser','2022-08-23 22:07:28');
/*!40000 ALTER TABLE `chat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_users`
--

DROP TABLE IF EXISTS `chat_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(30) NOT NULL,
  `user_pw` varchar(200) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_users`
--

LOCK TABLES `chat_users` WRITE;
/*!40000 ALTER TABLE `chat_users` DISABLE KEYS */;
INSERT INTO `chat_users` VALUES
(5,'testuser','$2y$10$w4FRHrJd81FKQ8xV9mjktu8q.tWVGcC6l7hTvGCG9sH.TWOTe3sKK'),
(13,'','$2y$10$pyAOauJrgPr00r5QQwRNsu/vYLEP8gmsu2fQ3zdZ/5sbK6dCcKajy'),
(11,'pek','$2y$10$IuKnbzmeNghyvMCM3YFHfeD0urmxD8RR3EzkXibUkdgUwLSPqVxNO'),
(12,'boba','$2y$10$8yq8qFRG8/4r7/zc2cqioet6LhRVjc2cxK2jznIczvuhZvGjyB5bq');
/*!40000 ALTER TABLE `chat_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persons`
--

DROP TABLE IF EXISTS `persons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persons` (
  `change_id` int(11) NOT NULL AUTO_INCREMENT,
  `crq_nr` varchar(30) NOT NULL,
  `timer` int(11) NOT NULL,
  `comment` varchar(70) DEFAULT NULL,
  `review` enum('good','neutral','bad') DEFAULT NULL,
  PRIMARY KEY (`change_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persons`
--

LOCK TABLES `persons` WRITE;
/*!40000 ALTER TABLE `persons` DISABLE KEYS */;
/*!40000 ALTER TABLE `persons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(30) NOT NULL,
  `user_pw` varchar(200) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(23,'PEK','$2y$10$5NACIMbz05iaI04uK/kiGuH7yCJ4.1iO/fsKHWXMrpstMXwqXRR2u'),
(22,'','$2y$10$Z.o.TGE4P/vkQQyBhNBeruuyoqfMHUDbLPyTj/mT3HVM8bmyUqohq'),
(21,'Lukas','$2y$10$VMxnL7TK/K7qTs54Nxs1cOR5YjtB0JR04knOPFOrNVclrmXv35zke');
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

-- Dump completed on 2025-01-21  9:52:11
