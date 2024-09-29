/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.5.20-log : Database - analyzing blood donation probabilities
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`analyzing blood donation probabilities` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `analyzing blood donation probabilities`;

/*Table structure for table `awareness program` */

DROP TABLE IF EXISTS `awareness program`;

CREATE TABLE `awareness program` (
  `A_id` int(11) NOT NULL AUTO_INCREMENT,
  `Date` date DEFAULT NULL,
  `Time` varchar(30) DEFAULT NULL,
  `Venue` varchar(20) DEFAULT NULL,
  `Details` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`A_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `awareness program` */

insert  into `awareness program`(`A_id`,`Date`,`Time`,`Venue`,`Details`) values 
(2,'2022-10-04','15:48:00','CAl','Munees');

/*Table structure for table `blood bank` */

DROP TABLE IF EXISTS `blood bank`;

CREATE TABLE `blood bank` (
  `B_id` int(11) NOT NULL AUTO_INCREMENT,
  `Login_id` int(11) DEFAULT NULL,
  `Name` varchar(20) DEFAULT NULL,
  `Place` varchar(20) DEFAULT NULL,
  `Post` varchar(20) DEFAULT NULL,
  `Pin` bigint(20) DEFAULT NULL,
  `Contact` varchar(10) DEFAULT NULL,
  `E-mail` varchar(15) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `latitude` varchar(20) DEFAULT NULL,
  `longitude` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`B_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `blood bank` */

insert  into `blood bank`(`B_id`,`Login_id`,`Name`,`Place`,`Post`,`Pin`,`Contact`,`E-mail`,`Date`,`latitude`,`longitude`) values 
(1,3,'Bloodbank','Perinthalmanna','Kaippuram',679308,'9874563210','athangalparambi','2023-02-26','76.230531','76.230531');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `C_id` int(11) NOT NULL AUTO_INCREMENT,
  `Login_id` int(11) DEFAULT NULL,
  `Complaint` varchar(200) DEFAULT NULL,
  `Date` varchar(50) DEFAULT NULL,
  `reply` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`C_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`C_id`,`Login_id`,`Complaint`,`Date`,`reply`) values 
(1,3,'Muneess','2022-10-06','pending'),
(2,19,'','2022-12-29','pending'),
(3,19,'ook','2022-12-29','pending'),
(4,19,'ook','2022-12-29','pending'),
(5,19,'ook','2022-12-29','pending'),
(6,19,'fdy','2022-12-29','pending'),
(7,19,'','2023-01-02','pending'),
(8,2,'fgg','2023-01-17','pending'),
(9,5,'fff','2023-02-21','pending');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `F_id` int(11) NOT NULL AUTO_INCREMENT,
  `Login_id` int(11) DEFAULT NULL,
  `Feedback` varchar(200) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  PRIMARY KEY (`F_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`F_id`,`Login_id`,`Feedback`,`Date`) values 
(1,3,'bjmnkl','2022-09-14'),
(2,19,'ok','2022-12-29'),
(3,19,'heloo','2022-12-29'),
(4,19,'o','2022-12-29'),
(5,19,'ggh','2022-12-29'),
(6,5,'yygg','2023-02-21');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `Login_id` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(20) DEFAULT NULL,
  `Password` varchar(20) DEFAULT NULL,
  `UserType` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`Login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`Login_id`,`Username`,`Password`,`UserType`) values 
(1,'admin','admin','admin'),
(2,'munees','1234567','user'),
(3,'bloodbank','Bloodbank@123','blood_bank'),
(4,'raheembinshaj','1234567','user');

/*Table structure for table `registration` */

DROP TABLE IF EXISTS `registration`;

CREATE TABLE `registration` (
  `R_id` int(11) NOT NULL AUTO_INCREMENT,
  `Login_id` int(11) DEFAULT NULL,
  `Name` varchar(25) DEFAULT NULL,
  `Gender` varchar(50) DEFAULT NULL,
  `DOB` varchar(50) DEFAULT NULL,
  `Bloodgroup` varchar(10) DEFAULT NULL,
  `Pin` varchar(6) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  `Phone` varchar(10) DEFAULT NULL,
  `Place` varchar(20) DEFAULT NULL,
  `Post` varchar(20) DEFAULT NULL,
  `Longitude` varchar(10) DEFAULT NULL,
  `Latitude` varchar(10) DEFAULT NULL,
  `Image` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`R_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `registration` */

