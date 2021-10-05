CREATE TABLE IF NOT EXISTS `test`.`stats` (
    `id` int NOT NULL AUTO_INCREMENT,
    `profile_id` varchar(255) NOT NULL,
    `resource` varchar(25),
    `counts`  int,
    INDEX (id),
    INDEX (profile_id)
);