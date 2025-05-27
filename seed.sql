-- Reset the tables to avoid conflicts (optional, run only if you want to clear existing data)
TRUNCATE TABLE manufacturer, kit, switch, keycap,artisan_keycap,accessory, service RESTART IDENTITY CASCADE;

-- Insert manufacturers first (including keycap manufacturers)
-- This ensures foreign key constraints won't be violated
INSERT INTO manufacturer (id, created_at, updated_at, code, label, logo) VALUES
-- Keyboard manufacturers
(1, '2025-04-22 03:33:00-07', '2025-04-22 03:33:00-07', 'KEYCHRON', 'Keychron', NULL),
(2, '2025-04-22 03:34:00-07', '2025-04-22 03:34:00-07', 'DUCKY', 'Ducky', NULL),
(3, '2025-04-22 03:35:00-07', '2025-04-22 03:35:00-07', 'LEOPOLD', 'Leopold', NULL),
(4, '2025-04-22 03:36:00-07', '2025-04-22 03:36:00-07', 'AKKO', 'Akko', NULL),
(5, '2025-04-22 03:37:00-07', '2025-04-22 03:37:00-07', 'IQUNIX', 'iQunix', NULL),
(6, '2025-04-22 03:38:00-07', '2025-04-22 03:38:00-07', 'DROP', 'Drop', NULL),
(7, '2025-04-22 03:39:00-07', '2025-04-22 03:39:00-07', 'KBDCRAFT', 'KBDCraft', NULL),
(8, '2025-04-22 03:40:00-07', '2025-04-22 03:40:00-07', 'KBDFANS', 'KBDFans', NULL),
(9, '2025-04-22 03:41:00-07', '2025-04-22 03:41:00-07', 'GLORIOUS', 'Glorious', NULL),
(10, '2025-04-22 03:42:00-07', '2025-04-22 03:42:00-07', 'VARMILO', 'Varmilo', NULL),
-- Keycap manufacturers
(11, '2025-04-22 04:03:00-07', '2025-04-22 04:03:00-07', 'GMK', 'GMK', NULL),
(12, '2025-04-22 04:04:00-07', '2025-04-22 04:04:00-07', 'EPBT', 'ePBT', NULL),
(13, '2025-04-22 04:05:00-07', '2025-04-22 04:05:00-07', 'SIGNATURE_PLASTICS', 'Signature Plastics', NULL),
(14, '2025-04-22 04:06:00-07', '2025-04-22 04:06:00-07', 'JTK', 'JTK', NULL),
(15, '2025-04-22 04:07:00-07', '2025-04-22 04:07:00-07', 'KAT', 'KAT', NULL);

