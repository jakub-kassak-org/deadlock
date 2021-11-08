<?php
include_once("localization/localization.php");
include_once("functions/functions.php");
include_once("functions/service.php");
$menuactive = "cards";
$title = localization_menu_cards();
include("hlavicka.php");
if (isValidStaffUser()) {
    $allUsers = get_all_users();
    ?>
    <section class="mt-2">
        <div class="container-fluid">
            <div class="row">
                <div class="col-12 d-sm-none">
                    <a class="btn btn-secondary" href="addUser.php"><?php echo localization_add_card(); ?></a>
                </div>
                <div class="col-sm-3 col-12"></div>
                <div class="col-sm-6 col-12">
                    <table class="table table-striped table-bordered">
                        <thead class="thead-dark">
                        <tr>
                            <th><?php echo localization_name_surname() ?></th>
                            <th><?php echo localization_card_number() ?></th>
                            <th><?php echo localization_delete(); ?></th>
                        </tr>
                        </thead>
                        <?php foreach ($allUsers as $user) {
                            echo "<tr>";
                            echo "<td><a href='cardHolder.php?id=" . $user->id . "'>" . $user->first_name . " " . $user->last_name . "</a></td>";
                            echo "<td><a href='cardHolder.php?id=" . $user->id . "'>" . $user->card . "</a></td>";
                            echo "<td><a href='deleteUser.php?id=". $user->id ."'> <i class='fa fa-trash'></i></a></td>";
                            echo "</tr>";
                        } ?>
                    </table>
                </div>
                <div class="col-3 d-none d-sm-block">
                    <a class="btn btn-secondary" href="addUser.php"><?php echo localization_add_card(); ?></a>
                </div>
            </div>
        </div>
    </section>
    <?php
} else {
    echo unauthorized();
}
include("paticka.php");
?>

