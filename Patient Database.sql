-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 13, 2022 at 02:58 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `medicine_box`
--

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `Time` datetime NOT NULL,
  `Room_No` varchar(255) NOT NULL,
  `Bed_location` varchar(1) NOT NULL,
  `Patient_ID` int(255) NOT NULL,
  `First_name` varchar(255) NOT NULL,
  `Last_name` varchar(255) NOT NULL,
  `Error` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`Time`, `Room_No`, `Bed_location`, `Patient_ID`, `First_name`, `Last_name`, `Error`) VALUES
('2022-03-13 11:54:45', '1', 'D', 3, 'Micheal', 'Scott', 0),
('2022-03-13 19:50:16', '1', 'D', 3, 'Micheal', 'Scott', 0);

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `Patient_ID` int(255) NOT NULL,
  `First_name` varchar(255) NOT NULL,
  `Last_name` varchar(255) NOT NULL,
  `Disease` varchar(255) NOT NULL,
  `Age` int(255) NOT NULL,
  `Gender` varchar(1) NOT NULL,
  `Prescription_ID` varchar(255) NOT NULL,
  `Doctor_email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`Patient_ID`, `First_name`, `Last_name`, `Disease`, `Age`, `Gender`, `Prescription_ID`, `Doctor_email`) VALUES
(1, 'See', 'Sheng Ting', 'Fever', 22, 'M', 'P1001', ''),
(2, 'David', 'Levinson', 'Diarrheal', 26, 'M', 'P1002', ''),
(3, 'Micheal', 'Scott', 'Covid-19', 33, 'F', 'P1003', ''),
(4, 'Angela', 'Martin', 'Dengue', 42, 'F', 'P1005', ''),
(5, 'Kelly ', 'Kapoor', 'Covid-19', 17, 'F', 'P1003', ''),
(6, 'Josh', 'Porter', 'Diarrheal', 28, 'M', 'P1002', ''),
(7, 'Andy', 'Bernard', 'Influence', 50, 'F', 'P1004', ''),
(8, 'Jim', 'Halpert', 'Influence', 66, 'M', 'P1005', '');

-- --------------------------------------------------------

--
-- Table structure for table `prescription`
--

CREATE TABLE `prescription` (
  `Prescription_ID` varchar(255) NOT NULL,
  `Antibiotic` int(255) DEFAULT NULL,
  `Panadol` int(255) DEFAULT NULL,
  `Painkiller` int(255) DEFAULT NULL,
  `Disease` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `prescription`
--

INSERT INTO `prescription` (`Prescription_ID`, `Antibiotic`, `Panadol`, `Painkiller`, `Disease`) VALUES
('P1001', 1, 2, 0, 'Fever'),
('P1002', 2, 1, 2, 'Diarrheal'),
('P1003', 2, 2, 2, 'Covid-19'),
('P1004', 1, 3, 0, 'Influenza'),
('P1005', 2, 3, 1, 'Dengue');

-- --------------------------------------------------------

--
-- Table structure for table `room`
--

CREATE TABLE `room` (
  `Room_No` varchar(255) NOT NULL,
  `Bed_location` varchar(1) NOT NULL,
  `Patient_ID` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `room`
--

INSERT INTO `room` (`Room_No`, `Bed_location`, `Patient_ID`) VALUES
('2', 'C', 1),
('2', 'B', 2),
('1', 'D', 3),
('1', 'B', 4),
('1', 'C', 5),
('2', 'D', 6),
('2', 'A', 7),
('1', 'A', 8);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`Time`),
  ADD KEY `Patient_ID` (`Patient_ID`),
  ADD KEY `Room_No` (`Room_No`,`Bed_location`);

--
-- Indexes for table `patient`
--
ALTER TABLE `patient`
  ADD PRIMARY KEY (`Patient_ID`),
  ADD KEY `Prescription_ID` (`Prescription_ID`);

--
-- Indexes for table `prescription`
--
ALTER TABLE `prescription`
  ADD PRIMARY KEY (`Prescription_ID`);

--
-- Indexes for table `room`
--
ALTER TABLE `room`
  ADD PRIMARY KEY (`Room_No`,`Bed_location`),
  ADD KEY `Patient_ID` (`Patient_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `patient`
--
ALTER TABLE `patient`
  MODIFY `Patient_ID` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `event`
--
ALTER TABLE `event`
  ADD CONSTRAINT `Event_ibfk_1` FOREIGN KEY (`Patient_ID`) REFERENCES `patient` (`Patient_ID`),
  ADD CONSTRAINT `Event_ibfk_2` FOREIGN KEY (`Room_No`,`Bed_location`) REFERENCES `room` (`Room_No`, `Bed_location`);

--
-- Constraints for table `patient`
--
ALTER TABLE `patient`
  ADD CONSTRAINT `Patient_ibfk_1` FOREIGN KEY (`Prescription_ID`) REFERENCES `prescription` (`Prescription_ID`);

--
-- Constraints for table `room`
--
ALTER TABLE `room`
  ADD CONSTRAINT `Room_ibfk_1` FOREIGN KEY (`Patient_ID`) REFERENCES `patient` (`Patient_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
