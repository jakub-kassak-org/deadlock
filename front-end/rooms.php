<?php
include_once("localization/localization.php");
include_once("functions/functions.php");
include_once("functions/service.php");
$menuactive="rooms";
$title=localization_menu_aps();
include("hlavicka.php");
if(isValidStaffUser()){
    $allApTypes = get_all_ap_types();
    ?>
    <section class="mt-2">
        <div class="container-fluid">
            <div class="row">
                <div class="col-12 d-sm-none">
                    <a class="btn btn-secondary" href="addRoom.php"><?php echo localization_add_room(); ?></a>
                </div>
                <div class="col-sm-3 col-12"></div>
                <div class="col-sm-6 col-12">
                        <?php
                        foreach($allApTypes as $apType){
                            echo "<h2><a href='roomDetail.php?id=".$apType["id"]."'>".localization_ap_type()." ".$apType['name']."</a><a href='deleteRoom.php?id=".$apType["id"]."'><i class='ml-2 fa fa-trash'></i></a></h2>";
                            $allAps = get_all_ap_by_ap_type($apType["id"]);
                            echo '<table class="table table-striped table-bordered">';
                            echo "<thead class='thead-dark'>";
                            echo '<tr><th>'.localization_ap()."</th>";
                            echo '<th>'.localization_delete()."</th></tr>";
                            echo "</thead>";
                            foreach ($allAps as $ap){
                                echo '<tr><td>'.$ap['name'].'</td>';
                                echo "<td><a href='deleteAp.php?id=". $ap['id'] ."'> <i class='fa fa-trash'></i></a></td></tr>";
                            }
                            echo "</table>";
                        }
                        ?>
                </div>
                <div class="col-3 d-none d-sm-block">
                    <a class="btn btn-secondary" href="addRoom.php"><?php echo localization_add_room(); ?></a>
                </div>
            </div>
        </div>
    </section>
<?php
}
else{
    echo unauthorized();
}
include("paticka.php");
?>

