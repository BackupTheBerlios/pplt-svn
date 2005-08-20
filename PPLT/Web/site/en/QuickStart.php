<div class="TextBody">
	<div class="Head">Requirements</div>
	<div class="Text">
	To install the PPLT you need to have done some preparation. You need to 
	install first the <b>Python interperter</b> version 2.3.0 or higher. You 
	can get it from <a href="http://www.python.org">python.org</a>.

	<p>The next is the grafic-library used by the PPLT tools like <i>PPLT Center</i>
	called <b>wxPython</b>. You need wxPython version 2.5.0 or higher. You can
	download this from <a href="http://www.wxpython.org">wxpython.org</a>. If you 
	only want to use the PPLT library in your own scripts then you may don't need it.</p>

	<p>If you want to use the PPLT under Windows you need to install the <b>pywin32</b>
	extention version 208. You can get it from 
	<a href="http://pywin32.sourceforge.net">pywin32.sourceforge.net</a>. If you use a 
	POSIX like system, for example Linux or BSD you don't need it.</p>

	<p>Some plugins need also some Python-extentions. To find out what extentions are
	needed look at the documentaion of the single plugin. For the GSM, Simatic S7-200,
	Agilent and NAiS modules you will need the <b>pyserial</b> extention from
	<a href="http://pyserial.sourceforge.net">pyserial.sourceforge.net</a>.</b> 
	</div>

	<div class="Head">Install</div>
	<div class="Text">
	To be sure that all will be fine, please install the packages in following order:
	<ol>
		<li><b>Python</b> interpreter</li>
		<li><b>pywin32 (*)</b></li>
		<li><b>wxPython (*)</b></li>
		<li><b>pyserial</b></li>
		<li><b>PPLT</b></li>
	</ol>

	<p>The procedure to install the single packages depends on the System you 
	use. For Windows you will have an executabe installer so it should not be
	a problem.<br>
	Under Linux you should get the source pakages, unpack and complile it. How 
	to do this, please read the README or INSTALL files inside the packages.
	</p>
	</div>

	<div class="Head">Starting the PPLT Center</div>
	<div class="Text">
	If you use Windows you need first to find the place where Python installs
	all scripts that come along the the extentions. Normaly it would be 
	something like <b>C:\Python23\scripts</b>. In this folder you find
	a script called <b>PPLTC.py</b>. This is the PPLT Center. If you double-click
	it, it will be executed. If the install was right you should see now something
	like this:
	<div style="text-align:center">
		<a href="/img/PPLTC01.png">
		<img 	src="/img/pPPLTC01.png"
				alt="The PPLT Center fornt-end."
				title="PPLT Center"></a>
	</div>

	Under Linux you should simply type <b>PPLTC.py</b> at a open terminal. Because Python copy all scripts into 
	<i>/usr/bin</i> or <i>/usr/local/bin</i>. 
	</div>

	<div class="Head">Install Modules</div>
	<div class="Text">
	Now if the Center is running, you can install the Modules. So get the module-package and unpack the ZIP into 
	a folder. The will be a lot of files in it. One called <b>Setup.idf</b>. Now start the PPLT-Center and click 
	on the left menu at the icon labled <i>Module install</i>. You will see a file section dialog. Change to 
	the folder where you unpacked the modules an select the Setup.idf. Now all modules will be installed. 
	</div>

	<div class="Head">The PPLT Center frontend</div>
	<div class="Text">
	The PPLT Center has a realy strange concept of use. You will not find so much buttons like in
	other GUI applications. Because the most actions you will do are in context with a specific item
	of a list or tree. So try to right-click everything you see. If you want to select a item, 
	try a double click (instead of selecting it with a single-click and then click the OK button).

	<p>For example: If you want to load a device, make a right-klick on the empty list of devices.
	In the context-menu select <i>Add device</i>. Now you will see a list off devices; Select 
	the device you want to load with a double-click.</p>

	<p>At the beginning it will be a little bit starange handleing. But later it is quiet fast.</p>
	
	</div>

	<p><b>If you want to know more, or if you have problems; Feel free to <a href="/en/Contact.html">contact</a>
	me.</b></p>
</div>
