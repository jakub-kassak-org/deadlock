<?php if (session_status() == PHP_SESSION_NONE) {
    session_start();
    include("localization/localization.php");
}
if (!isset($_SESSION["lang"])||isset($_POST["slovak"]))
    $_SESSION["lang"] = "sk";
if(isset($_POST["english"])){
    $_SESSION["lang"]= "en";
}
?>
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Prihlásenie</title>
        <link href="styly.css" rel="stylesheet">
        <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
        <link rel="icon" href="logo.png">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    </head>
<body class="pb-5">
<header class="mb-1 mt-0">
    <div class="container-fluid">
        <div class="row">
            <div class="col-7">
                <h1 style="display: inline-block;">Deadlock</h1>
            </div>
            <div class="col-4">
                <form method="post">
                    <input type="submit" <?php if($_SESSION["lang"]=="en")echo "disabled style='color: #FFFFFF'"?> class="btn btn-link" value="EN" name="english">
                    <input type="submit" <?php if($_SESSION["lang"]=="sk")echo "disabled style='color: #FFFFFF'"?> class="btn btn-link" value="SK" name="slovak">
                </form>
            </div>
        </div>
    </div>
</header>
<div class="container-fluid">
    <?php if(isset($_GET["error"])){ ?>
        <div class="row">
            <div class="col-4"></div>
            <div class="col-12 col-sm-4">
                <p class="alert alert-danger mx-2 mb-n4" role="alert">
                    <?php echo localization_error($_GET["error"]) ?>
                </p>
            </div>
        </div>
    <?php } ?>
    <div class="row">
        <div class="col-4 d-none d-sm-block"></div>
        <div class="col-12 col-sm-4">
            <div class="mx-2 mt-5 p-2" style="background-color: #DDDDDD; border-radius: 20px; min-width: 350px">
                <form method="post" action="loginSubmit.php">
                    <div class="container-fluid">
                        <div class="row">
                            <div class="col-4">
                                <label for="meno"><strong><?php echo localization_username() ?></strong></label>
                            </div>
                            <div class="col-8">
                                <input type="text" name="username" id="meno">
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-4">
                                <label for="heslo"><strong><?php echo localization_password() ?></strong></label>
                            </div>
                            <div class="col-8">
                                <input type="password" name="password" id="heslo">
                            </div>
                        </div>
                        <div class="row mt-1">
                            <div class="col-4"></div>
                            <div class="col-4">
                                <input class="btn btn-dark" type="submit" name="submit"
                                       value="<?php echo localization_submit() ?>">
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
<?php include("paticka.php");