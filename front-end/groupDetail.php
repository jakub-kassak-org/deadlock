<?php
include_once("localization/localization.php");
include_once("functions/functions.php");
include_once("functions/service.php");
$menuactive = "groups";
$title = localization_card_holder();
if (!isset($_GET["id"])) {
    header('Location: groups.php');
    die();
}
$currentgroup = get_group_by_id($_GET["id"]);
$currentgroupusers = get_group_users_by_id($_GET["id"]);
if (!$currentgroup) {
    header('Location: groups.php');
    die();
}
include("hlavicka.php");
if (isValidStaffUser()) {
    ?>
    <section class="mt-2">
        <div class="container-fluid">
            <div class="row">
                <div class="col-12 d-sm-none">
                    <a class="btn btn-secondary"
                       href="addUserToGroup.php?id=<?php echo $currentgroup->id; ?>"><?php echo localization_add_card_to_group(); ?></a>
                </div>
                <div class="col-sm-3 col-12"></div>
                <div class="col-sm-6 col-12">
                    <h2><?php echo localization_group() . " " . $currentgroup->name; ?></h2>
                    <table class="table table-bordered table-striped">
                        <thead class="thead-dark">
                        <tr>
                            <th><?php echo localization_username(); ?></th>
                            <th><?php echo localization_card_number(); ?></th>
                            <th><?php echo localization_delete(); ?></th>
                        </tr>
                        </thead>
                        <?php foreach ($currentgroupusers as $user) {
                            echo "<tr>";
                            echo "<td><a href='cardHolder.php?id=" . $user->id . "'>" . $user->first_name . " " . $user->last_name . "</a></td>";
                            echo "<td><a href='cardHolder.php?id=" . $user->id . "'>" . $user->card . "</a></td>";
                            echo "<td><a href='removeUserFromGroup.php?uid=". $user->id ."&gid=".$currentgroup->id."'> <i class='fa fa-trash'></i></a></td>";
                            echo "</tr>";
                        } ?>
                    </table>
                </div>
                <div class="col-3 d-none d-sm-block">
                    <a class="btn btn-secondary"
                       href="addUserToGroup.php?id=<?php echo $currentgroup->id; ?>"><?php echo localization_add_card_to_group(); ?></a>
                </div>
            </div>
        </div>
    </section>
    <?php
}
include("paticka.php");
