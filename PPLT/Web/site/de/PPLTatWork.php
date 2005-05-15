<div class="Head">PPLT at Work</div>
<div class="Text">
	In diesem Dokument m&ouml;chte ein paar Beispiele zeigen und diese kurz
	erleutern. In dem ersten Beispiel habe ich eine Siemens SIMATIC S7-200
	Steuerung an die zweite serielle Schnittstelle angeschlossen. Es werden
	dann die Merker SMB28(ein Byte) und SM0.5(ein Bit) ausgelesen. Des weiteren
	habe ich an die erste serielle Schnitstelle mein Siemens Handy (S55) mit
	einen sog. Datenkabel angeschlossen. Von diesem Telefon lasse ich dann
	den Battriestaus, die Signalqualit&auml;t, der Modellname und den
	Herstellernamen aus lesen.

	<p>Um diese Daten darstellen zu k&ouml;nnen, habe ich die Server
	<i>PPLTWebServer</i> und <i>JVisuServer</i> benutzt. Der erste
	Server ist ein einfacher Web-Server mit dessen Hilfe man mit
	einem Browser (hier Firefox) durch den Symbolbaum
	browsen kann. Der zweite Server stellt den Symbolbaum der
	in Java geschriebenen Visualisierung JVisu bereit.<p>

<pre>
import PPLT;

psys = PPLT.System();
psys.LoadDevice("Mobile.GSMMobilePhone", "handy", {"Port":"0","Speed":"115200"});
psys.LoadDevice("PLC.S7-200", "s7", {"Port":"1","PCAddr":"0","S7Addr":"2"});

psys.CreateFolder("/handy");
psys.CreateSymbol("/handy/battery", "handy::GSM::battery", "DWord");
psys.CreateSymbol("/handy/signal", "handy::GSM::quality", "DWord");
psys.CreateSymbol("/handy/manufacturer", "handy::GSM::manufacturer", "String");
psys.CreateSymbol("/handy/model", "handy::GSM::model", "String");

psys.CreateFolder("/simatic");
psys.CreateSymbol("/simatic/SMB28", "s7::Marker::SMB28", "Byte");
psys.CreateSymbol("/simatic/SM0.5", "s7::Marker::SM0.5", "Bool");

psys.LoadServer("Web.PPLTWebServer", "web", "admin", {"Address":"10.1.1.4","Port":"4711"});
psys.LoadServer("Visu.JVisuServer", "jvisu", "admin", {"Address":"10.1.1.4","Port":"2200"});

while True:
    pass;