-- Inserting data into kit table with VND prices
INSERT INTO kit (
    created_at, updated_at, id, code, name, description, number_of_keys, layout, layout_detail,
    case_spec, mounting_style, plate_material, stab_mount, hot_swap, knob, rgb_type,
    firmware_type, connectivity, dimensions, weight, image, price, manufacturer_id
) VALUES
('2025-04-22 03:43:00-07', '2025-04-22 03:43:00-07', gen_random_uuid(), 'K8PRO', 'Keychron K8 Pro', 'A premium tenkeyless keyboard with wireless connectivity and customizable RGB lighting, ideal for both gaming and typing.', 87, 'Tenkeyless', 'ANSI', 'Aluminum', 'Gasket Mount', 'Polycarbonate', 'Screw-in', true, true, 'Per-key RGB', 'QMK/VIA', 'USB-C, Bluetooth', '359x127x42mm', 1.2, NULL, 3249750, 1),
('2025-04-22 03:44:00-07', '2025-04-22 03:44:00-07', gen_random_uuid(), 'ONE3', 'Ducky One 3', 'A full-size keyboard with vibrant RGB backlighting and a sturdy plastic case, designed for durability and performance.', 104, 'Full-size', 'ISO', 'Plastic', 'Tray Mount', 'Steel', 'Clip-in', true, false, 'Backlit RGB', 'Ducky Firmware', 'USB-C', '440x140x40mm', 1.1, NULL, 3499750, 2),
('2025-04-22 03:45:00-07', '2025-04-22 03:45:00-07', gen_random_uuid(), 'FC750R', 'Leopold FC750R', 'A compact tenkeyless keyboard with a minimalist design, offering a solid typing experience for professionals.', 87, 'Tenkeyless', 'ANSI', 'Plastic', 'Top Mount', 'Steel', 'Screw-in', false, false, 'No RGB', 'Leopold Firmware', 'USB-C', '360x140x33mm', 1.0, NULL, 2999750, 3),
('2025-04-22 03:46:00-07', '2025-04-22 03:46:00-07', gen_random_uuid(), '5108B', 'Akko 5108B', 'A full-size keyboard with wireless capabilities and vibrant RGB lighting, perfect for gamers and enthusiasts.', 108, 'Full-size', 'ANSI', 'Plastic', 'Tray Mount', 'FR4', 'Clip-in', true, false, 'Per-key RGB', 'Akko Firmware', 'USB-C, Bluetooth', '442x132x41mm', 1.3, NULL, 2499750, 4),
('2025-04-22 03:47:00-07', '2025-04-22 03:47:00-07', gen_random_uuid(), 'F12', 'iQunix F12', 'A premium 120% layout keyboard with a split spacebar and aluminum case, designed for enthusiasts seeking a unique typing experience.', 120, '120% Layout', 'ANSI, Split Spacebar', 'Aluminum', 'Gasket Mount', 'Brass', 'Screw-in', false, true, 'Underglow RGB', 'QMK', 'USB-C', '450x150x35mm', 1.5, NULL, 4999750, 5),
('2025-04-22 03:48:00-07', '2025-04-22 03:48:00-07', gen_random_uuid(), 'ENTR', 'Drop Entr', 'A compact tenkeyless keyboard with a minimalist aluminum case, perfect for a clean desk setup.', 87, 'Tenkeyless', 'ANSI', 'Aluminum', 'Tray Mount', 'Steel', 'Clip-in', false, false, 'No RGB', 'Drop Firmware', 'USB-C', '355x127x32mm', 0.9, NULL, 2249750, 6),
('2025-04-22 03:49:00-07', '2025-04-22 03:49:00-07', gen_random_uuid(), 'ADAM', 'KBDCraft Adam', 'A 65% layout keyboard with a unique HHKB-style layout, offering a compact yet versatile typing experience.', 65, '65% Layout', 'HHKB-style', 'Plastic', 'Gasket Mount', 'Polycarbonate', 'Screw-in', true, false, 'Underglow RGB', 'QMK', 'USB-C', '310x110x30mm', 0.7, NULL, 1999750, 7),
('2025-04-22 03:50:00-07', '2025-04-22 03:50:00-07', gen_random_uuid(), 'TOFU60', 'KBDFans Tofu60', 'A 60% layout keyboard with a premium aluminum case, ideal for custom builds and enthusiasts.', 61, '60% Layout', 'ANSI', 'Aluminum', 'Tray Mount', 'Brass', 'Screw-in', false, false, 'No RGB', 'QMK', 'USB-C', '295x105x35mm', 1.0, NULL, 3749750, 8),
('2025-04-22 03:51:00-07', '2025-04-22 03:51:00-07', gen_random_uuid(), 'GMMKPRO', 'Glorious GMMK Pro', 'A 75% layout keyboard with a premium gasket-mounted aluminum case, offering a premium typing experience.', 75, '75% Layout', 'ANSI', 'Aluminum', 'Gasket Mount', 'Polycarbonate', 'Screw-in', true, true, 'Per-key RGB', 'QMK', 'USB-C', '332x132x32mm', 1.4, NULL, 4249750, 9),
('2025-04-22 03:52:00-07', '2025-04-22 03:52:00-07', gen_random_uuid(), 'VA88M', 'Varmilo VA88M', 'A tenkeyless keyboard with a classic design and vibrant RGB backlighting, ideal for both work and play.', 87, 'Tenkeyless', 'ISO', 'Plastic', 'Top Mount', 'Steel', 'Clip-in', false, false, 'Backlit RGB', 'Varmilo Firmware', 'USB-C', '356x134x33mm', 1.1, NULL, 3249750, 10);

