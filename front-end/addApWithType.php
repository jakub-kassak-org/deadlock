<?php
include_once("localization/localization.php");
if(!isset($_GET["id"])){
    header('Location: rooms.php');
    die();
}
include_once("functions/service.php");
$thisApType = get_ap_type_by_id($_GET["id"]);
if(!$thisApType){
    header('Location: rooms.php');
    die();
}
$menuactive="rooms";
$title = localization_add_ap();
include("hlavicka.php");
?>
<section>
    <div class="container-fluid">
        <div class="row">
            <div class="col-3 d-none d-sm-block"></div>
            <div class="col-6">
                <h2><?php echo localization_add_apto_ap_type()." ".$thisApType["name"]; ?></h2>
                <form method="post" action="addApWithTypeSubmit.php">
                    <input type="hidden" name="id" value="<?php echo $thisApType["id"]; ?>">
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

