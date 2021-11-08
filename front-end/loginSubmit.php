<?php
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}
$username=$_POST["username"];
$password=$_POST["password"];
include_once("models/user.php");
include_once("models/token.php");
include_once("constants/constants.php");
$urlToken = $serverAddress."token/";
$data = array('username' => $username, 'password' => $password);
$options = array(
    'http' => array(
        'header' => "Content-type: application/x-www-form-urlencoded\r\n",
        'method' => 'POST',
        'content' => http_build_query($data)
    )
);
$context = stream_context_create($options);
$result = file_get_contents($urlToken, false, $context);
if(!$result){
    header('Location: index.php?error=3');
    die();
}
//echo $result."<br>";
$resultDec = json_decode($result);
$token = new token(new DateTime("now"), $resultDec->valid_for_minutes,
    "Authorization: " . $resultDec->token_type . " $resultDec->access_token\r\n", $resultDec->expiration_time);
//echo $token->isValid();
$optsUser = array(
    'http' => array(
        'method' => "GET",
        'header' => "accept: application/json\r\n" .
            $token->value,
    )
);

$context2 = stream_context_create($optsUser);

// Open the file using the HTTP headers set above
$result = file_get_contents($serverAddress.'users/me/', false, $context2);
if(!$result){
    header('Location: index.php?error=4');
    die();
}
$user = new user(json_decode($result, true), $token);
echo json_encode($user);
$_SESSION["user"]=serialize($user);
header('Location: rooms.php');
die();