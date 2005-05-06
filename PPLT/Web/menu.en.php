<?
	function GetMenu($lang){
	?>
		<ul class="Menu">
			<li><a href="/<?=$lang?>/index.html">Index</a></li>
			<li><a href="/<?=$lang?>/DocIndex.html">Documentation</a>
				<ul>
					<li><a href="/<?=$lang?>/pyDCPU_Intro.html">pyDCPU Intoduction</a></li>
					<li><a href="/<?=$lang?>/pyDCPU.html">pyDCPU Reference</a></li>
					<li id="last"><a href="/<?=$lang?>/SimpleExport.html">Simple Export Tutorial</a></li>
				</ul></li>
			<li><a href="http://developer.berlios.de/project/showfiles.php?group_id=3237">Download</a></li>
			<li><a href="http://developer.berlios.de/sendmessage.php?touser=14093">Contact</a></li>
		</ul>
	<?
	}
?>
