<?
    function GetHead($lang,$site, $llist){
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <title>Potsdamer Prozess-LeitTechnik</title>
        <link rel="stylesheet" type="text/css" media="screen" href="/main.css">
        <link rel="stylesheet" type="text/css" media="print" href="/print.css">
    </head>
    <body>
        <div class="MainHead">PPLT - Potsdamer Prozess LeitTechnik</div>
        <? GetLangMenu($lang, $site, $llist)?>
		<? GetMainMenu($lang) ?>
<?
    }

    function GetLangMenu($lang, $site, $llist){
        if ($lang=='de'){
            ?><div class="LangMenu">de | <a href="/index.php?lang=en&site=<?=$site?>">en</a></div><?
        }
        if ($lang=='en'){
            ?><div class="LangMenu"><a href="/index.php?lang=de&site=<?=$site?>">de</a> | en</div><?
        }
    }
    
    function CheckFor($Site, $LList){
        $ret = array();
        foreach($LList as $Lang){
            $filename = 'site/'.$Lang.'/'.$Site.'.php';
            if (file_exists($filename)){
                $ret[] = $Lang;
            }
        }
        return($ret);
    }
    
    function GetSite($Lang, $Site, $LList){
        $filename = 'site/'.$Lang.'/'.$Site.'.php';
        if (!file_exists($filename)){
            ?>
                <div class="TextBody">                    
                    <div class="Head">File Not Found</div>
            <?
            
            $slist = CheckFor($Site, $LList);             
            if (count($slist) == 0){
                ?>
                    <div class="Text">Site <b><?=$Site?></b> it not avaiable for any language.</div>
                    </div>
                <?
                return;
            }
            
            ?>
                <div class="Text">
                    Site <b><?=$Site?></b> is not available for language <b><?=$Lang?></b> but for
                    the language(s):
            <?            
            
            foreach($slist as $lang){
                ?>
                    <a href="/index.php?lang=<?=$lang?>&site=<?=$Site?>"><?=$lang?></a>&nbsp;
                <?
            }
            ?></div><?
        }else
            include($filename);
    }
    
    function GetLangList(){
        $liste = glob('site/*',GLOB_ONLYDIR|GLOB_MARK);
        $ret = array();
        
        foreach($liste as $dir){
            $ret[] = basename($dir);
        }
        return($ret);
    }



	function GetMainMenu($lang){
		$filename = "menu.".$lang.".php";
		if(file_exists($filename)){
			include($filename);
			GetMenu($lang);
		}else{
			include("menu.en.php");
			GetMenu($lang);
		} 	
	}
?>