</pre>

	<p>Dieses Script l&auml;d also all die Ger&auml;te, erzeugt die Symbole und 
   startet zum Schluss die Server. Wenn sie nun mit ihrem Browser auf die
   Addresse "http://10.1.1.4:4711" gehen,	dann werden sie in etwa folgendes 
   sehen:

	<table style="border:none;" align="center">
	<tr>
	<td>
		<a href="/img/PPLTWeb02.png">
			<img src="/img/pPPLTWeb02.png" alt="Screenshot der Seite" title="PPLTWebServer">
		</a>
	</td>
	<td>
		<a href="/img/PPLTWeb01.png">
			<img src="/img/pPPLTWeb01.png" alt="Screenshot der Seite" title="PPLTWebServer">
		</a>
	</td>
	</tr></table>

	Wenn sie hingegen die Visualisierung JVisu verwenden wollen, kommt auf sie
	ein wenig Konfigurationsarbeit zu. Wenn sie JVisu gestartet haben,
	m&uuml;ssen sie zun&auml;chst einmal ein sog. Panel zusammen stellen.
	So ein Panel umfasst ein oder mehrere Anzeigeelemente, die jeweis mit einem
	Symbol aus dem Symbolbam verbunden werden. das Ergebnis k&ouml;nnte dann
	so aussehen:
	<p align="center">
		<a href="/img/JVisu01.png">
			<img src="/img/pJVisu01.png" alt="Screenshot von einem JVisuPanel" title="JVisu">
		</a>
	</p>
	</p>

	<p>Im folgenden m&ouml;chte ich kurz den Quelltext diskutieren.<br>
	In der ersten Zeile wird mit <i>import PPLT</i> die PPLT-Bibliothek
	eingebunden. Und in der 3. Zeile wird mit dem aufruf
	<i>psys = PPLT.System()</i> ein PPLT-System Objekt erzeugt und
	initialisiert. Bei der Initialisierung werden die Module, Ger&auml;te,
	und Server gesucht und die Benutzerdatenbank (auf die ich hier nicht
	weiter eingehen m&ouml;chte) geladen. Alle darauf folgenden Aktionen
	werden durch den Aufruf einer Methode dieses Objektes veranlasst.</p>

	<p>Die beiden Aufrufe von <i>psys.LoadDevice</i> laden, wie der Name schon 
   sagt, die entsprechenden Ger&auml;te.
	Um so ein Ger&auml;t korrekt laden zu k&ouml;nnen, ben&ouml;tigt das System 
   genaue Informationen. Wie zum Beispiel, welches Ger&auml;t zu laden ist,
	unter welchen Alias (Namen) es sp&auml;ter zu verwalten ist und
	mit welchen Parametern das Ger&auml;t initialisiert werden soll.
	Der Names des Ger&auml;tes, das zu laden ist wird als erster Parameter
	der Methode &uuml;bergen gefolgt von dem Alias, mit dem das erzeugte
	Ger&auml;t dann s&auml;ter identifiziert werden kann. Der letzte Parameter
	ist ein sog. Dictionary, welches die Parameter f&uuml;r das Initialisieren
	des Ger&auml;tes beinhaltet. (So ein <i>Dictionary</i> wird in anderen
   Sprachen auch als <i>Hash</i> oder <i>assoziatives Array</i> bezeichnet.)</p>

	<p>Das Mobiltelefon wird mit den Parametern <i>Port=0</i> und
	<i>Speed=115200</i> geladen, was so viel bedeutet, das das
	Handy an der ersten serielle Schnitstelle (0=COM1, 1=COM2,...)
	angeschlossen ist und diese mit einer &Uuml;bertragungsgeschwindigkeit von
	115200 Baud arbeiten soll.<br>
	Die Parameter f&uuml;r die SIMATIC sind hingegen komplizierter. Diese
	wird &uuml;ber die zweite serielle Schnitstelle (<i>Port=1</i>)
	angesprochen. Da es sich bei dem &Uuml;bertragungsprotokoll
	um PPI handelt, welches ein (echtes) BUS-Protokoll ist,
	m&uuml;ssen beide BUS-Teilnehmer eine Adresse besitzen.
	F&uuml;r den PC w&auml;re das die 0 (<i>PCAddr=0</i>) und
	f&uuml;r die Steuerung die 2 (<i>S7Addr=2</i>).</p>

	<p>Wenn w&auml;rend der initialisierung ein Fehler auftritt und
	das Ger&auml;t nicht geladen werden kann, gibt die Methode
	<i>False</i> zur&uuml;ck. Dies kann man dann mit einer einfachen
	<i>if</i>-Anweisung abfragen. Darauf habe ich bei diesem
	Beispiel aus Gr&uuml;den der &Uuml;bersicht verzichtet.</p>

	<p>Im folgenden Abschnitt will ich die Methodenaufrufe in den Zeilen 7-15 
   genauer erleutern. Alle diese Kommandos manipulieren den Symbol Baum. Der
   Symbol Baum ist ein pseudo (virtuelles) Dateisystem, welches die Werte, die
   aus der Steuerung oder dem Handy ausgelesen wurden, zwischenspeichert
   (cached) und Organisiert.<br>
   Im Gegensatz zu anderen Dateisystemen kennt dieses keine Dateien sondern
   sog. Symbole. Diese Symbole können aber, wie bei normalen Dateisystemen,
   in Verzeichnissen (hier Folder genannt) organisiert werden.</p>

   <p>Damit man den Überblick beh&auml;t, wird zun&auml;chst einmal ein
   Verzeichnis, mit dem Aufruf <i>psys.CreateFolder(VERZEICHNISNAME)</i>
   erzeugt. Danach werden in diesem Verzeichnis verschiedene Symbole
   mit dem Befehl <i>psys.CreateSymbol()</i> erzeugt. Die Parameter dieser
   Methode geben den kompletten Pfad des zu erzeugenen Symbols, die "Buchse"
   des Gerätes, an die das neue Symbol zu koppeln ist und den Typ des Symbols
   an. Die Pfad und die Typ-Angabe will ich hier nicht so sehr besprechen
   da ich denke, dass diese Angabe recht selbstk&auml;rend sind. Einer 
   Erkl&auml;rung bedarf aber die Angbe der "Buchse". Aus dieser "Buchse" 
   versorgt sich das Symbol mit den Daten, die es wiederspiegeln soll. Wenn
   also sp&auml;ter aus diesem Symbol gelesen wird, liest das Symbol zu
   n&auml;chst aus der "Buchse" und wandelt die Rohdaten, die es bekommt 
   entsprechend der Typangabe in einer Wert um und gibt diesen zur&uuml;ck.</p>
   
   <p>Es stellt sich also nur noch die Frage, wo diese Buchsen herkommen. 
   Kurz gesagt: jedes Ger&auml;t stellt eine oder eine Vielzahl dieser Buchsen
   zur verf&uuml;gung. Das erkl&auml;rt auch, warum als erster Teil der 
   "Buchsenangabe" das Alias eines Gr&auml;tes auf taucht. Da jedoch jedes
   Gr&auml;t aus mehreren Kernmodulen bestehen kann und eigentlich nicht das 
   Ger&auml;t sondern die Kern-Module Buchsen zur Verfügung stellen, ist die 
   Angabe in der Mitte erforderlich. Sie teilt dem System mit, welches der
   Kernmodule angesprochen werden soll. Tuen sie aber besser so, als w&uuml;rde
   der mittlere Teil zum Namen der Buchse (letzter Teil) dazugeh&ouml;ren.
   Welche Buchsen das einzelne Gr&auml;t hat, lesen sie bitte in der 
   Dokumentation des jeweiligen Ger&auml;tes nach.</p>




	<p>[Server]</p>
	<p>[Endlosschleife]</p>


</div>
