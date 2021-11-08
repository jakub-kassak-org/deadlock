<?php
if (!isset($_POST["submit"]) || !isset($_POST["title"]) || !isset($_POST["id"])) {
    header('Location: rooms.php');
    die();
}
include_once("functions/service.php");
$result=create_ap_of_type($_POST["id"], $_POST["title"]);
if($result)
    header('Location: roomDetail.php?id='.$_POST["id"]);