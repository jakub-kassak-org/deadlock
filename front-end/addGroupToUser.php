<?php
if (!isset($_GET["id"])) {
    header('Location: cards.php');
    die();
}
include_once("localization/localization.php");
include_once("functions/service.php");
include_once("models/user.php");
include_once("models/token.php");
$currentuser = get_user_by_id($_GET["id"]);
$menuactive = "groups";
$title = localization_add_group();
if (!$currentuser) {
    header('Location: cards.php');
    die();
}
include("hlavicka.php");
?>
<section>
    <div class="container-fluid">
        <div class="row">
            <div class="col">
                <form method="post" action="addGroupToUserSubmit.php">
                    <input type="hidden" name="uid" value="<?php echo $currentuser->id;?>">
                    <select name="gid">
                        <?php
                            $allGroups=get_all_groups();
                            foreach ($allGroups as $group) {
                                echo "<option value=$group->id>$group->name</option>";
                            }
                        ?>
                    </select>
                    <input type="submit" name="submit">
                </form>
            </div>
        </div>
    </div>
</section>
