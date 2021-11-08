<?php
include_once("localization/localization.php");
$title = localization_add_room();
$menuactive="rooms";
include("hlavicka.php");
?>
<section>
    <div class="container-fluid">
        <div class="row">
            <div class="col-3 d-none d-sm-block"></div>
            <div class="col-6">
                <form method="post" action="addRoomSubmit.php">
                    <div class="container-fluid">
                        <div class="row">
                            <div class="col-sm-5 col-6">
                                <label for="title"><?php echo localization_title() ?></label>
                            </div>
                            <div class="col-sm-7 col-6">
                                <input type="text" name="title" id="title">
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
