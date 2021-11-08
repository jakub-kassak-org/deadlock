<?php
if (!isset($_GET["uid"])||!isset($_GET["gid"])) {
    header('Location: cards.php');
    die();
}
include_once("functions/service.php");
$result = remove_user_from_group($_GET["uid"], $_GET["gid"]);
header('Location: cardHolder.php?id='.$_GET["uid"]);
