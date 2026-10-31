<?php
/**
 * Faux serveur n8n pour les tests (php -S 127.0.0.1:<port> tests/faux-n8n.php).
 * Vérifie la signature HMAC comme le nœud Code de WF01, indépendamment de lib/.
 *   /ok     : 200 si la signature est valable, 401 sinon
 *   /panne  : 500
 *   /lent   : attend 3 s puis 200 (test du délai d'attente)
 */
declare(strict_types=1);

$secret = (string) getenv('FAUX_N8N_SECRET');
$journal = (string) getenv('FAUX_N8N_JOURNAL');
$chemin = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);
$corps = (string) file_get_contents('php://input');

header('Content-Type: application/json');
if ($chemin === '/panne') {
    http_response_code(500);
    echo '{"ok":false}';
    return;
}
if ($chemin === '/lent') {
    sleep(3);
}

$horodatage = $_SERVER['HTTP_X_AC_TIMESTAMP'] ?? '';
$signature = $_SERVER['HTTP_X_AC_SIGNATURE'] ?? '';
$attendue = 'sha256=' . hash_hmac('sha256', $horodatage . '.' . $corps, $secret);
$fraicheur = ctype_digit($horodatage) && abs(time() - (int) $horodatage) <= 300;

if (!$fraicheur || !hash_equals($attendue, $signature)) {
    http_response_code(401);
    echo '{"ok":false,"raison":"signature"}';
    return;
}
if ($journal !== '') {
    file_put_contents($journal, $corps . "\n", FILE_APPEND | LOCK_EX);
}
echo '{"ok":true}';
