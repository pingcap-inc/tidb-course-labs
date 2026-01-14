-- MySQL dump 10.13  Distrib 8.4.7, for macos15 (arm64)
--
-- Host: 127.0.0.1    Database: shop
-- ------------------------------------------------------
-- Server version	8.4.7

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
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Tom','tom@tidb.com','2026-01-07 18:47:46','tom','A',NULL,NULL,NULL),(2,'Jack','jack@tidb.com','2026-01-07 18:48:43','jack','G',NULL,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `pay_type`
--

LOCK TABLES `pay_type` WRITE;
/*!40000 ALTER TABLE `pay_type` DISABLE KEYS */;
INSERT INTO `pay_type` VALUES (1,'Credit Card'),(2,'Debit Card'),(3,'Online Banking'),(4,'COD'),(5,'Prepaid Cards'),(6,'Gift Cards'),(7,'Cryptocurrency');
/*!40000 ALTER TABLE `pay_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `product_type`
--

LOCK TABLES `product_type` WRITE;
/*!40000 ALTER TABLE `product_type` DISABLE KEYS */;
INSERT INTO `product_type` VALUES (1,'No Category'),(2,'Kids'),(3,'Life'),(4,'Science & Technology'),(5,'Education & Reference'),(6,'Humanities & Social Sciences'),(7,'Magazine'),(8,'Comics'),(9,'Arts'),(10,'Sports'),(11,'Novel');
/*!40000 ALTER TABLE `product_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'S','The Sign','Deciphering the universe\'s most mysterious radio signals to answer the ultimate question: Are we alone?','/assets/images/695eaf5788d3e.png',138.97,38,'2026-01-07 11:06:41','2026-01-07 11:09:11',4),(2,'S','The Last Dance','Master the psychology of endings and transitions to finish strong in your career, business, and life.','/assets/images/695eb08251689.png',39.27,11,'2026-01-07 11:13:16','2026-01-07 11:14:10',5),(3,'S','Earth Angel','A fallen angel navigates the gritty streets of New York in this noir-inspired graphic novel of redemption.','/assets/images/695eb0cdec342.png',194.68,117,'2026-01-07 11:14:24','2026-01-07 11:15:26',8),(4,'S','Eve of Destruction','The essential quarterly journal for modern survivalists, analyzing global tipping points, cyber-warfare, and geopolitical risks.','/assets/images/695eb12952185.png',108.12,74,'2026-01-07 11:15:45','2026-01-07 11:16:57',7),(5,'S','Leader of the Pack','A lost wolf discovers that true leadership comes from the heart in this heartwarming winter adventure.','/assets/images/695eb1709ab94.png',56.32,1,'2026-01-07 11:17:12','2026-01-07 11:18:08',2),(6,'S','Sugar Sugar','A shocking exposé on the history, chemistry, and health impacts of the world’s most addictive substance: sucrose.','/assets/images/695eb1ceb1dd6.png',23.07,79,'2026-01-07 11:18:19','2026-01-07 11:19:42',5),(7,'S','One Bad Apple','In a perfect gated community, one neighbor\'s dirty secret threatens to rot the whole bunch. A razor-sharp thriller.','/assets/images/695eb216bafc9.png',191.90,747,'2026-01-07 11:19:49','2026-01-07 11:20:54',11),(8,'S','White Christmas','Reclaim the holiday magic with minimalist decor, cozy recipes, and stress-free tips for a serene winter season.','/assets/images/695eb26081b90.png',64.54,19,'2026-01-07 11:21:11','2026-01-07 11:22:08',3),(9,'S','Hey There','An interactive board book full of rhymes and flaps to teach toddlers social cues and animal sounds.','/assets/images/695eb2b2a3256.png',98.98,188,'2026-01-07 11:22:33','2026-01-07 11:23:30',2),(10,'S','The Way You Move','The premier lifestyle magazine celebrating the art of kinetics, biomechanics, and the sheer joy of physical expression.','/assets/images/695eb304b2ff9.png',9.84,720,'2026-01-07 11:23:43','2026-01-07 11:24:52',7),(11,'S','Look Back','Revisit the past choices and explores how memory reshapes the present.','/assets/images/695eb34b4867b.png',12.17,97,'2026-01-07 11:25:02','2026-01-07 11:26:03',3),(12,'S','ABC','Complex corporate strategies broken down into 26 clear, illustrated principles for the aspiring entrepreneur.','/assets/images/695eb3b016f42.png',74.95,118,'2026-01-07 11:26:22','2026-01-07 11:27:44',5);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-08  3:29:31
