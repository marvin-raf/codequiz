# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.21)
# Database: quiz_server
# Generation Time: 2018-07-05 03:36:56 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table answers
# ------------------------------------------------------------

DROP TABLE IF EXISTS `answers`;

CREATE TABLE `answers` (
  `answer_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `answer_question_id` int(11) unsigned NOT NULL,
  `answer_content` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`answer_id`),
  KEY `answer_question_id` (`answer_question_id`),
  CONSTRAINT `answers_ibfk_1` FOREIGN KEY (`answer_question_id`) REFERENCES `questions` (`question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table courses
# ------------------------------------------------------------

DROP TABLE IF EXISTS `courses`;

CREATE TABLE `courses` (
  `course_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `course_teacher_id` int(11) unsigned NOT NULL,
  `course_name` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`course_id`),
  KEY `course_teacher_id` (`course_teacher_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`course_teacher_id`) REFERENCES `teachers` (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table courses_students
# ------------------------------------------------------------

DROP TABLE IF EXISTS `courses_students`;

CREATE TABLE `courses_students` (
  `cs_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `cs_student_id` int(11) unsigned NOT NULL,
  `cs_course_id` int(11) unsigned NOT NULL,
  PRIMARY KEY (`cs_id`),
  KEY `cs_student_id` (`cs_student_id`),
  KEY `cs_course_id` (`cs_course_id`),
  CONSTRAINT `courses_students_ibfk_1` FOREIGN KEY (`cs_student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `courses_students_ibfk_2` FOREIGN KEY (`cs_course_id`) REFERENCES `courses` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table questions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `questions`;

CREATE TABLE `questions` (
  `question_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `question_quiz_id` int(11) unsigned NOT NULL,
  `question_description` varchar(500) NOT NULL DEFAULT '',
  PRIMARY KEY (`question_id`),
  KEY `question_quiz_id` (`question_quiz_id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`question_quiz_id`) REFERENCES `quizzes` (`quiz_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table quizes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `quizes`;

CREATE TABLE `quizes` (
  `quiz_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `quiz_course_id` int(11) NOT NULL,
  `quiz_name` varchar(50) NOT NULL DEFAULT '',
  `quiz_start_date` bigint(11) NOT NULL,
  `quiz_end_date` bigint(11) NOT NULL,
  PRIMARY KEY (`quiz_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table quizzes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `quizzes`;

CREATE TABLE `quizzes` (
  `quiz_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `quiz_course_id` int(11) unsigned NOT NULL,
  `quiz_name` varchar(50) NOT NULL DEFAULT '',
  `quiz_start_date` bigint(11) unsigned NOT NULL,
  `quiz_end_date` bigint(11) unsigned NOT NULL,
  PRIMARY KEY (`quiz_id`),
  KEY `quiz_course_id` (`quiz_course_id`),
  CONSTRAINT `quizzes_ibfk_1` FOREIGN KEY (`quiz_course_id`) REFERENCES `courses` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table students
# ------------------------------------------------------------

DROP TABLE IF EXISTS `students`;

CREATE TABLE `students` (
  `student_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `student_teacher_id` int(11) unsigned NOT NULL,
  `student_name` varchar(50) NOT NULL DEFAULT '',
  `student_email` varchar(128) NOT NULL DEFAULT '',
  `student_hash` varchar(128) DEFAULT '',
  `student_activate_token` varchar(128) NOT NULL DEFAULT '',
  `student_token` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_email` (`student_email`),
  UNIQUE KEY `student_token` (`student_activate_token`),
  UNIQUE KEY `student_hash` (`student_hash`),
  KEY `student_teacher_id` (`student_teacher_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`student_teacher_id`) REFERENCES `teachers` (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table teachers
# ------------------------------------------------------------

DROP TABLE IF EXISTS `teachers`;

CREATE TABLE `teachers` (
  `teacher_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `teacher_name` varchar(50) NOT NULL DEFAULT '',
  `teacher_email` varchar(128) NOT NULL DEFAULT '',
  `teacher_hash` varchar(128) NOT NULL DEFAULT '',
  `teacher_token` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`teacher_id`),
  UNIQUE KEY `teacher_email` (`teacher_email`),
  UNIQUE KEY `teacher_hash` (`teacher_hash`),
  UNIQUE KEY `teacher_token` (`teacher_token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table tests
# ------------------------------------------------------------

DROP TABLE IF EXISTS `tests`;

CREATE TABLE `tests` (
  `test_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `test_question_id` int(11) unsigned NOT NULL,
  `test_input` varchar(256) NOT NULL DEFAULT '',
  `test_expected` varchar(256) NOT NULL DEFAULT '',
  PRIMARY KEY (`test_id`),
  KEY `test_question_id` (`test_question_id`),
  CONSTRAINT `tests_ibfk_1` FOREIGN KEY (`test_question_id`) REFERENCES `questions` (`question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
