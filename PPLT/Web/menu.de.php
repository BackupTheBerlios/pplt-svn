<?
	function GetMenu($lang){
	?>
		<ul class="Menu">
			<li><a href="/<?=$lang?>/index.html">Index</a></li>
			<li><a href="/<?=$lang?>/DocIndex.html">Dokumentation</a>
				<ul>
					<li id="last"><a href="/<?=$lang?>/pyDCPU_Intro.html">pyDCPU Einf&uuml;hrung</a></li>
				</ul></li>
			<li><a href="/de/Download.html">Download</a></li>
			<li><a href="/de/Contact.html">Kontakt</a></li>
            <li id="last"><a href="/bugs/" target="_blank">Fehlerverfolgung</a></li>
		</ul>
	<?
	}
?>
