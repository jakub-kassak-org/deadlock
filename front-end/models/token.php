<?php


class token
{
    public $value;

    //token is valid for 30 minutes
    public $time_recieved;
    public $valid_for_minutes;
    public $expiration_time;

    public function __construct($timeRecieved, $validForMinutes, $value, $expirationTime){
        $this->time_recieved = $timeRecieved;
        $this->value = $value;
        $this->valid_for_minutes = $validForMinutes;
        $this->expiration_time =new DateTime($expirationTime);
    }

    public function isValid(){
        return new DateTime("now")<$this->expiration_time;
    }
}