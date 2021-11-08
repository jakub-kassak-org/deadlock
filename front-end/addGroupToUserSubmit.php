<?php
if (!isset($_POST["submit"]) || !isset($_POST["uid"]) || !isset($_POST["gid"])) {
    header('Location: groups.php');
    die();
}
include_once("functions/service.php");
add_users_to_group($_POST["gid"], array($_POST["uid"]));
header('Location: cardHolder.php?id=' . $_POST["uid"]);


