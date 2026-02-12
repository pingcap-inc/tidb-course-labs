-- Seed data for Mshop (demo_206). Use after running Django migrations.
-- For users, create via Django: python manage.py createsuperuser (or insert into auth_user if needed).
-- Tables product_type, pay_type, products must exist (from migrate).

SET NAMES utf8mb4;

INSERT INTO `pay_type` (`id`, `type`) VALUES
(1,'Credit Card'),(2,'Debit Card'),(3,'Online Banking'),(4,'COD'),(5,'Prepaid Cards'),(6,'Gift Cards'),(7,'Cryptocurrency')
ON DUPLICATE KEY UPDATE `type`=VALUES(`type`);

INSERT INTO `product_type` (`id`, `type`) VALUES
(1,'No Category'),(2,'Kids'),(3,'Life'),(4,'Science & Technology'),(5,'Education & Reference'),(6,'Humanities & Social Sciences'),(7,'Magazine'),(8,'Comics'),(9,'Arts'),(10,'Sports'),(11,'Novel')
ON DUPLICATE KEY UPDATE `type`=VALUES(`type`);

INSERT INTO `products` (`id`, `status`, `name`, `introduction`, `photo`, `price`, `remain_count`, `created_at`, `updated_at`, `product_type`) VALUES
(1,'S','The Sign','Deciphering the universe''s most mysterious radio signals to answer the ultimate question: Are we alone?','/assets/images/69515903eec4f.png',138.97,38,NOW(),NOW(),4),
(2,'S','The Last Dance','Master the psychology of endings and transitions to finish strong in your career, business, and life.','/assets/images/69515952c65b2.png',39.27,11,NOW(),NOW(),5),
(3,'S','Earth Angel','A fallen angel navigates the gritty streets of New York in this noir-inspired graphic novel of redemption.','/assets/images/695159f2e61ae.png',194.68,117,NOW(),NOW(),8),
(4,'S','Eve of Destruction','The essential quarterly journal for modern survivalists, analyzing global tipping points, cyber-warfare, and geopolitical risks.','/assets/images/69515a52219e2.png',108.12,74,NOW(),NOW(),7),
(5,'S','Leader of the Pack','A lost wolf discovers that true leadership comes from the heart in this heartwarming winter adventure.','/assets/images/6951d319a62a3.png',56.32,1,NOW(),NOW(),2),
(6,'S','Sugar Sugar','A shocking exposé on the history, chemistry, and health impacts of the world''s most addictive substance: sucrose.','/assets/images/69575ee63b97b.png',23.07,79,NOW(),NOW(),5),
(7,'S','One Bad Apple','In a perfect gated community, one neighbor''s dirty secret threatens to rot the whole bunch. A razor-sharp thriller.','/assets/images/69575e439e01c.png',191.90,747,NOW(),NOW(),11),
(8,'S','White Christmas','Reclaim the holiday magic with minimalist decor, cozy recipes, and stress-free tips for a serene winter season.','/assets/images/695347a82c2a5.png',64.54,19,NOW(),NOW(),3),
(9,'S','Hey There','An interactive board book full of rhymes and flaps to teach toddlers social cues and animal sounds.','/assets/images/6951d4f807426.png',98.98,188,NOW(),NOW(),2),
(10,'S','The Way You Move','The premier lifestyle magazine celebrating the art of kinetics, biomechanics, and the sheer joy of physical expression.','/assets/images/6951d5b515df9.png',9.84,720,NOW(),NOW(),7),
(11,'S','Thrift Shop','A vintage coat with a hidden love letter sparks a charming mystery about the stories we leave behind.','/assets/images/6951e7df23ef7.png',180.9,20,NOW(),NOW(),11),
(12,'S','Waterfalls','Adrenaline-fueled accounts of the extreme kayakers who risk it all to conquer the world''s most dangerous drops.','/assets/images/6951e11db6b14.png',74.95,118,NOW(),NOW(),10)
ON DUPLICATE KEY UPDATE `name`=VALUES(`name`), `price`=VALUES(`price`), `remain_count`=VALUES(`remain_count`);
