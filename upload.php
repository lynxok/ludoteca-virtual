<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $filename = isset($_GET['filename']) ? basename($_GET['filename']) : null;
    
    if (!$filename) {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "Falta parametro filename"]);
        exit();
    }

    $uploadDir = __DIR__ . '/portadas/';
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0755, true);
    }

    $targetFile = $uploadDir . $filename;
    $inputData = file_get_contents('php://input');

    if ($inputData && strlen($inputData) > 0) {
        if (file_put_contents($targetFile, $inputData) !== false) {
            http_response_code(200);
            echo json_encode(["status" => "success", "filename" => $filename]);
            exit();
        }
    }

    // Fallback for multipart form data
    if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
        if (move_uploaded_file($_FILES['file']['tmp_name'], $targetFile)) {
            http_response_code(200);
            echo json_encode(["status" => "success", "filename" => $filename]);
            exit();
        }
    }

    http_response_code(500);
    echo json_encode(["status" => "error", "message" => "No se pudo guardar el archivo"]);
    exit();
}

http_response_code(405);
echo json_encode(["status" => "error", "message" => "Metodo no permitido"]);
?>