-- Inserting data into switch table with VND prices
INSERT INTO switch (
    created_at, updated_at, id, code, name, description, type, actuation_force, bottom_out_force,
    pre_travel, total_travel, sound_level, factory_lubed, stem_material, housing_material,
    pin_type, led_support, led_position, lifespan, compatible_with, image, price_per_switch,
    manufacturer_id
) VALUES
('2025-04-22 03:53:00-07', '2025-04-22 03:53:00-07', gen_random_uuid(), 'GATERON_RED', 'Gateron Red', 'A smooth linear switch with light actuation, ideal for fast typing and gaming.', 'Linear', 45, 55, 2.0, 4.0, 'Quiet', false, 'POM', 'Polycarbonate', '3-pin', true, 'North-facing', 50000000, 'PCB, Plate', NULL, 7500, 1),
('2025-04-22 03:54:00-07', '2025-04-22 03:54:00-07', gen_random_uuid(), 'DUCKY_BROWN', 'Ducky Brown', 'A tactile switch with a moderate bump, offering a balanced typing experience for both work and gaming.', 'Tactile', 55, 65, 2.0, 4.0, 'Medium', true, 'POM', 'Nylon', '3-pin', true, 'South-facing', 60000000, 'PCB, Plate', NULL, 10000, 2),
('2025-04-22 03:55:00-07', '2025-04-22 03:55:00-07', gen_random_uuid(), 'LEOPOLD_BLUE', 'Leopold Blue', 'A clicky switch with a crisp tactile feedback and audible click, perfect for typists who enjoy a pronounced sound.', 'Clicky', 50, 60, 2.2, 4.0, 'Loud', false, 'POM', 'Polycarbonate', '3-pin', true, 'North-facing', 50000000, 'PCB, Plate', NULL, 8750, 3),
('2025-04-22 03:56:00-07', '2025-04-22 03:56:00-07', gen_random_uuid(), 'AKKO_CS_ROSE', 'Akko CS Rose Red', 'A light linear switch with a short travel distance, designed for quick response in gaming.', 'Linear', 43, 55, 1.9, 3.5, 'Quiet', true, 'POM', 'Polycarbonate', '3-pin', true, 'North-facing', 60000000, 'PCB, Plate', NULL, 7000, 4),
('2025-04-22 03:57:00-07', '2025-04-22 03:57:00-07', gen_random_uuid(), 'IQUNIX_GOLD', 'iQunix Gold', 'A tactile switch with a smooth bump and premium feel, ideal for enthusiasts seeking a refined typing experience.', 'Tactile', 50, 60, 2.0, 4.0, 'Medium', true, 'POM', 'Nylon', '5-pin', true, 'South-facing', 70000000, 'PCB, Plate', NULL, 11250, 5),
('2025-04-22 03:58:00-07', '2025-04-22 03:58:00-07', gen_random_uuid(), 'DROP_HALO', 'Drop Halo True', 'A tactile switch with a heavy actuation force, offering a pronounced bump for precise typing.', 'Tactile', 60, 70, 1.9, 4.0, 'Medium', true, 'POM', 'Polycarbonate', '3-pin', true, 'North-facing', 80000000, 'PCB, Plate', NULL, 12500, 6),
('2025-04-22 03:59:00-07', '2025-04-22 03:59:00-07', gen_random_uuid(), 'KBDCRAFT_TTC', 'KBDCraft TTC Gold Pink', 'A light linear switch with a smooth feel, perfect for gamers seeking a quiet and responsive switch.', 'Linear', 37, 50, 2.0, 4.0, 'Quiet', true, 'POM', 'Polycarbonate', '3-pin', true, 'North-facing', 60000000, 'PCB, Plate', NULL, 8000, 7),
('2025-04-22 04:00:00-07', '2025-04-22 04:00:00-07', gen_random_uuid(), 'KBDFANS_GHOST', 'KBDFans Ghost', 'A smooth linear switch with a medium actuation force, designed for a balanced typing and gaming experience.', 'Linear', 48, 58, 2.0, 3.8, 'Quiet', false, 'POM', 'Polycarbonate', '5-pin', true, 'South-facing', 50000000, 'PCB, Plate', NULL, 9500, 8),
('2025-04-22 04:01:00-07', '2025-04-22 04:01:00-07', gen_random_uuid(), 'GLORIOUS_PANDA', 'Glorious Panda', 'A tactile switch with a strong bump and crisp feel, ideal for typists who prefer a tactile feedback.', 'Tactile', 55, 67, 2.0, 4.0, 'Medium', false, 'POM', 'Nylon', '3-pin', true, 'North-facing', 80000000, 'PCB, Plate', NULL, 15000, 9),
('2025-04-22 04:02:00-07', '2025-04-22 04:02:00-07', gen_random_uuid(), 'VARMILO_EC', 'Varmilo EC Daisy', 'A smooth linear switch with a light actuation force, offering a quiet and comfortable typing experience.', 'Linear', 45, 55, 2.0, 4.0, 'Quiet', true, 'POM', 'Polycarbonate', '3-pin', true, 'North-facing', 60000000, 'PCB, Plate', NULL, 13750, 10);

