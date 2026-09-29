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
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $inputJSON = file_get_contents('php://input');
    $input = json_decode($inputJSON, true);
    $data = json_decode(file_get_contents($dataFile), true);

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

        // Check if user exists
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

    if ($action === 'delete_user') {
        $userId = intval($input['id'] ?? 0);
        $data['users'] = array_values(array_filter($data['users'], function($u) use ($userId) {
            return $u['id'] !== $userId;
        }));
        file_put_contents($dataFile, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        echo json_encode(["status" => "success", "users" => $data['users']]);
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
