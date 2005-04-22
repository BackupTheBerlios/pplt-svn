<?
    include('mylib.php');
    $LANG_LIST = GetLangList();
        
    $SITE = $_REQUEST['site'];
    if (empty($SITE)){
        $SITE = "index";
    }
    
    $LANG = $_REQUEST['lang'];
    if (empty($LANG)){
        $LANG = 'en';
    }
    
    GetHead($LANG, $SITE, $LANG_LIST);
    GetSite($LANG, $SITE, $LANG_LIST);
    
?>
<div style="font-size:10pt; text-align:right; color:#aaaaaa; border-top:3px double #000000; margin-top:50px;">
    Hosted by: 
    <a href="http://developer.berlios.de" title="BerliOS Developer">
        <img src="http://developer.berlios.de/bslogo.php?group_id=3237"
             width="124px"
             height="32px"
             border="0"
             alt="BerliOS Developer">
    </a>
</div>
