<?php
if (!isset($_POST["submit"]) || !isset($_POST["title"])) {
    header('Location: rooms.php');
    die();
}
include_once("functions/service.php");
$result=create_room($_POST["title"]);
if($result)
    header('Location: roomDetail.php?id='.$result["id"]);