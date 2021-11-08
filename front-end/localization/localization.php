<?php
function localization_username(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Prihlasovacie meno";
    if($_SESSION["lang"]=="en")
        return "Username";
    return "{Unknown language} Username";
}

function localization_password(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Heslo";
    if($_SESSION["lang"]=="en")
        return "Password";
    return "{Unknown language} Password";
}

function localization_submit(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Odošli";
    if($_SESSION["lang"]=="en")
        return "Submit";
    return "{Unknown language} Submit";
}

function localization_error($number){
    switch($number){
        case 0:
            if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
                return "Platnosť vášho prihlásenia vypršala. Prihláste sa znova.";
            if($_SESSION["lang"]=="en")
                return "Validity of your login has ended. Login again, please.";
            return "{Unknown language} Validity of your login has ended. Login again, please.";
            break;
        case 1:
            if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
                return "Na používanie aplikácie sa musíte prihlásiť.";
            if($_SESSION["lang"]=="en")
                return "You have to log in first.";
            return "{Unknown language} You have to log in first.";
            break;
        case 3:
            if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
                return "Neplatné meno alebo heslo.";
            if($_SESSION["lang"]=="en")
                return "Invalid name or password.";
            return "{Unknown language} Invalid name or password.";
            break;
        case 4:
            if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
                return "Nastala chyba pri spracovávaní požiadavky.";
            if($_SESSION["lang"]=="en")
                return "An error occurred while processing your request.";
            return "{Unknown language} An error occurred while processing your request.";
            break;
        default:
            return "";
            break;
    }
    return "";
}

function localization_menu_aps(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Miestnosti";
    if($_SESSION["lang"]=="en")
        return "Rooms";
    return "{Unknown language} Rooms";
}

function localization_menu_cards(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Karty";
    if($_SESSION["lang"]=="en")
        return "Cards";
    return "{Unknown language} Cards";
}

function localization_menu_groups(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Skupiny";
    if($_SESSION["lang"]=="en")
        return "Groups";
    return "{Unknown language} Groups";
}

function localization_logged_in_as(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Prihlásený ako ";
    if($_SESSION["lang"]=="en")
        return "Logged in as ";
    return "{Unknown language} Logged in as ";
}

function localization_log_out(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Odhlásiť";
    if($_SESSION["lang"]=="en")
        return "Log out";
    return "{Unknown language} Log out";
}

function localization_name_surname(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Meno a priezvisko";
    if($_SESSION["lang"]=="en")
        return "Full name";
    return "{Unknown language} Full name";
}

function localization_card_number(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Číslo karty";
    if($_SESSION["lang"]=="en")
        return "Card number";
    return "{Unknown language} Card number";
}

function localization_card_holder(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Karta";
    if($_SESSION["lang"]=="en")
        return "Card";
    return "{Unknown language} Card";
}

function localization_unauthorized_error(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Na zobrazenie stránky nemáte dostatočné oprávnenie.";
    if($_SESSION["lang"]=="en")
        return "Unauthorized to view site.";
    return "{Unknown language} Unauthorized to view site.";
}

function localization_first_name(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Meno";
    if($_SESSION["lang"]=="en")
        return "First name";
    return "{Unknown language} First name";
}

function localization_last_name(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Priezvisko";
    if($_SESSION["lang"]=="en")
        return "Last name";
    return "{Unknown language} Last name";
}

function localization_created(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Vytvorený";
    if($_SESSION["lang"]=="en")
        return "Created";
    return "{Unknown language} Created";
}

function localization_updated(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Upravený";
    if($_SESSION["lang"]=="en")
        return "Updated";
    return "{Unknown language} Updated";
}

function localization_is_admin(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Admin";
    if($_SESSION["lang"]=="en")
        return "Admin";
    return "{Unknown language} Admin";
}

function localization_is_disabled(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Blokovaný";
    if($_SESSION["lang"]=="en")
        return "Disabled";
    return "{Unknown language} Disabled";
}

function localization_edit(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Upraviť";
    if($_SESSION["lang"]=="en")
        return "Edit";
    return "{Unknown language} Edit";
}

function localization_group(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Skupina";
    if($_SESSION["lang"]=="en")
        return "Group";
    return "{Unknown language} Group";
}

function localization_add_card_to_group(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Pridať karty";
    if($_SESSION["lang"]=="en")
        return "Add cards";
    return "{Unknown language} Add carda";
}

function localization_delete(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Zmazať";
    if($_SESSION["lang"]=="en")
        return "Delete";
    return "{Unknown language} Delete";
}

function localization_add_group(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Pridať skupinu";
    if($_SESSION["lang"]=="en")
        return "Add group";
    return "{Unknown language} Add group";
}

function localization_ap_type(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Miestnosť";
    if($_SESSION["lang"]=="en")
        return "Room";
    return "{Unknown language} Room";
}

function localization_ap(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Čítačka";
    if($_SESSION["lang"]=="en")
        return "Reader";
    return "{Unknown language} Reader";
}

function localization_add_room(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Pridať miestnosť";
    if($_SESSION["lang"]=="en")
        return "Add room";
    return "{Unknown language} Add room";
}

function localization_add_card(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Pridať kartu";
    if($_SESSION["lang"]=="en")
        return "Add card";
    return "{Unknown language} Add card";
}

function localization_add_ap(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Pridať čítačku";
    if($_SESSION["lang"]=="en")
        return "Add reader";
    return "{Unknown language} Add reader";
}

function localization_title(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Názov";
    if($_SESSION["lang"]=="en")
        return "Title";
    return "{Unknown language} Title";
}

function localization_add_apto_ap_type(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Pridať čítačku do miestnosti";
    if($_SESSION["lang"]=="en")
        return "Add reader to room";
    return "{Unknown language} Add reader to room";
}

function localization_day_of_week($nr){
    $sk = ["Pondelok", "Utorok", "Streda", "Štvrtok", "Piatok", "Sobota", "Nedeľa"];
    $en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return $sk[$nr];
    if($_SESSION["lang"]=="en")
        return $en[$nr];
}

function localization_edit_timetable(){
    if(!isset($_SESSION["lang"])||$_SESSION["lang"]=="sk")
        return "Upraviť rozvrh";
    if($_SESSION["lang"]=="en")
        return "Edit timetable";
    return "{Unknown language} Edit timetable";
}