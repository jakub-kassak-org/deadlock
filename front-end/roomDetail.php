<?php
include_once("localization/localization.php");
if(!isset($_GET["id"])){
    header('Location: rooms.php');
    die();
}
include_once("functions/service.php");
include_once("functions/functions.php");
$thisApType = get_ap_type_by_id($_GET["id"]);
if(!$thisApType){
    header('Location: rooms.php');
    die();
}
$allAps = get_all_ap_by_ap_type($_GET["id"]);
$menuactive="rooms";
$title = localization_ap_type();
include("hlavicka.php");
?>
<section>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <h2><?php echo $thisApType["name"] ?></h2>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-4 col-12">
                <?php
                echo '<table class="table table-bordered table-striped">';
                echo "<thead class='thead-dark'>";
                echo '<tr><th>'.localization_ap()."</th></tr>";
                echo '</thead>';
                foreach ($allAps as $ap){
                    echo '<tr><td>'.$ap['name'].'</td></tr>';
                }
                echo "</table>";
                ?>
                <a class="btn btn-dark mt-2" href="addApWithType.php?id=<?php echo $_GET["id"]; ?>"><?php echo localization_add_ap(); ?></a>
            </div>
            <div class="col-lg-8 col-12">
                <table class="table table-striped table-bordered table-sm">
                    <thead class="thead-dark">
                    <tr>
                        <th></th>
                        <th><?php echo localization_day_of_week(0) ?></th>
                        <th><?php echo localization_day_of_week(1) ?></th>
                        <th><?php echo localization_day_of_week(2) ?></th>
                        <th><?php echo localization_day_of_week(3) ?></th>
                        <th><?php echo localization_day_of_week(4) ?></th>
                    </tr>
                    </thead>
                    <tr>
                        <td>8:10</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "8:10", "8:55", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "8:10", "8:55", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "8:10", "8:55", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "8:10", "8:55", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "8:10", "8:55", 4) ?></td>
                    </tr>
                    <tr>
                        <td>9:00</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "9:00", "9:45", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "9:00", "9:45", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "9:00", "9:45", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "9:00", "9:45", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "9:00", "9:45", 4) ?></td>
                    </tr>
                    <tr>
                        <td>9:50</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "9:50", "10:35", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "9:50", "10:35", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "9:50", "10:35", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "9:50", "10:35", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "9:50", "10:35", 4) ?></td>
                    </tr>
                    <tr>
                        <td>10:40</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "10:40", "11:25", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "10:40", "11:25", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "10:40", "11:25", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "10:40", "11:25", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "10:40", "11:25", 4) ?></td>
                    </tr>
                    <tr>
                        <td>11:30</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "11:30", "12:15", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "11:30", "12:15", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "11:30", "12:15", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "11:30", "12:15", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "11:30", "12:15", 4) ?></td>
                    </tr>
                    <tr>
                        <td>12:20</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "12:20", "13:05", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "12:20", "12:05", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "12:20", "12:05", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "12:20", "12:05", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "12:20", "12:05", 4) ?></td>
                    </tr>
                    <tr>
                        <td>13:10</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "13:10", "13:55", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "13:10", "13:55", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "13:10", "13:55", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "13:10", "13:55", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "13:10", "13:55", 4) ?></td>
                    </tr>
                    <tr>
                        <td>14:00</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "14:00", "14:45", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "14:00", "14:45", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "14:00", "14:45", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "14:00", "14:45", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "14:00", "14:45", 4) ?></td>
                    </tr>
                    <tr>
                        <td>14:50</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "14:50", "15:35", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "14:50", "15:35", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "14:50", "15:35", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "14:50", "15:35", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "14:50", "15:35", 4) ?></td>
                    </tr>
                    <tr>
                        <td>15:40</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "15:40", "16:25", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "15:40", "16:25", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "15:40", "16:25", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "15:40", "16:25", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "15:40", "16:25", 4) ?></td>
                    </tr>
                    <tr>
                        <td>16:30</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "16:30", "17:15", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "16:30", "17:15", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "16:30", "17:15", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "16:30", "17:15", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "16:30", "17:15", 4) ?></td>
                    </tr>
                    <tr>
                        <td>17:20</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "17:20", "18:05", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "17:20", "18:05", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "17:20", "18:05", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "17:20", "18:05", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "17:20", "18:05", 4) ?></td>
                    </tr>
                    <tr>
                        <td>18:10</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "18:10", "18:55", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "18:10", "18:55", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "18:10", "18:55", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "18:10", "18:55", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "18:10", "18:55", 4) ?></td>
                    </tr>
                    <tr>
                        <td>19:00</td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "19:00", "19:45", 0) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "19:00", "19:45", 1) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "19:00", "19:45", 2) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "19:00", "19:45", 3) ?></td>
                        <td><?php echo get_timetable_room_time($thisApType["id"], "19:00", "19:45", 4) ?></td>
                    </tr>
                </table>
                <a class="btn btn-dark" href="editTimetale.php?room_id=<?php echo $thisApType["id"]; ?>"><?php echo localization_edit_timetable(); ?></a>
            </div>
        </div>
    </div>
</section>
<?php include("paticka.php"); ?>