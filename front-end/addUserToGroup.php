<?php
$menuactive = "groups";
include_once("localization/localization.php");
$title = localization_add_card_to_group();
include("hlavicka.php");
include("functions/service.php");
if (!isset($_GET["id"])) {
    header('Location: groups.php');
    die();
}
$group = get_group_by_id($_GET["id"]);
if (!$group) {
    header('Location: groups.php');
    die();
}
$allusers = get_all_users();
?>
<section>
    <form method="post" action="addUserToGroupSubmit.php">
        <div class="container-fluid">
            <div class="row">
                <input type="hidden" name="gid" value="<?php echo $group->id; ?>">
                <div class="col-7">
                    <div class="demo ml-5 mt-2">
                        <select style="display:none" name="uids[]" multiple>
                            <?php
                            foreach ($allusers as $user) {
                                echo "<option value='$user->id'>$user->first_name $user->last_name $user->card</option>";
                            }
                            ?>
                        </select>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-7">
                    <input type="submit" name="submit" class="ml-5 mt-1 btn btn-dark" value="<?php echo localization_submit() ?>">
                </div>
            </div>
        </div>
    </form>
</section>
<script>
    $('.demo').dropdown({
        multipleMode: 'label'
    });
</script>
<?php include("paticka.php"); ?>
