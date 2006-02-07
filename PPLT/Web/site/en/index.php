<div class="TextBody">
    <div class="Head">News
		<a style="font-size:0.5em;" href="/en/NewsHistory.html">[History]</a>
	</div>
    <div class="NewsItem">
    <b>2006-02-04 - Website update and bug-tracking</b><br>
    There were now an open <a href="/bugs/" target="_blank">bug-tracking</a>
    system and two <a href="/en/Contact.html">mailing-lists</a>.  You can 
    simply report bugs and feature-requests by the bug-track without register 
    your self using the predefined <i>guest-account</i>.<br><br>
    <b>2005-08-20 - Bug-fix Release of PPLT Version 0.3.1</b><br>
	I've done a lot of testing and debugging. Also I've wrote
	a post-install script for the windows-installer, that creates
	a folder in the start menu.<br>
	<u>Please update!</u><br><br> 
	<b>2005-08-20 - Release of PPLT Version 0.3.0</b><br>
	I've done a lot of debugging and (sometimes) rewriting
	wide parts of the PPLT library. Will stop now developing
	to focus on debugging to reach the stable state.
	<u>Note:</u> Please also update the modules!<br><br>
	<b>2005-06-03 - Release of PPLT Version 0.2.2</b><br>
	I've added some features to the library and the PPLTC application.
	You can now save a session and load it later. Also I've fixed
	some bugs and the German translation of PPLTC.<br><br>
    </div>



	<div class="Head">Help Wanted</div>
	<div class="Text">I need some people who help me to test and debug the
	software. I want to reach as fast as possible the stable state. So
	it would be nice, if you test the PPLT at your platform and 
	<a href="/en/Contact.html">report me</a> any appearing problem.
	
	<p>Also you can contact me, if you have problems with the handling
	of the GUI application so I can improve the GUI.</p>
	</div>

    <div class="Head">What is PPLT</div>
    <div class="Text">
    PPLT is an open framework for any master-slave orientated communication. It was written in
    Python and it is licensed under the GNU LGPL. It is designed as a Python
    library, so you can use it in your own applications. It is modular, that
    means the number of devices supported by the PPLT-System depends on the
    modules you are using.

    <p>The main targets are to be able to import data from very different systems like controllers,
    manage them into a single file-system-like symbol-tree and export them to
    other systems like visualisations. So you can also use it for data-invention etc...
    </p>

    <p>On the other hand it is still a library. So you can use it to access data
    from systems that are supported. Until now there are modules for some PLCs,
    mobile phones etc. So it makes no difference to access status information from
    a mobile phone like battery-level or the current status of the output-coils of
    an industry controller (<span title="Programable Logic Controller">PLC</span>).</p>
    </div>

    <div class="Head">Design</div>
    <div class="Text">
    The PPLT system consists of two parts. The first is the core library called
    <span title="PYthon Data Collect and Process Unit">pyDCPU</span>. This unit
    loads and unloads the modules, takes care about the central symbol-tree and handles
    users/groups. If you want to know more about the core library please take a look
    at the pyDCPU
    <a href="/en/pyDCPU_Intro.html"
        title="Intoduction into the pyDCPU Core library.">introduction</a>.

    <p>The second part is called PPLT-Library. This library is built on the top
    of pyDCPU. It is an abstraction-layer. This is necessary for providing an 
    </div>
    
    <div class="Head">Supported Hardware/Software</div>
    <div class="Text">
    <ul>
        <li><b>Panasonic FP0/FP2</b> - I tested them over the ToolPort. It was
        also possible to access them over the tunnelled ToolPort of an
        <b>Panasonic FPWEB Web-Server</b>.

        <li><b>Panasonic A200</b> - This is an industrial image-checker. To
        access it I used the built in RS232 port.

        <li><b>Siemens SIMATIC S7-200</b> - I used the PPI-Cable in
        <i>FreePort</i> mode.

        <li><b>Siemens S55</b> mobile phone. I am sure that other GSM
        compatible mobile phones will also work fine.</li>
		
		<li><b>Agilent 5462X</b> Oscilloscopes. You can measure frequency,
		amplitude etc. of signals.</li>

		<li><b>JVisu 1.0</b> This is an open-source visualisation written in Java.
		There is a server module to export the symbol-tree to this application.</li>

		<li>A <b>Simple HTTP</b> web-server is also available as a server module.
		So you can browse the symbol-tree with the FireFox or another web-browser.</li>

		<li>A <b>XML-RPC</b> server module called <i>SimpleExport</i> serves
		you the symbol-tree for nearly every programming language on every platform.
		So you can get access to the collected data within your own applications.</li>
    </ul>
    </div>
</div>
