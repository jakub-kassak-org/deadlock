<?php
include_once("localization/localization.php");
include_once("functions/functions.php");
include_once("functions/service.php");
$menuactive = "cards";
$title = localization_card_holder();
if (!isset($_GET["id"])) {
    header('Location: cards.php');
    die();
}
$currentuser = get_user_by_id($_GET["id"]);
if (!$currentuser) {
    header('Location: cards.php');
    die();
}
include("hlavicka.php");
if (isValidStaffUser()) {
    ?>
    <section>
        <div class="container-fluid">
            <div class="row">
                <div class="col-lg-5 col-12">
                    <form method="post" action="editCardHolder.php">
                        <div class="container-fluid">
                            <input type="hidden" name="id" value="<?php echo $currentuser->id ?>">
                            <div class="row">
                                <div class="col-sm-5 col-6">
                                    <label for="username"><?php echo localization_username() ?></label>
                                </div>
                                <div class="col-sm-7 col-6">
                                    <input class="enableOnClick" type="text" name="username" id="username"
                                           value="<?php echo $currentuser->username ?>" readonly>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-5 col-6">
                                    <label for="fname"><?php echo localization_first_name() ?></label>
                                </div>
                                <div class="col-sm-7 col-6">
                                    <input class="enableOnClick" type="text" name="fname" id="fname"
                                           value="<?php echo $currentuser->first_name ?>" readonly>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-5 col-6">
                                    <label for="lname"><?php echo localization_last_name() ?></label>
                                </div>
                                <div class="col-sm-7 col-6">
                                    <input class="enableOnClick" type="text" name="lname" id="lname"
                                           value="<?php echo $currentuser->last_name ?>" readonly>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-5 col-6">
                                    <label for="cnr"><?php echo localization_card_number() ?></label>
                                </div>
                                <div class="col-sm-7 col-6">
                                    <input type="text" class="enableOnClick" name="cnr" id="cnr"
                                           value="<?php echo $currentuser->card ?>" readonly>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-5 col-6">
                                    <label><?php echo localization_created() ?></label>
                                </div>
                                <div class="col-sm-7 col-6">
                                    <p><?php echo $currentuser->created ?></p>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-5 col-6">
                                    <label><?php echo localization_updated() ?></label>
                                </div>
                                <div class="col-sm-7 col-6">
                                    <p><?php echo $currentuser->updated ?></p>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-5 col-6">
                                    <label for="admin"><?php echo localization_is_admin() ?></label>
                                </div>
                                <div class="col-sm-7 col-6">
                                    <input type="checkbox" name="admin"
                                           id="admin" <?php if ($currentuser->is_staff) echo 'checked' ?> readonly>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-5 col-6">
                                    <label for="disabled"><?php echo localization_is_disabled() ?></label>
                                </div>
                                <div class="col-sm-7 col-6">
                                    <input class="enableOnClick" type="checkbox" name="disabled"
                                           id="disabled" <?php if ($currentuser->disabled) echo 'checked' ?> readonly>
                                </div>
                            </div>
                            <div class="row" id="btns">
                                <div class="col-sm-5 col-6">
                                    <button type="button" id="enablebtn"><?php echo localization_edit() ?></button>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="col-lg-3 col-12">
                    <table class="table table-striped table-bordered">
                        <thead class="thead-dark">
                        <tr>
                            <th><?php echo localization_group(); ?></th>
                            <th><?php echo localization_delete(); ?></th>
                            <th><?php echo localization_delete(); ?></th>
                        </tr>
                        </thead>
                        <?php
                        $userGroups = get_all_groups_of_user($currentuser->id);
                        foreach ($userGroups as $group) {
                            echo "<tr>";
                            echo "<td><a href='groupDetail.php?id=" . $group->id . "'>" . $group->name . "</a></td>";
                            echo "<td>" . $group->updated . "</td>";
                            echo "<td><a href='removeUserFromGroup.php?uid=". $currentuser->id ."&gid=".$group->id."'> <i class='fa fa-trash'></i></a></td>";
                            echo "</tr>";
                        } ?>
                    </table>
                </div>
                <div class="col-lg-3 col-12">
                    <a href="addGroupToUser.php?id=<?php echo $currentuser->id ?>" class="btn btn-dark">
                        <?php echo localization_add_group(); ?>
                    </a>
                </div>
            </div>
        </div>
    </section>
    <script>
        $(function () {
            $('#enablebtn').click(function () {
                console.log("asd");
                $("input.enableOnClick").removeAttr("readonly");
                document.getElementById("btns").innerHTML += '<div class="col-sm-4 col-6"><input type="submit" name="submit" value="<?php echo localization_submit(); ?>"></div>';
            });
        });

    </script>
    <?php
} else {
    echo unauthorized();
}
include("paticka.php");
?>

