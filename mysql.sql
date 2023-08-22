-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Aug 22, 2023 at 07:00 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fastapi`
--

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `id` int NOT NULL,
  `uuid` varchar(64) COLLATE utf8mb4_general_ci NOT NULL,
  `amount` int NOT NULL,
  `currency` text COLLATE utf8mb4_general_ci NOT NULL,
  `time` int NOT NULL,
  `wallet_id` int NOT NULL,
  `service_id` int NOT NULL,
  `status` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`id`, `uuid`, `amount`, `currency`, `time`, `wallet_id`, `service_id`, `status`) VALUES
(7, 'c5c86b12-ed88-450f-ac0a-9a6d875d0d7c', 99, 'TJS', 1692675149, 1, 1, 'success'),
(8, '27422f55-bef8-4237-a498-788a03e75301', 99, 'TJS', 1692675366, 2, 1, 'Insufficient funds'),
(9, 'a7f8aeff-6e8a-4e31-a81b-c781861e9a34', 99, 'TJS', 1692675444, 2, 1, 'Wallet not found'),
(10, 'e4fd74f9-a8c1-4602-b28a-22855d8f6e20', 99, 'TJS', 1692675455, 1, 1, 'insufficient funds'),
(11, '575750ea-f9c3-4f47-b2b2-b0d85060d57e', 0, 'TJS', 1692675534, 1, 2, 'Service not found');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `id` int NOT NULL,
  `earnings` int NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `price` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`id`, `earnings`, `name`, `price`) VALUES
(1, 99, 'Интернет тариф', 99);

-- --------------------------------------------------------

--
-- Table structure for table `wallets`
--

CREATE TABLE `wallets` (
  `id` int NOT NULL,
  `balance` int NOT NULL,
  `currency` text COLLATE utf8mb4_general_ci NOT NULL,
  `owner` varchar(255) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `wallets`
--

INSERT INTO `wallets` (`id`, `balance`, `currency`, `owner`) VALUES
(1, 2400, 'TJS', 'Testzoda Testullo');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD UNIQUE KEY `id` (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `wallets`
--
ALTER TABLE `wallets`
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `wallets`
--
ALTER TABLE `wallets`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
