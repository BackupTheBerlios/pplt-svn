<?
	function GetMenu($lang){
	?>
		<ul class="Menu">
			<li><a href="/index.php?lang=<?=$lang?>&site=index">Index</a></li>
			<li><a href="/index.php?lang=<?=$lang?>&site=DocIndex">Dokumentation</a>
				<ul>
					<li id="last"><a href="/index.php?lang=<?=$lang?>&site=pyDCPU_Intro">pyDCPU Einf&uuml;hrung</a></li>
				</ul></li>
			<li><a href="http://developer.berlios.de/project/showfiles.php?group_id=3237">Download</a></li>
			<li id="last"><a href="http://developer.berlios.de/sendmessage.php?touser=14093">Kontakt</a></li>
		</ul>
	<?
	}
?>
