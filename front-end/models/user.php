<?php


class user
{
    public $id;
    public $first_name;
    public $is_staff;
    public $disabled;
    public $updated;
    public $card;
    public $last_name;
    public $created;
    public $token;
    public $username;

    function __construct(array $data, $token) {
        //echo "<br><br>".json_encode($data);
        $this->token = $token;
        foreach($data as $key => $val) {
            //echo $key." ".$val."<br>";
            if(property_exists(__CLASS__,$key)) {
                $this->$key = $val;
            }
        }
    }
}
?>