<?php
if (!isset($_GET["id"])) {
    header('Location: groups.php');
    die();
}
include_once("functions/service.php");
$result=delete_group_with_id($_GET["id"]);
header('Location: groups.php');