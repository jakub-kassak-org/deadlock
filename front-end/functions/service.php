<?php
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}
include_once("models/user.php");
include_once("models/group.php");
include_once("models/token.php");
include_once("constants/constants.php");
function get_all_users()
{
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    $opts = array(
        'http' => array(
            'method' => "GET",
            'header' => "accept: application/json\r\n" .
                $user->token->value,
        )
    );

    $context = stream_context_create($opts);

// Open the file using the HTTP headers set above
    include("constants/constants.php");
    $result = file_get_contents($serverAddress . "users/", false, $context);
    //echo $result;
    $users = json_decode($result, true);
    $retval = array();
    foreach ($users as $user) {
        //echo json_encode($user);
        array_push($retval, new user($user, null));
    }
    return $retval;
}

function get_user_by_id($id)
{
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
        return false;
    }
    $opts = array(
        'http' => array(
            'method' => "GET",
            'header' => "accept: application/json\r\n" .
                $user->token->value,
        )
    );

    $context = stream_context_create($opts);

// Open the file using the HTTP headers set above
    include("constants/constants.php");
    $result = file_get_contents($serverAddress . "users/", false, $context);
    //echo "<br><br><br>".$result;
    $users = json_decode($result, true);
    foreach ($users as $user) {
        //echo "<br><br>".json_encode($user);
        if ($user["id"] == $id) {
            return new user($user, null);
        }
    }
    return false;
}

function editUser($id, $fname, $lname, $card, $admin, $username, $disabled)
{
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
        return false;
    }
    $data = array("card" => $card, "username" => $username, "first_name" => $fname, "last_name" => $lname, "is_staff" => $admin, "disabled" => $disabled);
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n" .
                $user->token->value,
            'method' => 'PUT',
            'content' => json_encode($data)
        )
    );
    echo http_build_query($data);
    $context = stream_context_create($options);
    include("constants/constants.php");
    return file_get_contents($serverAddress . "users/update/" . $id . "/", false, $context);
}

function get_all_groups()
{
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    $opts = array(
        'http' => array(
            'method' => "GET",
            'header' => "accept: application/json\r\n" .
                $user->token->value,
        )
    );

    $context = stream_context_create($opts);

// Open the file using the HTTP headers set above
    include("constants/constants.php");
    $result = file_get_contents($serverAddress . "groups/", false, $context);
    //echo $result;
    $groups = json_decode($result, true);
    $retval = array();
    foreach ($groups["groups"] as $group) {
        //echo json_encode($user);
        array_push($retval, new group($group));
    }
    return $retval;
}

function get_group_users_by_id($id)
{
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    $opts = array(
        'http' => array(
            'method' => "GET",
            'header' => "accept: application/json\r\n" .
                $user->token->value,
        )
    );

    $context = stream_context_create($opts);

// Open the file using the HTTP headers set above
    include("constants/constants.php");
    $result = file_get_contents($serverAddress . "groups/" . $id . "/", false, $context);
    if($result == null){
        return array();
    }
    //echo $result;
    $groups = json_decode($result, true);
    if(!is_array($groups["users"])){
        return array();
    }
    $retval = array();
    foreach ($groups["users"] as $user) {
        //echo json_encode($user);
        array_push($retval, new user($user, null));
    }
    return $retval;
}

function get_group_by_id($id)
{
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    $opts = array(
        'http' => array(
            'method' => "GET",
            'header' => "accept: application/json\r\n" .
                $user->token->value,
        )
    );

    $context = stream_context_create($opts);

// Open the file using the HTTP headers set above
    include("constants/constants.php");
    $result = file_get_contents($serverAddress . "groups/", false, $context);
    //echo $result;
    $groups = json_decode($result, true);
    foreach ($groups["groups"] as $group) {
        if ($group["id"] == $id) {
            return new group($group);
        }
    }
    return false;
}

function add_users_to_group($groupid, array $uids)
{
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    //usergroup/add/?user_id=3&group_id=1
    foreach ($uids as $uid) {
        $options = array(
            'http' => array(
                'header' => "Content-type: application/x-www-form-urlencoded\r\n" .
                    $user->token->value,
                'method' => 'POST',
                //'content' => "?user_id=$uid&group_id=$groupid"
            )
        );
        include("constants/constants.php");
        $context = stream_context_create($options);
        $result = file_get_contents($serverAddress . "usergroup/add/?user_id=$uid&group_id=$groupid", false, $context);
        if(!$result)
            return false;
    }
}

function get_all_groups_of_user($uid){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    $opts = array(
        'http' => array(
            'method' => "GET",
            'header' => "accept: application/json\r\n" .
                $user->token->value,
        )
    );

    $context = stream_context_create($opts);

// Open the file using the HTTP headers set above
    include("constants/constants.php");
    $result = file_get_contents($serverAddress . "users/".$uid."/get_groups/", false, $context);
    if(!$result)
        return false;
    //echo $result;
    $groups = json_decode($result, true);
    $retval = array();
    foreach ($groups as $group) {
        array_push($retval, new group($group));
    }
    return $retval;
}

function get_all_ap_types(){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    $opts = array(
        'http' => array(
            'method' => "GET",
            'header' => "accept: application/json\r\n" .
                $user->token->value,
        )
    );

    $context = stream_context_create($opts);

// Open the file using the HTTP headers set above
    include("constants/constants.php");
    $result = file_get_contents($serverAddress . "aptype/", false, $context);
    return json_decode($result, true);
}

