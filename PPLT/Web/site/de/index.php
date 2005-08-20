<div class="TextBody">
    <div class="Head">Neuigkeiten
		<a href="/de/NewsHistory.html" style="font-size:0.5em;">[Archiv]</a>
	</div>
    <div class="NewsItem">
	<b>2005-08-20 - PPLT Version 0.3.0</b><br>
	Ich habe weite Teile der PPLT bibliothek 
	debuged und auch streckenweise neu geschrieben.
	Ich beende nun die Entwicklung um mich auf
	das Entfernen von Fehlern zu konzentrieren.
	<u>Hinweis:</u> Bitte laden sie sich auch
	die neuen Module herunter!<br><br>
	<b>2005-06-03 - PPLT Version 0.2.2</b><br>
	Ich habe einige nette Kleinigkeiten erweitert.
	So k&ouml;nnen sie jetzt eine Sitztung im PPLTC speichern
	und sp&auml;ter fortsetzen. Desweiteren habe ich einige
	Fehler der Vorversion behoben, vor allem in der 
	deutschen &Uuml;bersetzung. Ich w&uuml;rde ihnen also
	raten diese zu nutzten.</br><br>
	<b>2005-05-28 - BugfixRelease (0.2.1)</b><br>
	Ich habe einige unangenehme Fehler in der Bibliothek
	sowie in der Applikation entfernt. Ich empfehle ihnen
	auf diese Version zu aktualisieren. Des weitren habe
	ich den <i>gettext</i> Support in das PPLT Center
	eingepflegt.<br><br>
    </div>

    <div class="Head">Was ist PPLT</div>
    <div class="Text">
    PPLT ist ein quell-offenes Framework f&uuml;r die industrielle Kommunikation.
    Es wurde in Python geschrieben und ist unter der GNU LGPL lizensiert.
    Es ist als Python-Bibliothek gedacht, so dass sie es in ihren eigenen
    Applikationen nutzen k&ouml;nnen. Des Weiteren ist es modular aufgebaut,
    so dass die Anzahl der unterst&uuml;tzten Ger&auml;te von den verwendeten Modulen
    abh&auml;ngt.
    
    <p>Das Hauptziel ist es, Daten von unterschiedlichen Systemen, wie zum Beispiel
    Industrie-Steuerungen, zu importieren, diese Daten dann in einem dateisystem
    &auml;hnlichen <i>Symbol-Baum</i> zu verwalten und anderen Systemen, wie zum Beispiel
    Visualisierungen, zur Verf&uuml;gung zu stellen. Es kann so zum Beispiel f&uuml;r die
    Datenerfassung genutzt werden.</p>

    <p>Auf der anderen Seite bleibt es dennoch eine simple Python-Bibliothek. So
    k&ouml;nnen sie auf einfache Weise auf Daten von unterst&uuml;tzten Systemen zugreifen.
    Bis jetzt gibt es Module f&uuml;r einige Steuerungen, Handys, usw. Da die
    Schnittstelle (API) immer die gleiche ist, macht es keinen Unterschied ob
    sie den Ladestand des Handys oder die aktuellen Ausg&auml;nge einer Steuerung abfragen.
    </div>

    <div class="Head">Design</div>
    <div class="Text">
    Das PPLT System besteht im wesentlichen aus 2 Teilen. Zun&auml;chst aus der
    Kernbibliothek, die <span title="PYthon Data Collect and Process Unit">pyDCPU</span>
    genannt wird. Diese Bibliothek l&auml;d und entfernt die Module, k&uuml;mmert sich um den
    Symbol-Baum und verwaltet die Benutzer und Gruppen. Wenn sie mehr &uuml;ber die
    Kernbibliothek wissen wollen, lesen sie bitte die
    <a href="/de/pyDCPU_Intro.html">pyDCPU-Einf&uuml;hrung</a>.

    <p>Der zweite Teil nennt sich PPLT-Bibliothek. Diese Bibliothek setzt auf der
    pyDCPU auf. Sie ist eine Abstraktions-Schicht. Dies ist notwendig, um eine
    einfachere Schnittstelle zur pyDCPU zu bieten, als diese zur Verf&uuml;gung stellt.
    Denn anstatt mit einer Vielzahl an Modulen, arbeitet die PPLT Bibliothek
    mit einzelnen Ger&auml;te-Dateien.</p>


    </div>

    <div class="Head">Unterst&uuml;tzte Hardware/Software</div>
    <div class="Text">
    <ul>
        <li><b>NAIS FP0/FP2</b> - Getestet mit dem sog. ToolPort. Es ist auch m&ouml;glich die
        Steuerungen &uuml;ber den getunnelten ToolPort des <b>NAIS Web-Servers</b> zu erreichen.</li>

        <li><b>NAIS A200</b> - Das ist ein industrieller Bild-Pr&uuml;fer. Es ist m&ouml;glich
        diesen &uuml;ber die eingebaute serielle Schnittstelle zu steuern.</li>

        <li><b>Siemens SIMATIC S7-200</b> - Steuerbar &uuml;ber die PPI Schnittstelle.</li>

        <li><b>Siemens S55</b> Mobiltelefon. Ich bin mir sicher, dass auch andere
        GSM konforme Telefone abgefragt werden k&ouml;nnen.</li>
    	
		<li><b>Agilent 5462X</b> Ozilloskope. Sie k&ouml;nnen die Frequenz, 
		Aplitude, u.s.w der anliegenden Signale messen.</li>
	
		<li><b>JVisu</b> ist eine in Java geschriebene (freie) Visualisierung. Mit dem
		Servermodul k&ouml;nnen sie den Symbolbaum zu JVisu exportieren.</li>

		<li>Ein einfache <b>HTTP</b> Webserver ist ebenfalls als Servermodul
		vorhanden. So k&ouml;nnen sie den Symbolbaum mit ihrem Webbrowser (z.B. Firefox)
		durchsuchen.</li>

		<li>Ein <b>XML-RPC</b> Server, der hier <i>SimpleExport</i> genannt wird,
		erm&ouml;glicht es ihnen auf die Werte im Symbolbaum, mit fast jeder 
		Programmiersprache und auf jeder Plattform, zuzugreifen.</li>
	</ul>
    </div>
</div>
