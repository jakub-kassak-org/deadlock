<?php
include_once("models/user.php");
include_once("models/token.php");
include_once("localization/localization.php");
include_once("service.php");
function isValidLogin()
{
    if (!isset($_SESSION["user"]))
        return false;
    $user = unserialize($_SESSION["user"]);
    $token = $user->token;
    return $token->isValid();
}

function isValidStaffUser()
{
    if (!isset($_SESSION["user"]))
        return false;
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid())
        return false;
    return $user->is_staff == "true";
}

function unauthorized()
{
    $retval = "<p class='alert alert-danger'>";
    $retval .= localization_unauthorized_error();
    $retval .= "</p>";
}

function get_timetable_room_time($ap_type_id, $tfrom, $tto, $weekday)
{
    $tss = get_timespec_id($tfrom, $tto, $weekday);
    if (!(is_array($tss) && count($tss) > 0)) {
        return "";
    }
    $retval = "";
    foreach ($tss as $ts) {
        $groups = get_rule_by_timespec_ap_type($ap_type_id, $ts["id"]);
        if (!(is_array($groups) && count($groups) > 0)) {
            continue;
        }
        foreach ($groups as $group) {
            $retval .= "<a href='groupDetail?id=" .$group["id"]."'>".$group['name']."</a>";
        }
    }
    return $retval;
}