<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$dataFile = __DIR__ . '/db_data.json';

if (!file_exists($dataFile)) {
    $initialData = [
        "users" => [
            ["id" => 1, "username" => "admin", "name" => "Maestro de Juegos", "avatar" => "warrior_blue"]
        ],
        "matches" => [
            [
                "id" => 1,
                "game_name" => "Catan",
                "date" => "2026-09-28",
                "players" => [
                    ["name" => "Jugador 1", "score" => 10, "winner" => true],
                    ["name" => "Jugador 2", "score" => 8, "winner" => false],
                    ["name" => "Jugador 3", "score" => 6, "winner" => false]
                ],
                "notes" => "Partida inaugural en el reino"
            ]
        ]
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
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $inputJSON = file_get_contents('php://input');
    $input = json_decode($inputJSON, true);
    $data = json_decode(file_get_contents($dataFile), true);

    if ($action === 'login') {
        $username = trim($input['username'] ?? '');
        if (!$username) {
            http_response_code(400);
            echo json_encode(["status" => "error", "message" => "Nombre requerido"]);
            exit();
        }

        // Find or create user
        $userFound = null;
        foreach ($data['users'] as $u) {
            if (strtolower($u['username']) === strtolower($username)) {
                $userFound = $u;
                break;
            }
        }

        if (!$userFound) {
            $userFound = [
                "id" => count($data['users']) + 1,
                "username" => $username,
                "name" => $username,
                "avatar" => "warrior_blue"
            ];
            $data['users'][] = $userFound;
            file_put_contents($dataFile, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        }

        echo json_encode(["status" => "success", "user" => $userFound]);
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
