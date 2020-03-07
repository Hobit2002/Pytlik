-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Počítač: localhost
-- Vytvořeno: Sob 07. bře 2020, 18:30
-- Verze serveru: 10.3.21-MariaDB
-- Verze PHP: 5.6.40

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Databáze: `pytlik`
--

-- --------------------------------------------------------

--
-- Struktura tabulky `ActiveUsers`
--

CREATE TABLE `ActiveUsers` (
  `ActiveUser_ID` int(20) NOT NULL,
  `ActiveUser_FirstName` varchar(20) NOT NULL,
  `ActiveUser_OtherNames` varchar(20) NOT NULL,
  `ActiveUser_Password` varchar(30) NOT NULL,
  `ActiveUser_Email` varchar(70) NOT NULL,
  `ActiveUser_Taste` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `ActiveUser_Image` varchar(20) DEFAULT NULL,
  `ActiveUser_Info` text DEFAULT NULL,
  `ActiveUser_Sex` set('Male','Female','Other') DEFAULT NULL,
  `ActiveUser_FirstActive` timestamp NOT NULL DEFAULT current_timestamp(),
  `ActiveUser_LastActive` timestamp NOT NULL DEFAULT current_timestamp(),
  `ActiveUser_Home` set('Metropolis','City','Town','Village','Isolation') DEFAULT NULL,
  `ActiveUser_Birthday` date DEFAULT NULL,
  `ActiveUser_Year` year(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Vyprázdnit tabulku před vkládáním `ActiveUsers`
--

TRUNCATE TABLE `ActiveUsers`;
--
-- Vypisuji data pro tabulku `ActiveUsers`
--

INSERT INTO `ActiveUsers` (`ActiveUser_ID`, `ActiveUser_FirstName`, `ActiveUser_OtherNames`, `ActiveUser_Password`, `ActiveUser_Email`, `ActiveUser_Taste`, `ActiveUser_Image`, `ActiveUser_Info`, `ActiveUser_Sex`, `ActiveUser_FirstActive`, `ActiveUser_LastActive`, `ActiveUser_Home`, `ActiveUser_Birthday`, `ActiveUser_Year`) VALUES
(3, 'David', 'Nadrchal', 'Junák', 'davidnadrchalintj@gmail.com', '', NULL, NULL, NULL, '2020-02-29 17:22:48', '2020-03-07 17:28:36', NULL, NULL, 2002),
(4, 'Píďal', 'Ženatý', 'PravéJá', 'kvokodak@gmail.com', '', NULL, NULL, NULL, '2020-02-29 20:24:23', '2020-02-29 20:24:23', NULL, NULL, 2045),
(5, 'Mr.', 'Quaker', 'lokoko', 'regvqreverqbvhalintj@gmail.com', '', NULL, NULL, NULL, '2020-02-29 20:27:44', '2020-02-29 20:27:44', NULL, NULL, 1999),
(8, 'Davihh', 'Nadrchgh', 'luž', 'zxkrintj@gmail.com', '', NULL, NULL, NULL, '2020-02-29 20:49:39', '2020-02-29 20:49:39', NULL, NULL, 1980),
(9, 'Lou', 'Korona', 'neziju', 'marnice@nebesa.alah', '', NULL, NULL, NULL, '2020-02-29 21:25:10', '2020-02-29 21:25:10', NULL, NULL, 1950),
(14, 'Řako', 'Varchat', 'l', 'luho@jjj.dd', '', NULL, NULL, NULL, '2020-02-29 22:18:09', '2020-02-29 22:18:09', NULL, NULL, 1920),
(15, 'Řacho', 'Lumír', 'belk', 'koala@vyhynuly.heaven', '', NULL, NULL, NULL, '2020-02-29 22:19:30', '2020-02-29 22:19:30', NULL, NULL, 1970),
(17, 'um', 'um', 'ulo', 'um', '', NULL, NULL, NULL, '2020-02-29 22:20:35', '2020-03-02 17:41:28', NULL, NULL, 1999),
(18, 'Lop', 'Lop', 'pedro', 'zehon', '', NULL, NULL, NULL, '2020-02-29 22:22:47', '2020-02-29 22:22:47', NULL, NULL, 1980),
(19, 'Generál', 'Žukov', 'Socialismus', 'lech@sputink.ru', '', NULL, NULL, NULL, '2020-03-01 08:08:53', '2020-03-01 08:08:53', NULL, NULL, 1945),
(20, 'Opol', 'Bulbon', 'Čechov', 'rqeiu', '', NULL, NULL, NULL, '2020-03-01 08:11:10', '2020-03-01 08:11:10', NULL, NULL, 1994),
(21, 'David', 'Nadrchal', 'Já', 'davidnadrchal@gmail.com', '', NULL, NULL, NULL, '2020-03-01 10:48:48', '2020-03-01 10:48:48', NULL, NULL, 2002),
(22, 'Andrej', 'Kiska', 'borec', 'slovak@borec.com', '', NULL, NULL, NULL, '2020-03-01 17:34:30', '2020-03-01 17:34:56', NULL, NULL, 1930),
(23, 'Vasil', 'Blahý', 'židle', 'bliferwij', '', NULL, NULL, NULL, '2020-03-02 08:13:17', '2020-03-02 08:13:17', NULL, NULL, 1915);

-- --------------------------------------------------------

--
-- Struktura tabulky `PasiveUsers`
--

CREATE TABLE `PasiveUsers` (
  `PasiveUser_ID` bigint(20) UNSIGNED NOT NULL,
  `PasiveUser_Nickname` varchar(25) NOT NULL,
  `PasiveUser_Email` varchar(70) NOT NULL,
  `PasiveUser_Taste` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `PasiveUser_Info` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Vyprázdnit tabulku před vkládáním `PasiveUsers`
--

TRUNCATE TABLE `PasiveUsers`;
-- --------------------------------------------------------

--
-- Struktura tabulky `REL_ActiveUsers_PasiveUsers`
--

CREATE TABLE `REL_ActiveUsers_PasiveUsers` (
  `ActiveUser_ID` int(11) NOT NULL,
  `PassiveUser_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Aneb kdo koho může označovat za klienta svých akcí.';

--
-- Vyprázdnit tabulku před vkládáním `REL_ActiveUsers_PasiveUsers`
--

TRUNCATE TABLE `REL_ActiveUsers_PasiveUsers`;
--
-- Vypisuji data pro tabulku `REL_ActiveUsers_PasiveUsers`
--

INSERT INTO `REL_ActiveUsers_PasiveUsers` (`ActiveUser_ID`, `PassiveUser_ID`) VALUES
(3, 4);

-- --------------------------------------------------------

--
-- Struktura tabulky `Session`
--

CREATE TABLE `Session` (
  `Session_EventTime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Session_UserID` int(11) NOT NULL,
  `Session_UserToken` bigint(11) NOT NULL,
  `Session_UserDevice` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Vyprázdnit tabulku před vkládáním `Session`
--

TRUNCATE TABLE `Session`;
--
-- Vypisuji data pro tabulku `Session`
--

INSERT INTO `Session` (`Session_EventTime`, `Session_UserID`, `Session_UserToken`, `Session_UserDevice`) VALUES
('2020-03-07 17:28:36', 3, 31583602117, '127.0.0.1');

--
-- Klíče pro exportované tabulky
--

--
-- Klíče pro tabulku `ActiveUsers`
--
ALTER TABLE `ActiveUsers`
  ADD PRIMARY KEY (`ActiveUser_ID`),
  ADD UNIQUE KEY `ActiveUser_ID` (`ActiveUser_ID`),
  ADD UNIQUE KEY `Key_ActiveUser_Password` (`ActiveUser_Password`),
  ADD UNIQUE KEY `Key_ActiveUser_Email` (`ActiveUser_Email`),
  ADD KEY `Key_ActiveUser_FirstName` (`ActiveUser_FirstName`),
  ADD KEY `Key_ActiveUser_OtherNames` (`ActiveUser_OtherNames`),
  ADD KEY `Key_ActiveUser_LasActivity` (`ActiveUser_LastActive`);

--
-- Klíče pro tabulku `PasiveUsers`
--
ALTER TABLE `PasiveUsers`
  ADD PRIMARY KEY (`PasiveUser_ID`),
  ADD KEY `Key_PasiveUser_Nickname` (`PasiveUser_Nickname`);

--
-- Klíče pro tabulku `REL_ActiveUsers_PasiveUsers`
--
ALTER TABLE `REL_ActiveUsers_PasiveUsers`
  ADD KEY `Key_REL_ActiveUsers_PasiveUsers_ActiveUser` (`ActiveUser_ID`),
  ADD KEY `Key_REL_ActiveUsers_PasiveUsers_PassiveUser` (`PassiveUser_ID`);

--
-- Klíče pro tabulku `Session`
--
ALTER TABLE `Session`
  ADD KEY `Key_Session_EventTime` (`Session_EventTime`),
  ADD KEY `Key_Session_UserToken` (`Session_UserToken`);

--
-- AUTO_INCREMENT pro tabulky
--

--
-- AUTO_INCREMENT pro tabulku `ActiveUsers`
--
ALTER TABLE `ActiveUsers`
  MODIFY `ActiveUser_ID` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT pro tabulku `PasiveUsers`
--
ALTER TABLE `PasiveUsers`
  MODIFY `PasiveUser_ID` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Omezení pro exportované tabulky
--

--
-- Omezení pro tabulku `REL_ActiveUsers_PasiveUsers`
--
ALTER TABLE `REL_ActiveUsers_PasiveUsers`
  ADD CONSTRAINT `ForeignKey_REL_ActiveUsers_PasiveUsers_ActiveUser` FOREIGN KEY (`ActiveUser_ID`) REFERENCES `ActiveUsers` (`ActiveUser_ID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
