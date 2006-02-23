<?
	function GetMenu($lang){
	?>
		<ul class="Menu">
			<li><a href="/<?=$lang?>/index.html">Index</a></li>
			<li><a href="/<?=$lang?>/DocIndex.html">Documentation</a>
				<ul>
					<li><a href="/<?=$lang?>/QuickStart.html">QuickStart</a></li>
					<li><a href="/<?=$lang?>/Terms.html">Explanation of Terms</a></li>
					<li><a href="/<?=$lang?>/pyDCPU_Intro.html">pyDCPU Intoduction</a></li>
					<li id="last"><a href="/<?=$lang?>/SimpleExport.html">Simple Export Tutorial</a></li>
				</ul></li>
			<li><a href="/<?=$lang?>/Download.html">Download</a></li>
			<li><a href="/<?=$lang?>/Contact.html">Contact</a></li>
            <li id="last"><a href="/bugs/" target="_blank">Bugtrack</a></li>
		</ul>
	<?
	}
?>
