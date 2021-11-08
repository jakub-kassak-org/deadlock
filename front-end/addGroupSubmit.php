<?php
if (!isset($_POST["submit"]) || !isset($_POST["title"])) {
    header('Location: groups.php');
    die();
}
include_once("functions/service.php");
$result=create_group($_POST["title"]);
if($result)
    header('Location: groupDetail.php?id='.$result["id"]);