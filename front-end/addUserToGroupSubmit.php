<?php
if(!isset($_POST["submit"])||!isset($_POST["uids"])||!isset($_POST["gid"])){
    header('Location: groups.php');
    die();
}
include_once("functions/service.php");
add_users_to_group($_POST["gid"], $_POST["uids"]);
header('Location: groupDetail.php?id='.$_POST["gid"]);

