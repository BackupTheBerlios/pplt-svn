<div class="TextBody">
    <div class="Text">
        <p>Auf dieser Seite will ich ihnen eine (sehr) kurze Einf&uuml;hrung in das
        Konzept der Kernbibliothek, der Potsdamer Prozess Leittechnik geben. Wenn 
        sie mehr wissen wollen, folgen sie bitte den Verweisen innerhab des textes.
    </div>


    <div class="Head">Ziele</div>
    <div class="Text">
        Das Hauptziel was es, ein flexibles, modulares und vor allem plattformunabh&auml;ngiges
        System zu schaffen, das auf Informationen aus verschiedenen Quellen &uuml;ber 
        unterschiedlichste Schnittstellen zugreifen kann, dabei vor allem auf
        Steuerungen und sog. intelligente Sensoren. All diese Informationen sollen
        dann zentral in einem sog. Symbol-Baum abgelegt werden.

        <p>Als Zweites sollte das System eine eigene Benutzer- und Gruppenverwaltung haben
        um den Zugriff auf den Symbol-Baum regeln zu k&ouml;nen.</p>

        <p>Als Letztes sollte es die M&ouml;glichkeit geben, &uuml;ber Module diesen Symbol-Baum wieder
        anderen Systemen zur Verf&uuml;gung zu stellen. So dass man nicht an eine bestimmte Applikation,
        wie zum Beispiel eine Visualisierung, gebunden ist.</p>
    </div>



    <div class="Head">Design</div>
    <div class="Text">
    Im Groben l&auml;sst sich das pyDCPU System in drei Bereiche teilen.

    <p style="text-align:center"><img src="/img/BasicConcept.png" alt="" title="Grundkonzept"></p>

    <p>Der erste Teil ist etwas schwierig zu verstehen, weil sie mit einer Vielzahl
    an Modulen arbeiten m&uuml;ssen. Er ist dazu da, Informationen und Daten aus
    anderen Systemen zu importieren. Dazu ben&ouml;tigt man zum Beispiel, um aus
    den Merkern einer Steuerung zu lesen, ein Modul f&uuml;r die Schnittstelle,
    eins f&uuml;r das BUS-Protokoll und eins das das Kommando-Nachrichtenformat
    der Steuerung implementiert, bevor man die Daten auslesen kann. So m&uuml;ssen
    sie zu mindest wissen, welches BUS-Protokoll, und welche Schnittstelle verwendet
    wird um mit der Steuerung zu kommunizieren. Dies ist jedoch auch einer Vorteile
    des pyDCPU Systems, da sie nun lediglich das Schnittstellen- und das BUS-Modul
    austauschen m&uuml;ssen um mit der Steuerung &uuml;ber einen anderen BUS zu
    kommunizieren.</p>

    <p>Der andere Teil verwaltet diese importierten Informationen in einem
    Dateisystem &auml;hnlichen Symbol-Baum. Stellen sie sich diesen Baum als eine
    Art mini Dateisystem mit Verzeichnissen und Dateien vor. Jede Datei (hier
    Symbol genannt) representiert zum Beispiel einen Merker in einer Steuerung
    oder den aktuellen Wert eines Sensors. Um diese ganzen Symbole besser
    organisieren zu k&ouml;nnen, gibt es Verzeichnisse oder Ordner.<br>
    Wie jedes Datei-System besitzt auch der Symbol-Baum eine Rechteverwaltung,
    mit der sie den Zugriff von Benutzern oder Gruppen auf jedes Symbol oder jedes
    Verzeichnis einzeln regeln.</p>

    <p>Der lezte Teil exportiert diesen Symbol-Baum zu anderen Systemen, wie zum
    Beispiel Visualisierungen oder Datenbanken. Dieser Export-Teil arbeitet auch mit
    Modulen, so dass sie die Daten im Symbolbaum in belibiegen Anwendungen verwenden
    k&ouml;nnen (insofern f&uuml;r diese ein Export-Modul existiert). Es gibt ein
    Export-Modul, das die <a href="/index.php/lang=de/site=SimpleExport">XML-RPC</a> Bibliothek 
    verwendet um den Symbol-Baum zu exportieren. Auf diese Weise k&ouml;nnen sie 
    auf die Symbole in ihren selbgeschriebenen Applikationenen zugreifen.</p>

    Das Beste ist jedoch, dass es in Python geschrieben ist.


    <div class="Head">Zukunft</div>
    <div class="Text">
        Zun&auml;chst habe ich vor, eine stabile Version von PPLT zu ver&ouml;ffentlichen.

        <p>In naher Zukunft will ich noch eine verwendbare Dokumentation
            ver&ouml;ffentlichen.</p>

        <p>Um all dies zu erreichen ben&ouml;tige ich <u>Untersttzung</u>. Ich studiere Physik
        an der Universit&auml;t zu Potsdam und das Schreiben von Open Source Software und
        Studieren gleichzeitig d&uuml;rfte wohl &uuml;ber meine Grenzen gehen. <br>
        Wenn sie also Interesse haben diese Software weiter zu entwickeln,
        melden sie sich bei mir. (Bitte)</p>
    </div>
</div>
