<?
	function GetMenu($lang){
	?>
		<ul class="Menu">
			<li><a href="/index.php?lang=<?=$lang?>&site=index">Index</a></li>
			<li><a href="/index.php?lang=<?=$lang?>&site=DocIndex">Documentation</a>
				<ul>
					<li><a href="/index.php?lang=<?=$lang?>&site=pyDCPU_Intro">pyDCPU Intoduction</a></li>
					<li><a href="/index.php?lang=<?=$lang?>&site=pyDCPU">pyDCPU Reference</a></li>
					<li id="last"><a href="/index.php?lang=<?=$lang?>&site=SimpleExport">Simple Export Tutorial</a></li>
				</ul></li>
			<li><a href="http://developer.berlios.de/project/showfiles.php?group_id=3237">Download</a></li>
			<li><a href="http://developer.berlios.de/sendmessage.php?touser=14093">Contact</a></li>
		</ul>
	<?
	}
?>