-- Inserting data into keycap table with VND prices
INSERT INTO keycap (
    created_at, updated_at, id, code, name, description, material, profile, legend_type, shine_through,
    compatibility, number_of_keys, layout_support, colorway, theme_name, thickness, texture,
    sound_profile, image, price, manufacturer_id
) VALUES
('2025-04-22 04:08:00-07', '2025-04-22 04:08:00-07', gen_random_uuid(), 'GMK_LASER', 'GMK Laser', 'A vibrant ABS keycap set with a cyberpunk-inspired purple and pink colorway, featuring doubleshot legends for durability.', 'ABS', 'Cherry', 'Doubleshot', true, 'Cherry, Gateron, Kailh', 150, 'ANSI, ISO', 'Purple/Pink', 'Cyberpunk', 1.5, 'Smooth', 'Clacky', NULL, 3499750, 11),
('2025-04-22 04:09:00-07', '2025-04-22 04:09:00-07', gen_random_uuid(), 'EPBT_9009', 'ePBT 9009', 'A retro-inspired PBT keycap set with a beige and grey colorway, featuring dye-sub legends for a textured and durable finish.', 'PBT', 'Cherry', 'Dye-sub', false, 'Cherry, Gateron', 142, 'ANSI, ISO', 'Beige/Grey', 'Retro', 1.4, 'Textured', 'Thocky', NULL, 2749750, 12),
('2025-04-22 04:10:00-07', '2025-04-22 04:10:00-07', gen_random_uuid(), 'SP_DCS', 'Signature Plastics DCS White', 'A classic ABS keycap set with a white and black colorway, featuring doubleshot legends for a clean and timeless look.', 'ABS', 'DCS', 'Doubleshot', false, 'Cherry, Gateron', 130, 'ANSI', 'White/Black', 'Classic', 1.3, 'Smooth', 'Clacky', NULL, 2249750, 13),
('2025-04-22 04:11:00-07', '2025-04-22 04:11:00-07', gen_random_uuid(), 'JTK_NIGHT', 'JTK Night Sakura', 'A beautiful ABS keycap set with a black and pink sakura theme, featuring doubleshot legends for a vibrant and elegant look.', 'ABS', 'Cherry', 'Doubleshot', true, 'Cherry, Gateron', 145, 'ANSI, ISO', 'Black/Pink', 'Sakura', 1.5, 'Smooth', 'Clacky', NULL, 2999750, 14),
('2025-04-22 04:12:00-07', '2025-04-22 04:12:00-07', gen_random_uuid(), 'KAT_MILK', 'KAT Milkshake', 'A pastel-themed PBT keycap set with a white and pink colorway, featuring dye-sub legends for a soft and thocky typing experience.', 'PBT', 'KAT', 'Dye-sub', false, 'Cherry, Gateron', 160, 'ANSI, ISO', 'White/Pink', 'Pastel', 1.4, 'Textured', 'Thocky', NULL, 3249750, 15),
('2025-04-22 04:13:00-07', '2025-04-22 04:13:00-07', gen_random_uuid(), 'AKKO_MAC', 'Akko Macaron', 'A playful PBT keycap set with a pastel blue and green macaron theme, featuring dye-sub legends for a textured and colorful look.', 'PBT', 'OEM', 'Dye-sub', false, 'Cherry, Gateron', 137, 'ANSI, ISO', 'Pastel Blue/Green', 'Macaron', 1.3, 'Textured', 'Thocky', NULL, 1999750, 4),
('2025-04-22 04:14:00-07', '2025-04-22 04:14:00-07', gen_random_uuid(), 'DROP_MT3', 'Drop MT3 Cyber', 'An ABS keycap set with a black and yellow cyber theme, featuring doubleshot legends and a unique MT3 profile for ergonomic typing.', 'ABS', 'MT3', 'Doubleshot', false, 'Cherry, Gateron', 140, 'ANSI', 'Black/Yellow', 'Cyber', 1.5, 'Smooth', 'Clacky', NULL, 2499750, 6),
('2025-04-22 04:15:00-07', '2025-04-22 04:15:00-07', gen_random_uuid(), 'KBDFANS_PBT', 'KBDFans PBT Minimal', 'A minimalist PBT keycap set with a white and grey colorway, featuring dye-sub legends for a clean and thocky typing experience.', 'PBT', 'Cherry', 'Dye-sub', false, 'Cherry, Gateron', 132, 'ANSI, ISO', 'White/Grey', 'Minimalist', 1.4, 'Textured', 'Thocky', NULL, 1749750, 8),
('2025-04-22 04:16:00-07', '2025-04-22 04:16:00-07', gen_random_uuid(), 'GLORIOUS_AURA', 'Glorious Aura V2', 'A transparent polycarbonate keycap set with a clear and black colorway, featuring doubleshot legends for a vibrant and clacky typing experience.', 'Polycarbonate', 'OEM', 'Doubleshot', true, 'Cherry, Gateron', 138, 'ANSI, ISO', 'Clear/Black', 'Transparent', 1.6, 'Smooth', 'Clacky', NULL, 2249750, 9),
('2025-04-22 04:17:00-07', '2025-04-22 04:17:00-07', gen_random_uuid(), 'VARMILO_SAKURA', 'Varmilo Sakura', 'A PBT keycap set with a white and pink sakura theme, featuring dye-sub legends for a textured and elegant typing experience.', 'PBT', 'Cherry', 'Dye-sub', true, 'Cherry, Gateron', 135, 'ANSI, ISO', 'White/Pink', 'Sakura', 1.4, 'Textured', 'Thocky', NULL, 2499750, 10);

