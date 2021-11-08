<?php
include("user.php");
$url = 'http://localhost:8000/token/';
$data = array('username' => 'stlpik', 'password' => 'secret');

$options = array(
    'http' => array(
        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
        'method'  => 'POST',
        'content' => http_build_query($data)
    )
);
$context  = stream_context_create($options);
$result = file_get_contents($url, false, $context);
$resultDec = json_decode($result);
//echo $result."<br>";
//echo $resultDec->access_token."<br>";
//echo $resultDec->token_type."<br>";
$opts = array(
    'http'=>array(
        'method'=>"GET",
        'header'=>"accept: application/json\r\n" .
            "Authorization: ".$resultDec->token_type." $resultDec->access_token\r\n" ,
    )
);

$context2 = stream_context_create($opts);

// Open the file using the HTTP headers set above
$file = file_get_contents('http://localhost:8000/users/me/', false, $context2);
$user = new user(json_decode($file, true));
echo json_encode($user);