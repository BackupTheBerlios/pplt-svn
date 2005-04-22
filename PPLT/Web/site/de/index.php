<div class="TextBody">
    <div class="Head">Neuigkeiten</div>
    <div class="NewsItem">
    <b>2005-03-31 - Release PPLT Version 0.1pre</b><br>
    Ich habe eine Prealpha Version der PPLT Bibliothek
    <a href="http://developer.berlios.de/project/showfiles.php?group_id=3237"
        title="Link zu den Dateien.">frei gegeben</a>.
    Die <span title="Die Kern-Bibliothk wird pyDCPU genannt.">Kern-Bibliothek</span> ist
    durchaus benutzbar, jedoch fehlt die Abstraktions-Schicht vollst&auml;ndig.
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
    Industrie-Steuerungen, zu importieren, diese Daten dann in einem Dateisystem
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
    Symbol-Baum und verwaltet die Benutzter und Gruppen. Wenn sie mehr &uuml;ber die
    Kernbibliothek wissen wollen, lesen sie bitte die
    <a href="/index.php?lang=de&site=pyDCPU_Intro">pyDCPU-Einf&uuml;hrung</a>.

    <p>Der zweite Teil nennt sich PPLT-Bibliothek. Diese Bibliothek setzt auf der
    pyDCPU auf. Sie ist eine Abstraktions-Schicht. Dies ist notwendig um eine
    einfachere Schnittstelle zur pyDCPU zu bieten, als diese zur Verf&uuml;gung stellt.
    Denn anstatt mit einer Vielzahl an Modulen, arbeitet die PPLT Bibliothek
    mit einzelnen Ger&auml;te-Dateien.</p>


    </div>

    <div class="Head">Unterst&uuml;tzte Hardware</div>
    <div class="Text">
    <ul>
        <li><b>NAIS FP0/FP2</b> - Getestet mit dem sog. ToolPort. Es ist auch m&ouml;glich die
        Steuerungen &uuml;ber den getunnelten ToolPort des <b>NAIS Web-Servers</b> zu erreichen.</li>

        <li><b>NAIS A200</b> - Das ist ein industrieller Bild-Pr&uuml;fer. Es ist m&ouml;glich
        diesen &uuml;ber die eingebaute serielle Schnitstelle zu steuern.</li>

        <li><b>Siemens SIMATIC S7-200</b> - Steuerbar &uuml;ber die PPI Schnittstelle.</li>

        <li><b>Siemens S55</b> Mobiltelefon. Ich bin mir sicher, dass auch andere
        GSM konforme Telefone abgefragt werden k&ouml;nnen.</li>
    </ul>
    </div>
</div>