function get_ap_type_by_id($id){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    $opts = array(
        'http' => array(
            'method' => "GET",
            'header' => "accept: application/json\r\n" .
                $user->token->value,
        )
    );

    $context = stream_context_create($opts);

// Open the file using the HTTP headers set above
    include("constants/constants.php");
    $result = file_get_contents($serverAddress . "aptype/", false, $context);
    $ap_types = json_decode($result, true);
    if(!$ap_types)
        return false;
    foreach ($ap_types as $ap_type) {
        if($ap_type["id"]==$id)
            return $ap_type;
    }
    return false;
}

function get_all_ap_by_ap_type($aptypeid){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    $opts = array(
        'http' => array(
            'method' => "GET",
            'header' => "accept: application/json\r\n" .
                $user->token->value,
        )
    );

    $context = stream_context_create($opts);

// Open the file using the HTTP headers set above
    include("constants/constants.php");
    $result = file_get_contents($serverAddress . "aptype/$aptypeid/get_aps/", false, $context);
    return json_decode($result, true);
}

function create_user($username, $first_name, $last_name, $card, $admin){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    $data = array('username' => $username, 'first_name' => $first_name, 'last_name' => $last_name,
        'card'=>$card, 'is_staff'=>$admin);
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n".
        $user->token->value,
            'method' => 'POST',
            'content' => json_encode($data)
        )
    );
    $context = stream_context_create($options);
    include("constants/constants.php");
    $result = file_get_contents($serverAddress."users/", false, $context);
    if(!$result){
        return false;
    }
    return new user(json_decode($result, true), false);
}

function create_room($title){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    $data = array('name' => $title);
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n".
                $user->token->value,
            'method' => 'POST',
            'content' => json_encode($data)
        )
    );
    $context = stream_context_create($options);
    include("constants/constants.php");
    $result = file_get_contents($serverAddress."aptype/add/", false, $context);
    return json_decode($result, true);
}

function create_ap_of_type($aptype_id, $title){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    $data = array('name' => $title);
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n".
                $user->token->value,
            'method' => 'POST',
            'content' => json_encode($data)
        )
    );
    $context = stream_context_create($options);
    include("constants/constants.php");
    $result = file_get_contents($serverAddress."ap/add/", false, $context);
    echo $result;
    if(!$result)
        return false;
    $ap = json_decode($result, true);
    $data2 = array($ap["id"]);
    $options2 = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n" .
                $user->token->value,
            'method' => 'PUT',
            'content' => json_encode($data2)
        )
    );
    $context2 = stream_context_create($options2);
    file_get_contents($serverAddress."aptype/$aptype_id/add_aps/", false, $context2);
    return $ap;
}

function create_group($title){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
    }
    $data = array('name' => $title);
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n".
                $user->token->value,
            'method' => 'POST',
            'content' => json_encode($data)
        )
    );
    $context = stream_context_create($options);
    include("constants/constants.php");
    $result = file_get_contents($serverAddress."groups/", false, $context);
    return json_decode($result, true);
}

function delete_user_with_id($id){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if($user->id == $id)
        return false;
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
        return false;
    }
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n".
                $user->token->value,
            'method' => 'DELETE'
        )
    );
    $context = stream_context_create($options);
    include("constants/constants.php");
    $result = file_get_contents($serverAddress."users/delete/$id/", false, $context);
    return $result;
}

function delete_group_with_id($id){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
        return false;
    }
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n".
                $user->token->value,
            'method' => 'DELETE'
        )
    );
    $context = stream_context_create($options);
    include("constants/constants.php");
    $result = file_get_contents($serverAddress."groups/delete/$id/", false, $context);
    return $result;
}

function remove_user_from_group($uid, $gid){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
        return false;
    }
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n".
                $user->token->value,
            'method' => 'DELETE'
        )
    );
    $context = stream_context_create($options);
    include("constants/constants.php");
    $result = file_get_contents($serverAddress."usergroup/delete/$uid/$gid/", false, $context);
    return $result;
}

function delete_ap_type_with_id($id){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
        return false;
    }
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n".
                $user->token->value,
            'method' => 'DELETE'
        )
    );
    $context = stream_context_create($options);
    include("constants/constants.php");
    $result = file_get_contents($serverAddress."aptype/delete/$id/", false, $context);
    return $result;
}

function delete_ap_with_id($id){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
        return false;
    }
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n".
                $user->token->value,
            'method' => 'DELETE'
        )
    );
    $context = stream_context_create($options);
    include("constants/constants.php");
    $result = file_get_contents($serverAddress."ap/delete/$id/", false, $context);
    return $result;
}

function get_timespec_id($tfrom, $tto, $weekday){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
        return false;
    }
    $opts = array(
        'http' => array(
            'method' => "GET",
            'header' => "accept: application/json\r\n" .
                $user->token->value,
        )
    );
    $context = stream_context_create($opts);
    $data = array('weekday'=>$weekday, 'time_from'=>$tfrom, 'time_to'=>$tto);
    include("constants/constants.php");
    $result = file_get_contents($serverAddress."timespec/get_ids/?".http_build_query($data), false, $context);
    return json_encode($result, true);
}

function get_rule_by_timespec_ap_type($ap_type_id, $timespec_id){
    if (!isset($_SESSION["user"])) {
        header('Location: index.php?error=1');
        return false;
    }
    $user = unserialize($_SESSION["user"]);
    if (!$user->token->isValid()) {
        header('Location: index.php?error=0');
        return false;
    }
    $opts = array(
        'http' => array(
            'method' => "GET",
            'header' => "accept: application/json\r\n" .
                $user->token->value,
        )
    );
    $context = stream_context_create($opts);
    $data = array('ap_type_id'=>$ap_type_id, 'time_spec_id'=>$timespec_id);
    include("constants/constants.php");
    $result = file_get_contents($serverAddress."groups/by_ap_type_and_time_spec/?".http_build_query($data), false, $context);
    return json_encode($result, true);
}
