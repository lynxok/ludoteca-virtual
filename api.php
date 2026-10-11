<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$dataFile = __DIR__ . '/db_data.json';
$gamesFile = __DIR__ . '/games_with_images.json';

if (!file_exists($dataFile)) {
    $initialData = [
        "users" => [
            [
                "id" => 1,
                "username" => "admin",
                "name" => "Maestro de Juegos",
                "avatar" => "warrior_blue",
                "favorite_game" => "Catan",
                "registered_at" => "2026-09-28"
            ]
        ],
        "matches" => []
    ];
    file_put_contents($dataFile, json_encode($initialData, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
}

$action = isset($_GET['action']) ? $_GET['action'] : '';

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if ($action === 'get_data') {
        header('Content-Type: application/json');
        echo file_get_contents($dataFile);
        exit();
    }

    if ($action === 'get_games') {
        header('Content-Type: application/json');
        echo file_get_contents($gamesFile);
        exit();
    }

    // BGG Search proxy / scraper for autocompletion
    if ($action === 'search_bgg') {
        $q = trim($_GET['q'] ?? '');
        if (!$q) {
            echo json_encode(["status" => "error", "items" => []]);
            exit();
        }

        // Search BGG XML API2
        $searchUrl = "https://boardgamegeek.com/xmlapi2/search?type=boardgame&query=" . urlencode($q);
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $searchUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
        curl_setopt($ch, CURLOPT_TIMEOUT, 6);
        $xmlData = curl_exec($ch);
        curl_close($ch);

        $results = [];
        if ($xmlData) {
            $xml = @simplexml_load_string($xmlData);
            if ($xml && isset($xml->item)) {
                $count = 0;
                foreach ($xml->item as $item) {
                    if ($count++ >= 8) break;
                    $bggId = (string)$item['id'];
                    $name = (string)$item->name['value'];
                    $year = isset($item->yearpublished) ? (string)$item->yearpublished['value'] : '';
                    $results[] = [
                        "id" => $bggId,
                        "name" => $name,
                        "year" => $year,
                        "bgg_url" => "https://boardgamegeek.com/boardgame/" . $bggId
                    ];
                }
            }
        }

        header('Content-Type: application/json');
        echo json_encode(["status" => "success", "items" => $results]);
        exit();
    }

    // Fetch detailed game data from BGG ID
    if ($action === 'fetch_bgg_details') {
        $id = trim($_GET['id'] ?? '');
        if (!$id) {
            echo json_encode(["status" => "error", "message" => "ID requerido"]);
            exit();
        }

        $detailUrl = "https://boardgamegeek.com/xmlapi2/thing?stats=1&id=" . urlencode($id);
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $detailUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
        curl_setopt($ch, CURLOPT_TIMEOUT, 8);
        $xmlData = curl_exec($ch);
        curl_close($ch);

        if ($xmlData) {
            $xml = @simplexml_load_string($xmlData);
            if ($xml && isset($xml->item)) {
                $item = $xml->item[0];
                $name = (string)$item->name['value'];
                foreach ($item->name as $n) {
                    if ((string)$n['type'] === 'primary') {
                        $name = (string)$n['value'];
                        break;
                    }
                }
                $image = isset($item->image) ? (string)$item->image : '';
                $minp = isset($item->minplayers) ? (string)$item->minplayers['value'] : '1';
                $maxp = isset($item->maxplayers) ? (string)$item->maxplayers['value'] : '4';
                $playtime = isset($item->playingtime) ? (string)$item->playingtime['value'] : '45';
                $minage = isset($item->minage) ? (string)$item->minage['value'] : '10';

                // Stats
                $rating = '7.0';
                $weight = 2.0;
                if (isset($item->statistics->ratings)) {
                    $ratings = $item->statistics->ratings;
                    if (isset($ratings->average)) $rating = number_format((float)$ratings->average['value'], 1);
                    if (isset($ratings->averageweight)) $weight = round((float)$ratings->averageweight['value'], 2);
                }

                // Rank
                $rank = "Rookie";
                if ($weight >= 4.0) $rank = "Master";
                elseif ($weight >= 3.0) $rank = "Advance";
                elseif ($weight >= 2.0) $rank = "Beginner";

                $desc = isset($item->description) ? html_entity_decode(strip_tags((string)$item->description)) : '';
                $synopsis = mb_substr($desc, 0, 180) . '...';

                header('Content-Type: application/json');
                echo json_encode([
                    "status" => "success",
                    "data" => [
                        "name" => $name,
                        "bgg_id" => (int)$id,
                        "bgg_url" => "https://boardgamegeek.com/boardgame/" . $id,
                        "image" => $image,
                        "players" => ($minp === $maxp) ? $minp : "$minp-$maxp",
                        "playing_time" => $playtime . " Min",
                        "age" => $minage . "+",
                        "rating" => $rating,
                        "weight" => $weight,
                        "rank" => $rank,
                        "type" => "Estrategia / Temático",
                        "synopsis" => $synopsis
                    ]
                ]);
                exit();
            }
        }

        echo json_encode(["status" => "error", "message" => "No se pudo obtener datos"]);
        exit();
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $inputJSON = file_get_contents('php://input');
    $input = json_decode($inputJSON, true);
    $data = json_decode(file_get_contents($dataFile), true);

    if ($action === 'save_game') {
        $games = json_decode(file_get_contents($gamesFile), true);
        $newGame = $input['game'] ?? null;
        if (!$newGame || empty($newGame['name'])) {
            http_response_code(400);
            echo json_encode(["status" => "error", "message" => "Juego invalido"]);
            exit();
        }

        // Assign ID and ranking
        $newGame['id'] = count($games);
        $w = floatval($newGame['weight'] ?? 1.5);
        if ($w >= 4.0) { $newGame['rank'] = "Master"; $newGame['islandId'] = 3; }
        elseif ($w >= 3.0) { $newGame['rank'] = "Advance"; $newGame['islandId'] = 2; }
        elseif ($w >= 2.0) { $newGame['rank'] = "Beginner"; $newGame['islandId'] = 1; }
        else { $newGame['rank'] = "Rookie"; $newGame['islandId'] = 0; }

        if (empty($newGame['scoring'])) {
            $newGame['scoring'] = "• Puntos de Victoria estándar según el manual oficial del juego.";
        }

        $games[] = $newGame;
        file_put_contents($gamesFile, json_encode($games, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

        echo json_encode(["status" => "success", "game" => $newGame, "total" => count($games)]);
        exit();
    }

    if ($action === 'register_user') {
        $username = trim($input['username'] ?? '');
        $name = trim($input['name'] ?? $username);
        $favorite = trim($input['favorite_game'] ?? 'Catan');
        $avatar = trim($input['avatar'] ?? 'warrior_blue');

        if (!$username) {
            http_response_code(400);
            echo json_encode(["status" => "error", "message" => "Nombre de usuario requerido"]);
            exit();
        }

        $userFound = null;
        foreach ($data['users'] as &$u) {
            if (strtolower($u['username']) === strtolower($username)) {
                $u['name'] = $name;
                $u['favorite_game'] = $favorite;
                $u['avatar'] = $avatar;
                $userFound = $u;
                break;
            }
        }

        if (!$userFound) {
            $userFound = [
                "id" => count($data['users']) + 1,
                "username" => $username,
                "name" => $name,
                "avatar" => $avatar,
                "favorite_game" => $favorite,
                "registered_at" => date('Y-m-d')
            ];
            $data['users'][] = $userFound;
        }

        file_put_contents($dataFile, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        echo json_encode(["status" => "success", "user" => $userFound, "users" => $data['users']]);
        exit();
    }

    if ($action === 'add_match') {
        if (!isset($input['game_name']) || !isset($input['players'])) {
            http_response_code(400);
            echo json_encode(["status" => "error", "message" => "Datos incompletos"]);
            exit();
        }

        $newMatch = [
            "id" => count($data['matches']) + 1,
            "game_name" => $input['game_name'],
            "date" => $input['date'] ?? date('Y-m-d'),
            "players" => $input['players'],
            "notes" => $input['notes'] ?? ''
        ];

        $data['matches'][] = $newMatch;
        file_put_contents($dataFile, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

        echo json_encode(["status" => "success", "match" => $newMatch]);
        exit();
    }
}

http_response_code(404);
echo json_encode(["status" => "error", "message" => "Accion no encontrada"]);
?>
