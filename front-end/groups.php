<?php
include_once("localization/localization.php");
include_once("functions/functions.php");
include_once("functions/service.php");
$menuactive = "groups";
$title = localization_menu_groups();
include("hlavicka.php");
if (isValidStaffUser()) {
    $allGroups = get_all_groups();
    if ($allGroups) {
        ?>
        <section class="mt-2">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-12 d-sm-none">
                        <a class="btn btn-secondary" href="addGroup.php"><?php echo localization_add_group(); ?></a>
                    </div>
                    <div class="col-sm-3 col-12"></div>
                    <div class="col-sm-6 col-12">
                        <table class="table table-striped table-bordered">
                            <thead class="thead-dark">
                            <tr>
                                <th><?php echo localization_group() ?></th>
                                <th><?php echo localization_updated() ?></th>
                                <th><?php echo localization_delete() ?></th>
                            </tr>
                            </thead>
                            <?php foreach ($allGroups as $group) {
                                echo "<tr>";
                                echo "<td><a href='groupDetail.php?id=" . $group->id . "'>" . $group->name . "</a></td>";
                                echo "<td>" . $group->updated . "</td>";
                                echo "<td><a href='deleteGroup.php?id=". $group->id ."'> <i class='fa fa-trash'></i></a></td>";
                                echo "</tr>";
                            } ?>
                        </table>
                    </div>
                    <div class="col-3 d-none d-sm-block">
                        <a class="btn btn-secondary" href="addGroup.php"><?php echo localization_add_group(); ?></a>
                    </div>
                </div>
            </div>
        </section>
        <?php
    }
} else {
    echo unauthorized();
}
include("paticka.php");
?>

