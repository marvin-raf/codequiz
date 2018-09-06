# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.21)
# Database: quiz_server
# Generation Time: 2018-09-06 02:08:26 +0000
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
  `answer_content` varchar(256) DEFAULT NULL,
  `answer_test_id` int(11) unsigned NOT NULL,
  `answer_attempt_id` int(11) unsigned NOT NULL,
  PRIMARY KEY (`answer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table attempts
# ------------------------------------------------------------

DROP TABLE IF EXISTS `attempts`;

CREATE TABLE `attempts` (
  `attempt_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `attempt_question_id` int(11) unsigned NOT NULL,
  `attempt_student_id` int(11) unsigned NOT NULL,
  PRIMARY KEY (`attempt_id`),
  KEY `attempt_question_id` (`attempt_question_id`),
  KEY `attempt_student_id` (`attempt_student_id`),
  CONSTRAINT `attempts_ibfk_1` FOREIGN KEY (`attempt_question_id`) REFERENCES `questions` (`question_id`),
  CONSTRAINT `attempts_ibfk_2` FOREIGN KEY (`attempt_student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table classes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `classes`;

CREATE TABLE `classes` (
  `class_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `class_name` varchar(50) NOT NULL DEFAULT '',
  `class_teacher_id` int(11) NOT NULL,
  PRIMARY KEY (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table classes_courses
# ------------------------------------------------------------

DROP TABLE IF EXISTS `classes_courses`;

CREATE TABLE `classes_courses` (
  `cc_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `cc_class_id` int(11) NOT NULL,
  `cc_course_id` int(11) NOT NULL,
  PRIMARY KEY (`cc_id`)
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



# Dump of table languages
# ------------------------------------------------------------

DROP TABLE IF EXISTS `languages`;

CREATE TABLE `languages` (
  `language_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `language_name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`language_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `languages` WRITE;
/*!40000 ALTER TABLE `languages` DISABLE KEYS */;

INSERT INTO `languages` (`language_id`, `language_name`)
VALUES
	(1,'Python');

/*!40000 ALTER TABLE `languages` ENABLE KEYS */;
UNLOCK TABLES;


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

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;

INSERT INTO `questions` (`question_id`, `question_quiz_id`, `question_description`)
VALUES
	(5,1,'Write a function `hello_world()` that returns \"Hello World!\"\n\n(Note: make sure you\'re returning \"Hello World!\" instead of printing)'),
	(6,1,'Write a function `multiply(num1, num2)` that returns the product of `num1` and `num2`'),
	(7,1,'Write a function `concat(str1, str2)` that joins two strings and adds a space in between them'),
	(8,1,'Write a function `n_strings(str1, n)` that returns a string that is `n` copies of `str1`\n\n(Note: you don\'t need any loops for this question)'),
	(9,1,'Write a function `hypotenuse(a, b)` that returns the length of the hypotenuse of a triangle with length `a` and width `b`'),
	(10,2,'Write a function `is_even(num1)` that returns `True` if `num1` is even and `False` if not'),
	(12,2,'Write a function `count_down(n)` that prints every integer from `n` to `0`'),
	(13,2,'Write a function `step_back(n)` that counts from `n` to `0` and\n- Decreases by `3` when its even\n- Increases by `1` when its odd'),
	(14,2,'Write a function `fizz_buzz(n)` that loops from `1` to `n` and:\n- Prints `Fizz` when `n` is divisible by `3`\n- Prints `Buzz` when `n` is divisible by `5`\n- Prints `FizzBuzz` when `n` is divisible by both `3` and `5`\n- Prints `n` otherwise'),
	(16,2,'Write a function `prime_numbers(n)` that prints out all of the prime numbers up to `n`'),
	(17,3,'Write a function `concat(str1, str2)` that joins two strings and adds a space in between them'),
	(18,3,'Write a function `reverse_string(str1)` that returns `str1` reversed'),
	(19,3,'Write a function `remove_letter(str1, letter)` that returns `str1` with all copies of that letter removed'),
	(20,3,'Write a function `is_palindrome(str1)` that returns `True` if `str1` is a palindrome and `False` if not\n(Note: a palindrome is a word that reads the same way from both directions)'),
	(21,3,'Write a function `is_anagram(\"str1\", \"str2\")` that returns `True` if `str2` is an anagram of `str1` and `False` otherwise\n(Note: an anagram is a word formed by rearranging the letters of another word)'),
	(23,4,'Write a function `swap_ends(list1)` that returns `list1` with its ends swapped'),
	(24,4,'Write a function `total_list(list1)` that returns the result of adding all of its elements together'),
	(25,4,'Write a function `convert_to_string(list1)` that returns `list1` converted to a string'),
	(26,4,'Write a function `remove_duplicates(list1)` that returns a list with all values removed that are found in `list1` more than once'),
	(27,4,'Write a function `merge(list1, list2)` that returns a list of `list1` and `list2` merged together');

/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table quizzes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `quizzes`;

CREATE TABLE `quizzes` (
  `quiz_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `quiz_course_id` int(11) unsigned DEFAULT NULL,
  `quiz_name` varchar(30) NOT NULL DEFAULT '',
  `quiz_start_date` bigint(11) unsigned DEFAULT NULL,
  `quiz_end_date` bigint(11) unsigned DEFAULT NULL,
  `quiz_language_id` int(11) unsigned DEFAULT NULL,
  `quiz_short_desc` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`quiz_id`),
  KEY `quiz_course_id` (`quiz_course_id`),
  KEY `quiz_language_id` (`quiz_language_id`),
  CONSTRAINT `quizzes_ibfk_1` FOREIGN KEY (`quiz_course_id`) REFERENCES `courses` (`course_id`),
  CONSTRAINT `quizzes_ibfk_2` FOREIGN KEY (`quiz_language_id`) REFERENCES `languages` (`language_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `quizzes` WRITE;
/*!40000 ALTER TABLE `quizzes` DISABLE KEYS */;

INSERT INTO `quizzes` (`quiz_id`, `quiz_course_id`, `quiz_name`, `quiz_start_date`, `quiz_end_date`, `quiz_language_id`, `quiz_short_desc`)
VALUES
	(1,NULL,'Functions',NULL,NULL,1,'A brief introduction to functions'),
	(2,NULL,'Conditionals and loops',NULL,NULL,1,'A brief introduction to conditionals and loops'),
	(3,NULL,'Strings',NULL,NULL,1,'A brief introduction to strings'),
	(4,NULL,'Lists',NULL,NULL,1,'A brief introduction to lists');

/*!40000 ALTER TABLE `quizzes` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table students
# ------------------------------------------------------------

DROP TABLE IF EXISTS `students`;

CREATE TABLE `students` (
  `student_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `student_teacher_id` int(11) unsigned NOT NULL,
  `student_name` varchar(50) NOT NULL DEFAULT '',
  `student_email` varchar(128) NOT NULL DEFAULT '',
  `student_hash` varchar(128) NOT NULL DEFAULT '',
  `student_activate_token` varchar(128) NOT NULL DEFAULT '',
  `student_token` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_email` (`student_email`),
  UNIQUE KEY `student_hash` (`student_hash`),
  UNIQUE KEY `student_token` (`student_activate_token`),
  KEY `student_teacher_id` (`student_teacher_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`student_teacher_id`) REFERENCES `teachers` (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table students_classes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `students_classes`;

CREATE TABLE `students_classes` (
  `sc_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `sc_student_id` int(11) NOT NULL,
  `sc_class_id` int(11) NOT NULL,
  PRIMARY KEY (`sc_id`)
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
  `teacher_is_admin` tinyint(1) NOT NULL DEFAULT '0',
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

LOCK TABLES `tests` WRITE;
/*!40000 ALTER TABLE `tests` DISABLE KEYS */;

INSERT INTO `tests` (`test_id`, `test_question_id`, `test_input`, `test_expected`)
VALUES
	(3,5,'print(hello_world())','Hello World!'),
	(5,6,'print(multiply(3, 2))','6'),
	(6,6,'print(multiply(2, -1))','-2'),
	(7,7,'print(concat(\"Hello\", \"World!\"))','Hello World!'),
	(8,7,'print(concat(\"First\", \"Second\"))','First Second'),
	(9,8,'print(n_strings(\"Three\", 3))','ThreeThreeThree'),
	(10,8,'print(n_strings(\"Repeat\", 2))','RepeatRepeat'),
	(11,9,'print(hypotenuse(3, 4))','5'),
	(12,9,'print(hypotenuse(5, 12))','13'),
	(13,10,'print(is_even(1))','False'),
	(14,10,'print(is_even(2))','True'),
	(17,12,'count_down(3)','3\n2\n1\n0'),
	(19,12,'count_down(5)','5\n4\n3\n2\n1\n0'),
	(20,14,'fizz_buzz(5)','1\n2\nFizz\n4\nBuzz'),
	(21,14,'fizz_buzz(15)','1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz'),
	(22,13,'step_back(8)','8\n5\n6\n3\n4\n1\n2'),
	(23,13,'step_back(7)','7\n8\n5\n6\n3\n4\n1\n2'),
	(24,16,'prime_numbers(10)','2\n3\n5\n7'),
	(25,16,'prime_numbers(50)','2\n3\n5\n7\n11\n13\n17\n19\n23\n29\n31\n37\n41\n43\n47'),
	(26,17,'print(concat(\"Hello\", \"World!\"))','Hello World!'),
	(27,17,'print(concat(\"First\", \"Second\"))','First Second'),
	(28,18,'print(reverse_string(\"desserts\"))','stressed'),
	(29,18,'print(reverse_string(\"live\"))','evil'),
	(30,19,'print(remove_letter(\"Hello World!\", \"l\"))','Heo Word!'),
	(31,19,'print(remove_letter(\"Remove\", \"R\"))','emove'),
	(32,20,'print(is_palindrome(\"racecar\"))','True'),
	(34,20,'print(is_palindrome(\"palindrome\"))','False'),
	(37,21,'print(is_anagram(\"restful\", \"fluster\"))','True'),
	(39,21,'print(is_anagram(\"anagram\", \"palindrome\"))','False'),
	(42,23,'print(swap_ends([1, 2, 3, 4]))','[4, 2, 3, 1]'),
	(43,23,'print(swap_ends([\"a\", \"b\", \"c\"]))','[\"c\", \"b\", \"a\"]'),
	(44,24,'print(total_list([1, 2, 3, 4]))','10'),
	(45,24,'print(total_list([1, -1, 0]))','0'),
	(46,25,'print(convert_to_string([\"F\", \"o\", \"o\"]))','Foo'),
	(47,25,'print(convert_to_string[2, 0, 1, 8]))','2018'),
	(48,26,'print(remove_duplicates([1, 2, 2, 5, 5, 3]))','[1, 3]'),
	(49,26,'print(remove_duplicates([1, 1]))','[]'),
	(51,27,'print(merge([1, 3, 5, 7], [2, 4, 6, 8]))','[1, 2, 3, 4, 5, 6, 7, 8]'),
	(52,27,'print(merge([1, 2], [1, 2, 3, 4, 5]))','[1, 1, 2, 2, 3, 4, 5]');

/*!40000 ALTER TABLE `tests` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
