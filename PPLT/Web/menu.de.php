<?
	function GetMenu($lang){
	?>
		<ul class="Menu">
			<li><a href="/<?=$lang?>/index.html">Index</a></li>
			<li><a href="/<?=$lang?>/DocIndex.html">Dokumentation</a>
				<ul>
					<li id="last"><a href="/<?=$lang?>/pyDCPU_Intro.html">pyDCPU Einf&uuml;hrung</a></li>
				</ul></li>
			<li><a href="http://developer.berlios.de/project/showfiles.php?group_id=3237">Download</a></li>
			<li id="last"><a href="http://developer.berlios.de/sendmessage.php?touser=14093">Kontakt</a></li>
		</ul>
	<?
	}
?>
