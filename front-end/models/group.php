<?php


class group
{
    public $name;
    public $created;
    public $updated;
    public $id;
    function __construct(array $data) {
        //echo "<br><br>".json_encode($data);
        foreach($data as $key => $val) {
            //echo $key." ".$val."<br>";
            if(property_exists(__CLASS__,$key)) {
                $this->$key = $val;
            }
        }
    }
}