insert  into `registration`(`R_id`,`Login_id`,`Name`,`Gender`,`DOB`,`Bloodgroup`,`Pin`,`Email`,`Phone`,`Place`,`Post`,`Longitude`,`Latitude`,`Image`) values 
(1,2,'Munees','MALE','14/02/2001','A+ve','679308','www.munees001@gmail.com','9037239730','pattambi','pattambi','76.0787789','10.881508','1677406199855.png'),
(2,4,'Raheem','MALE','01/02/2023','A+ve','678905','raheemshaj@gmail.com','9876543210','Tirur','Alathiyur','0','0','1677406786841.png');

/*Table structure for table `request` */

DROP TABLE IF EXISTS `request`;

CREATE TABLE `request` (
  `R_id` int(11) NOT NULL AUTO_INCREMENT,
  `Login_id` int(11) DEFAULT NULL,
  `Blood_Group` varchar(5) DEFAULT NULL,
  `Date` varchar(50) DEFAULT NULL,
  `bbid` int(11) DEFAULT NULL,
  `units` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`R_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

/*Data for the table `request` */

insert  into `request`(`R_id`,`Login_id`,`Blood_Group`,`Date`,`bbid`,`units`,`status`) values 
(1,2,'A+ve','28/02/2023',3,'1','completed'),
(2,3,'A+ve','28/01/2022',5,'1','completed'),
(3,4,'A+ve','22/02/2021',6,'1','completed'),
(4,5,'A+ve','21/02/2022',7,'1','completed'),
(5,6,'A+ve','20/01/2022',8,'1','completed'),
(6,7,'A+ve','20/02/2020',9,'1','completed'),
(7,8,'A+ve','19/02/2019',4,'1','completed'),
(8,9,'A+ve','15/02/2022',11,'1','completed'),
(9,10,'A+ve','14/02/2021',12,'1','completed'),
(10,11,'A+ve','16/02/2021',13,'1','completed'),
(11,12,'A+ve','12/02/2022',14,'2','completed'),
(12,13,'A+ve','12/01/2021',16,'1','completed'),
(13,14,'A+ve','13/01/2022',17,'1','completed'),
(14,2,'A+ve','7/3/2023',3,'12','pending'),
(15,4,'A+ve','',3,'2','rejected'),
(16,4,'A+ve','07/03/2023',3,'2','accepted');

/*Table structure for table `response` */

DROP TABLE IF EXISTS `response`;

CREATE TABLE `response` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `reqid` int(11) DEFAULT NULL,
  `lid` int(11) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

/*Data for the table `response` */

insert  into `response`(`rid`,`reqid`,`lid`,`date`,`status`) values 
(1,1,4,'2023-02-26','accepted'),
(2,2,4,'2022-01-28','accepted'),
(3,3,4,'2021-02-22','accepted'),
(4,4,4,'2022-02-21','accepted'),
(5,5,4,'2022-01-21','accepted'),
(6,6,4,'2020-02-20','accepted'),
(7,7,4,'2019-02-19','accepted'),
(8,8,4,'2022-02-15','accepted'),
(9,9,10,'2021-02-15','accepted'),
(10,10,11,'2021-02-17','accepted'),
(11,11,12,'2022-02-12','accepted'),
(12,12,13,'2021-01-12','accepted'),
(13,13,14,'2022-01-14','accepted'),
(14,16,2,'2023-03-06','pending');

/*Table structure for table `tips` */

DROP TABLE IF EXISTS `tips`;

CREATE TABLE `tips` (
  `T_id` int(11) NOT NULL AUTO_INCREMENT,
  `Tip` varchar(150) DEFAULT NULL,
  `Date` varchar(50) DEFAULT NULL,
  `Details` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`T_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `tips` */

insert  into `tips`(`T_id`,`Tip`,`Date`,`Details`) values 
(8,'HEloo','2022-11-11','Goodevening'),
(10,'helo','2022-11-11','haai'),
(11,'ansartp','2022-11-11','pop');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `u_id` int(11) NOT NULL AUTO_INCREMENT,
  `l_id` int(11) DEFAULT NULL,
  `Name` varchar(20) NOT NULL,
  `Gender` varchar(10) NOT NULL,
  `Blood group` varchar(4) NOT NULL,
  `E-mail` varchar(30) DEFAULT NULL,
  `Contact` varchar(10) NOT NULL,
  `Place` varchar(25) NOT NULL,
  `Post` varchar(25) NOT NULL,
  `Pin` int(6) NOT NULL,
  `Image` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`u_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `user` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
