-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.32-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para agentechatbot
CREATE DATABASE IF NOT EXISTS `agentechatbot` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `agentechatbot`;

-- Volcando estructura para tabla agentechatbot.agenda
CREATE TABLE IF NOT EXISTS `agenda` (
  `id` int(11) NOT NULL,
  `paciente_documento` int(11) DEFAULT NULL,
  `profesional_id` int(11) DEFAULT NULL,
  `dia_semana` varchar(10) DEFAULT NULL,
  `hora_inicio` time DEFAULT NULL,
  `hora_fin` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `paciente_documento` (`paciente_documento`),
  KEY `profesional_id` (`profesional_id`),
  CONSTRAINT `agenda_ibfk_1` FOREIGN KEY (`paciente_documento`) REFERENCES `paciente` (`documento`),
  CONSTRAINT `agenda_ibfk_2` FOREIGN KEY (`profesional_id`) REFERENCES `profesionales` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla agentechatbot.agenda: ~15 rows (aproximadamente)
INSERT IGNORE INTO `agenda` (`id`, `paciente_documento`, `profesional_id`, `dia_semana`, `hora_inicio`, `hora_fin`) VALUES
	(1, 1005232345, 1, 'Lunes', '09:00:00', '09:30:00'),
	(9, 1005030299, 10, 'Viernes', '09:00:00', '09:30:00'),
	(10, 1005987654, 10, 'Viernes', '09:00:00', '09:30:00'),
	(11, 1005239087, 11, 'Lunes', '10:00:00', '10:30:00'),
	(13, 12345678, 13, 'Miércoles', '08:00:00', '08:30:00'),
	(14, 1005777890, 14, 'Jueves', '10:30:00', '11:00:00'),
	(16, 1005030299, 25, 'Viernes', '16:30:00', '17:00:00'),
	(17, 1005030299, 19, 'Jueves', '09:00:00', '09:30:00'),
	(19, 1005412345, 21, 'Lunes', '13:00:00', '13:30:00'),
	(23, 1005345679, 25, 'Viernes', '11:30:00', '12:00:00'),
	(26, 1005987654, 7, 'Jueves', '14:30:00', '15:00:00'),
	(27, 1005232345, 8, 'Viernes', '09:00:00', '09:30:00'),
	(29, 1005412345, 19, 'Jueves', '10:30:00', '11:00:00'),
	(30, 1005239087, 21, 'Martes', '12:00:00', '12:30:00'),
	(33, 1005987654, 25, 'Viernes', '17:00:00', '17:30:00');

-- Volcando estructura para tabla agentechatbot.cups
CREATE TABLE IF NOT EXISTS `cups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo_cup` int(11) NOT NULL,
  `procedimiento` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla agentechatbot.cups: ~97 rows (aproximadamente)
INSERT IGNORE INTO `cups` (`id`, `codigo_cup`, `procedimiento`) VALUES
	(1, 890201, 'CONSULTA DE PRIMERA VEZ POR MEDICINA GENERAL'),
	(2, 890202, 'CONSULTA DE PRIMERA VEZ POR OTRAS ESPECIALIDADES MÉDICAS'),
	(3, 890203, 'CONSULTA DE PRIMERA VEZ POR ODONTOLOGÍA GENERAL'),
	(4, 890204, 'CONSULTA DE PRIMERA VEZ POR OTRAS ESPECIALIDADES EN ODONTOLOGIA'),
	(5, 890205, 'CONSULTA DE PRIMERA VEZ POR ENFERMERÍA'),
	(6, 890206, 'CONSULTA DE PRIMERA VEZ POR NUTRICIÓN Y DIETÉTICA'),
	(7, 890207, 'CONSULTA DE PRIMERA VEZ POR OPTOMETRÍA'),
	(8, 890208, 'CONSULTA DE PRIMERA VEZ POR PSICOLOGÍA'),
	(9, 890209, 'CONSULTA DE PRIMERA VEZ POR TRABAJO SOCIAL'),
	(10, 890210, 'CONSULTA DE PRIMERA VEZ POR FONOAUDIOLOGÍA'),
	(11, 890211, 'CONSULTA DE PRIMERA VEZ POR FISIOTERAPIA'),
	(12, 890212, 'CONSULTA DE PRIMERA VEZ POR TERAPIA RESPIRATORIA'),
	(13, 890213, 'CONSULTA DE PRIMERA VEZ POR TERAPIA OCUPACIONAL'),
	(14, 890214, 'CONSULTA DE PRIMERA VEZ POR TERAPIAS ALTERNATIVAS'),
	(15, 890215, 'CONSULTA DE PRIMERA VEZ POR EQUIPO INTERDISCIPLINARIO'),
	(16, 890216, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN SALUD FAMILIAR Y COMUNITARIA'),
	(17, 890217, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CIRUGÍA ORAL'),
	(18, 890218, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ENDODONCIA'),
	(19, 890219, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ESTOMATOLOGÍA Y CIRUGÍA ORAL'),
	(20, 890220, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ODONTOPEDIATRÍA'),
	(21, 890221, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN PERIODONCIA'),
	(22, 890222, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ORTODONCIA'),
	(23, 890223, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN RADIOLOGÍA ORAL Y MAXILOFACIAL'),
	(24, 890224, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN REHABILITACIÓN ORAL'),
	(25, 890225, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ALERGOLOGÍA'),
	(26, 890226, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ANESTESIOLOGÍA'),
	(27, 890227, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ANESTESIOLOGÍA CARDIOVASCULAR'),
	(28, 890228, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CARDIOLOGÍA'),
	(29, 890229, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CARDIOLOGÍA PEDIÁTRICA'),
	(30, 890230, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CIRUGÍA CARDIOVASCULAR'),
	(31, 890231, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CIRUGÍA DE CABEZA Y CUELLO'),
	(32, 890232, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CIRUGÍA DE MAMA Y TUMORES DE TEJIDOS BLANDOS'),
	(33, 890233, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CIRUGÍA DE TÓRAX'),
	(34, 890234, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CIRUGÍA GASTROINTESTINAL'),
	(35, 890235, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CIRUGÍA GENERAL'),
	(36, 890236, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CIRUGÍA MAXILOFACIAL'),
	(37, 890237, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CIRUGÍA ONCOLÓGICA'),
	(38, 890238, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CIRUGÍA PEDIÁTRICA'),
	(39, 890239, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CIRUGÍA PLÁSTICA, ESTÉTICA Y RECONSTRUCTIVA'),
	(40, 890240, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN CIRUGÍA VASCULAR'),
	(41, 890241, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN COLOPROCTOLOGÍA'),
	(42, 890242, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN DERMATOLOGÍA'),
	(43, 890243, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN DOLOR Y CUIDADOS PALIATIVOS'),
	(44, 890244, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ENDOCRINOLOGÍA'),
	(45, 890245, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ENDOCRINOLOGÍA PEDIÁTRICA'),
	(46, 890246, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN GASTROENTEROLOGÍA'),
	(47, 890247, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN GASTROENTEROLOGÍA PEDIÁTRICA'),
	(48, 890248, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN GENÉTICA MÉDICA'),
	(49, 890249, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN GERIATRÍA'),
	(50, 890250, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN GINECOLOGÍA Y OBSTETRICIA'),
	(51, 890251, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN HEMATOLOGÍA'),
	(52, 890252, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN HEMATOLOGÍA PEDIÁTRICA'),
	(53, 890253, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN HEPATOLOGÍA'),
	(54, 890254, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN INFECTOLOGÍA'),
	(55, 890255, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MASTOLOGÍA'),
	(56, 890256, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA AEROESPACIAL'),
	(57, 890257, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA ALTERNATIVA (AYURVEDA)'),
	(58, 890258, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA ALTERNATIVA (HOMEOPÁTICA)'),
	(59, 890259, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA ALTERNATIVA (MEDICINA TRADICIONAL CHINA)'),
	(60, 890260, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA ALTERNATIVA (NATUROPATÍA)'),
	(61, 890261, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA DEL DEPORTE'),
	(62, 890262, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA DEL TRABAJO O SEGURIDAD Y SALUD EN EL TRABAJO'),
	(63, 890263, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA FAMILIAR'),
	(64, 890264, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA FÍSICA Y REHABILITACIÓN'),
	(65, 890265, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA FORENSE'),
	(66, 890266, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA INTERNA'),
	(67, 890267, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA NUCLEAR'),
	(68, 890268, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN NEFROLOGÍA'),
	(69, 890269, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN NEFROLOGÍA PEDIÁTRICA'),
	(70, 890270, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN NEONATOLOGÍA'),
	(71, 890271, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN NEUMOLOGÍA'),
	(72, 890272, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN NEUMOLOGÍA PEDIÁTRICA'),
	(73, 890273, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN NEUROCIRUGÍA'),
	(74, 890274, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN NEUROLOGÍA'),
	(75, 890275, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN NEUROLOGÍA PEDIÁTRICA'),
	(76, 890276, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN OFTALMOLOGÍA'),
	(77, 890277, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ONCOHEMATOLOGÍA PEDIÁTRICA'),
	(78, 890278, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ONCOLOGÍA'),
	(79, 890279, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ONCOLOGÍA PEDIÁTRICA'),
	(80, 890280, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ORTOPEDIA Y TRAUMATOLOGÍA'),
	(81, 890281, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN ORTOPEDIA Y TRAUMATOLOGÍA PEDIÁTRICA'),
	(82, 890282, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN OTORRINOLARINGOLOGÍA'),
	(83, 890283, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN PEDIATRÍA'),
	(84, 890284, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN PSIQUIATRÍA'),
	(85, 890285, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN PSIQUIATRÍA PEDIÁTRICA'),
	(86, 890286, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN RADIOLOGÍA E IMÁGENES DIAGNÓSTICAS'),
	(87, 890287, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN RADIOTERAPIA'),
	(88, 890288, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN REUMATOLOGÍA'),
	(89, 890289, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN REUMATOLOGÍA PEDIÁTRICA'),
	(90, 890290, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN SEXOLOGÍA CLÍNICA'),
	(91, 890291, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN TOXICOLOGÍA CLÍNICA'),
	(92, 890292, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN TRASPLANTES'),
	(93, 890294, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN UROLOGÍA'),
	(94, 890295, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA ALTERNATIVA (OSTEOPÁTICA)'),
	(95, 890296, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA ALTERNATIVA (NEURALTERAPÉUTICA)'),
	(96, 890297, 'CONSULTA DE PRIMERA VEZ POR OTRAS ESPECIALIDADES DE PSICOLOGÍA'),
	(97, 890298, 'CONSULTA DE PRIMERA VEZ POR ESPECIALISTA EN MEDICINA ESTÉTICA');

-- Volcando estructura para tabla agentechatbot.disponibilidad
CREATE TABLE IF NOT EXISTS `disponibilidad` (
  `id` int(11) NOT NULL,
  `profesional_id` int(11) DEFAULT NULL,
  `dia_semana` varchar(10) DEFAULT NULL,
  `hora_inicio` time DEFAULT NULL,
  `hora_fin` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `profesional_id` (`profesional_id`),
  CONSTRAINT `disponibilidad_ibfk_1` FOREIGN KEY (`profesional_id`) REFERENCES `profesionales` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla agentechatbot.disponibilidad: ~16 rows (aproximadamente)
INSERT IGNORE INTO `disponibilidad` (`id`, `profesional_id`, `dia_semana`, `hora_inicio`, `hora_fin`) VALUES
	(3, 3, 'Miércoles', '08:00:00', '08:30:00'),
	(4, 4, 'Jueves', '11:00:00', '11:30:00'),
	(5, 7, 'Martes', '12:00:00', '12:30:00'),
	(6, 8, 'Miércoles', '09:00:00', '09:30:00'),
	(8, 8, 'Miércoles', '15:00:00', '15:30:00'),
	(12, 12, 'Martes', '13:00:00', '13:30:00'),
	(15, 15, 'Viernes', '12:00:00', '12:30:00'),
	(18, 20, 'Viernes', '08:00:00', '08:30:00'),
	(20, 22, 'Martes', '09:00:00', '09:30:00'),
	(21, 23, 'Miércoles', '08:00:00', '08:30:00'),
	(22, 25, 'Viernes', '11:00:00', '11:30:00'),
	(24, 25, 'Viernes', '12:00:00', '12:30:00'),
	(25, 25, 'Viernes', '16:00:00', '16:30:00'),
	(28, 13, 'Lunes', '14:00:00', '14:30:00'),
	(31, 22, 'Lunes', '13:00:00', '13:30:00'),
	(32, 25, 'Viernes', '17:30:00', '18:00:00');

-- Volcando estructura para tabla agentechatbot.paciente
CREATE TABLE IF NOT EXISTS `paciente` (
  `documento` int(11) NOT NULL DEFAULT 0,
  `nombre` varchar(255) NOT NULL,
  `tipoDocumento` varchar(10) NOT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla agentechatbot.paciente: ~9 rows (aproximadamente)
INSERT IGNORE INTO `paciente` (`documento`, `nombre`, `tipoDocumento`, `correo`, `direccion`, `telefono`, `password`) VALUES
	(12345678, 'Juan Pérez', 'CC', 'juan@example.com', 'Calle Falsa 123', '555-1234', 'juan123'),
	(1005030299, 'Anderson Castellanos', 'CC', 'anderson@example.com', 'Calle Falsa 123', '555-1234', 'anderson123'),
	(1005232345, 'Guillermo Ruiz', 'CC', 'juan.perez@example.com', 'Avenida Central 202', '320-654-9870', '123456'),
	(1005239087, 'Luis Rodríguez', 'CC', 'luis.rodriguez@example.com', 'Calle Norte 12 #34-56', '310-987-6543', '123456'),
	(1005345679, 'María López', 'CC', 'maria.lopez@example.com', 'Carrera 15 #23-45', '311-223-3344', '123456'),
	(1005412345, 'Pedro García', 'CC', 'pedro.garcia@example.com', 'Calle 50 #10-20', '313-567-8901', '123456'),
	(1005777890, 'Carolina Sánchez', 'CC', 'carolina.sanchez@example.com', 'Avenida Sur 45 #67-89', '314-876-5432', '123456'),
	(1005987654, 'Mario Andres', 'CC', 'anderson.araque@example.com', 'Calle Principal 101', '321-456-7890', '123456');

-- Volcando estructura para tabla agentechatbot.profesionales
CREATE TABLE IF NOT EXISTS `profesionales` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `especialidad` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Volcando datos para la tabla agentechatbot.profesionales: ~25 rows (aproximadamente)
INSERT IGNORE INTO `profesionales` (`id`, `nombre`, `especialidad`) VALUES
	(1, 'Dr Federico Cordero', 'Consulta de Primera Vez por Especialista en Cardiología'),
	(2, 'Dra Cristina Medina', 'Consulta de Primera Vez por Especialista en Psiquiatría'),
	(3, 'Dr Carlos Martínez', 'Consulta de Primera Vez por Psicología'),
	(4, 'Dr Marco Antonio', 'Consulta de Primera Vez por Ginecología y Obstetricia'),
	(5, 'Dr Felipe Sánchez', 'Consulta de Primera Vez por Terapia Respiratoria'),
	(6, 'Dra Carmen Jiménez', 'Consulta de Primera Vez por Fisioterapia'),
	(7, 'Dr Javier Salazar', 'Consulta de Primera Vez por Cirugía General'),
	(8, 'Dr Oscar García', 'Consulta de Primera Vez por Especialista en Gastroenterología'),
	(9, 'Dra Patricia Núñez', 'Consulta de Primera Vez por Especialista en Urología'),
	(10, 'Dra Laura Gómez', 'Consulta de Primera Vez por Odontología General'),
	(11, 'Dr Luis Martínez', 'Consulta de Primera Vez por Especialista en Endocrinología'),
	(12, 'Dra Isabel Ortega', 'Consulta de Primera Vez por Especialista en Medicina Alternativa'),
	(13, 'Dr Andrés Soto', 'Consulta de Primera Vez por Especialista en Oncología'),
	(14, 'Dra Silvia Paredes', 'Consulta de Primera Vez por Dermatología'),
	(15, 'Dra Nadia Torres', 'Consulta de Primera Vez por Especialista en Hematología'),
	(16, 'Dra Valentina López', 'Consulta de Primera Vez por Especialista en Otorrinolaringología'),
	(17, 'Dr Alberto Castillo', 'Consulta de Primera Vez por Especialista en Medicina del Trabajo'),
	(18, 'Dr Ricardo Peña', 'Consulta de Primera Vez por Especialista en Geriatría'),
	(19, 'Dra Mónica Ruiz', 'Consulta de Primera Vez por Especialista en Reumatología'),
	(20, 'Dr Leonardo Castro', 'Consulta de Primera Vez por Especialista en Medicina Interna'),
	(21, 'Dra Mariana Pérez', 'Consulta de Primera Vez por Especialista en Cirugía Plástica'),
	(22, 'Dr Esteban Ramírez', 'Consulta de Primera Vez por Especialista en Medicina Forense'),
	(23, 'Dra Ana Herrera', 'Consulta de Primera Vez por Nutrición y Dietética'),
	(24, 'Dr Juan Pérez', 'Consulta de Primera Vez por Medicina General'),
	(25, 'Dra Paula Ríos', 'Consulta de Primera Vez por Pediatría');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