-- Inserting data into artisan_keycap table with VND prices
INSERT INTO artisan_keycap (
    created_at, updated_at, id, code, name, artist_name, profile, colorway,
    image, description, price, limited_quantity
) VALUES
('2025-05-24 07:00:00-07', '2025-05-24 07:00:00-07', gen_random_uuid(), 'KPR_ECLIPSE', 'Eclipse Moon', 'Keypora', 'SA', 'Silver/Black', NULL, 'Dark-themed artisan inspired by lunar eclipse.', 749000, 50),
('2025-05-24 07:01:00-07', '2025-05-24 07:01:00-07', gen_random_uuid(), 'DWF_DRAGON', 'Serika Dragon', 'Dwarf Factory', 'Cherry', 'Gold/Red', NULL, 'Dragon-themed sculpt inspired by Eastern mythology.', 1099000, 35),
('2025-05-24 07:02:00-07', '2025-05-24 07:02:00-07', gen_random_uuid(), 'AKU_SAKURA', 'Sakura Blossom', 'ArtKey Universe', 'OEM', 'Pink/White', NULL, 'Soft pastel artisan resembling cherry blossoms.', 890000, 70),
('2025-05-24 07:03:00-07', '2025-05-24 07:03:00-07', gen_random_uuid(), 'SUK_NEON', 'Neon City', 'Suited Up Keycaps', 'DSA', 'Blue/Purple', NULL, 'Cyberpunk styled artisan with glow-in-the-dark resin.', 990000, 40),
('2025-05-24 07:04:00-07', '2025-05-24 07:04:00-07', gen_random_uuid(), 'MNK_GEISHA', 'Geisha Red', 'Monokei', 'SA', 'Red/Black', NULL, 'Traditional Japanese Geisha in bold red outfit.', 1190000, 25),
('2025-05-24 07:05:00-07', '2025-05-24 07:05:00-07', gen_random_uuid(), 'APK_KITSUNE', 'Kitsune Spirit', 'Alpha Keycaps', 'Cherry', 'White/Orange', NULL, 'Fox spirit inspired sculpt with tribal markings.', 1250000, 30),
('2025-05-24 07:06:00-07', '2025-05-24 07:06:00-07', gen_random_uuid(), 'KRT_CLOUD', 'Cloud Nine', 'Keyreative', 'KAT', 'White/Blue', NULL, 'Fluffy cloud design with gradient blue swirls.', 720000, 60),
('2025-05-24 07:07:00-07', '2025-05-24 07:07:00-07', gen_random_uuid(), 'CMS_RUNES', 'Forest Runes', 'Capsmiths', 'OEM', 'Green/Brown', NULL, 'Mystical rune carvings on forest wood resin.', 880000, 45),
('2025-05-24 07:08:00-07', '2025-05-24 07:08:00-07', gen_random_uuid(), 'ZNS_TIGER', 'Cyber Tiger', 'Zion Studios', 'DSA', 'Black/Yellow', NULL, 'Tiger face with cybernetic implants.', 1349000, 20),
('2025-05-24 07:09:00-07', '2025-05-24 07:09:00-07', gen_random_uuid(), 'TMT_UNDERSEA', 'Undersea Orb', 'TinyMakesThings', 'Cherry', 'Blue/Teal', NULL, 'Miniature coral reef encased in epoxy resin.', 1025000, 25);

