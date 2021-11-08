<?php
include_once("localization/localization.php");
$title = localization_add_card();
$menuactive="cards";
include("hlavicka.php");
?>
<section>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <form method="post" action="addCardHolderSubmit.php">
                    <div class="container-fluid">
                        <div class="row">
                            <div class="col-sm-5 col-6">
                                <label for="username"><?php echo localization_username() ?></label>
                            </div>
                            <div class="col-sm-7 col-6">
                                <input type="text" name="username" id="username">
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-sm-5 col-6">
                                <label for="fname"><?php echo localization_first_name() ?></label>
                            </div>
                            <div class="col-sm-7 col-6">
                                <input type="text" name="fname" id="fname">
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-sm-5 col-6">
                                <label for="lname"><?php echo localization_last_name() ?></label>
                            </div>
                            <div class="col-sm-7 col-6">
                                <input type="text" name="lname" id="lname">
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-sm-5 col-6">
                                <label for="cnr"><?php echo localization_card_number() ?></label>
                            </div>
                            <div class="col-sm-7 col-6">
                                <input type="text" name="cnr" id="cnr">
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-sm-5 col-6">
                                <label for="admin"><?php echo localization_is_admin() ?></label>
                            </div>
                            <div class="col-sm-7 col-6">
                                <input type="checkbox" name="admin" id="admin">
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-sm-5 col-6">
                                <input type="submit" name="submit" value="<?php echo localization_submit() ?>">
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</section>
<?php include("paticka.php");?>