-- Inserting data into accessory table with VND prices
INSERT INTO accessory (
    created_at, updated_at, id, name, type, description, image, price
) VALUES
('2025-04-22 04:18:00-07', '2025-04-22 04:18:00-07', gen_random_uuid(), 'Coiled USB-C Cable', 'Cable', 'A high-quality coiled USB-C cable, 1.5m when extended, compatible with most mechanical keyboards.', NULL, 499750),
('2025-04-22 04:19:00-07', '2025-04-22 04:19:00-07', gen_random_uuid(), 'Switch Puller Tool', 'Tool', 'A durable stainless steel switch puller for safely removing mechanical keyboard switches.', NULL, 249750),
('2025-04-22 04:20:00-07', '2025-04-22 04:20:00-07', gen_random_uuid(), 'Desk Mat - Minimalist', 'Desk Mat', 'A large desk mat (900x400mm) with a minimalist design, anti-slip base, and smooth surface.', NULL, 749750),
('2025-04-22 04:21:00-07', '2025-04-22 04:21:00-07', gen_random_uuid(), 'Keycap Puller', 'Tool', 'A plastic keycap puller with a wire design to easily remove keycaps without scratching.', NULL, 124750),
('2025-04-22 04:22:00-07', '2025-04-22 04:22:00-07', gen_random_uuid(), 'Wrist Rest - 60% Layout', 'Wrist Rest', 'A memory foam wrist rest for 60% keyboards, covered with soft PU leather, 300x100x20mm.', NULL, 374750);

-- Inserting data into service table with VND prices
INSERT INTO service (
    code, name, description, price
) VALUES
('LUBE_SWITCH', 'Switch Lubing Service', 'Professional lubing service for mechanical keyboard switches using Krytox 205g0 to improve smoothness and reduce scratchiness. Price per switch.', 12500),
('ADD_FOAM', 'Add Foam to Keyboard', 'Adding PE foam and case foam to your keyboard to reduce hollowness and improve sound profile. Suitable for 60%, 65%, 75%, TKL, and full-size layouts.', 625000),
('SWITCH_FILM', 'Switch Filming Service', 'Applying switch films to stabilize switches, reducing wobble and enhancing typing feel. Price per switch, compatible with most 3-pin and 5-pin switches.', 7500),
('STAB_TUNING', 'Stabilizer Tuning Service', 'Tuning stabilizers with lube (Krytox 205g0), band-aid mod, and holee mod to eliminate rattle and improve smoothness. Price per keyboard.', 500000),
('CUSTOM_ASSEMBLY', 'Custom Keyboard Assembly', 'Full assembly of a custom mechanical keyboard, including soldering or hot-swap switch installation, stabilizer tuning, foam addition, and keycap mounting. Does not include parts.', 1250000);
