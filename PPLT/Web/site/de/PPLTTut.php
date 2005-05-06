<div class="TextBody">
	<div class="Head">Vorbereitung</div>
	<div class="Text">
		<p>Bevor sie PPLT installieren und nutzen k&ouml;nnen m&uuml;ssen 
		bestimmte Abh&auml;ngigkeiten erf&uuml;llt sein.
		So sollten sie auf jeden Fall den Python-Interpreter mit der Version 
		&gt;= 2.3.0 installiert haben. Dies ist notwendig, 
		da PPLT eigentlich eine Python-Bibliothek ist und die 
		dazugeh&ouml;rigen Scripte (Programme) nicht ohne diesen Interperter
		ausgef&uuml;hrt werden k&ouml;nnen. Der Python-Interpreter kann von der URL 
		<a href="http://www.python.org">http://www.python.org</a> herunter 
		geladen werden.</p>

		<p> Als n&auml;chstes ben&ouml;tigen sie einige Bibliotheken um PPLT 
		ausf&uuml;hren zu k&ouml;nnen. Welche dieser Bibliotheken die
		ben&ouml;tigen, h&auml;ngt stark von dem Betriebsystem ab, das sie verwenden.<br>
		Sollten sie ein Windows verwenden, ben&ouml;tigen sie unbedingt noch 
		die <a href="http://pywin32.sf.net">PyWin32 Extention</a>, die 
		den Zugriff auf Ressourcen, wie der seriellen Schnittstelle, unter Windows zur 
		Verf&uuml;gung stellt.</p>

		<p>Unabh&auml;ngig vom Betriebsystem sollten sie auch die 
		<a href="http://pyserial.sf.net">PySerial Bibliothek</a> installieren.
		Diese Bibliothek wird von dem Modul f&uuml;r die serielle Schnittstelle 
		verwendet. Fall sie sich sicher sind, dass sie die
		serielle Schnittstelle nicht verwenden werden, k&ouml;nnen sie auch auf 
		diese Bibliothek verzichten.</p>

		<p>Wenn sie die PPLT nicht nur als Bibliothek benutzen, sonder auch die 
		teils grafischen Scripte verwenden wollen,
		sollten sie die <a href="http://www.wxpython.org">wxPython Bibliothek</a> 
		installieren. Diese Bibliothek bietet eine Platformunabh&auml;ngige
		API zur grafischen Oberfl&auml;chenprogrammierung und wurde in einigen 
		Scripten, die zur PPLT geh&ouml;ren verwendet.</p>  
		
		<p>Es ist durchaus m&ouml;glich, dass die Standardbibliothek von Python 
		bei einigen Linux Distributoren auf mehrere Pakete verteiel wurde. Dies ist 
		zum Beisiel bei SuSE Linux 8.x der fall. Daher sollten sie darauf 
		acheten, dass auch die XML Unterst&uuml;zung f&uuml;r Python installiert 
		ist.</p>

		<p>Sollten alle Abh&auml;ngigkeiten aufgel&ouml;st sein, k&ouml;nnen 
		sie mit der Installation der PPLT beginnen. Sollten sie dennoch ein 
		Paket vergessen,
		oder ich eine Abh&auml;ngigkeit &uuml;bersehen haben, so wird bei dem 
		Ausf&uuml;hren eines Scriptes, das die PPLT verwendet ein Fehler auftreten, anhand
		dessen sie erkennen k&ouml;nnen, welche Abh&auml;nigkeit nicht 
		aufgel&ouml;st wurde.</p>
	</div>

	<div class="Head">PPLT Installieren</div>
	<div class="Text">
		<p>Sind alle Vorbereitungen getroffen, k&ouml;nnen sie die PPLT 
		Bibliothek und die dazgeh&ouml;rigen Scripte installieren. Die 
		Installation der Bibliothek	
		verl&auml;uft automatisch. Lediglich das installieren der Module, 
		Ger&auml;te und Server verlangt das ausf&uuml;hren eines Scriptes.</p>

		<p>Die installation h&auml;ngt wider stark vom Betriebssystem, das sie 
		verwenden ab. Der Aufwand jedoch unterscheidet sich kaum. Wenn sie mit 
		Windows arbeiten,
		k&ouml;nnen sie den vorbereiteten Installer (EXE) verwenden. F&uuml;hren 
		sie dazu diesen installer aus und folgen sie den Anweisungen des Dialoges. 
		F&uuml;r Linux 
		Systeme, die den RPM Paketmanager installiert haben (alle SuSE und RedHat), 
		ist der Aufwand &auml;hnlich niedrig. wechseln sie also auf der Konsole 
		in das Verzeichnis, in dem die 
		Installationsdatei liegt und f&uuml;ren sie <i>rpm -i PPLT-0.1pre2.rpm</i> 
		aus. Es kann sein, dass sich die Versionsnummer ihrer Datei von diesem Beispiel
		unterscheidet. Also allgemein <i>rpm -i PPLT-[VERSION].rpm</i>.</p>

		<p>F&uuml;r alle Platformen kann alternativ auch folgende Installation 
		vorgenommen werden. Enpacken sie das Archiv, das die Quellen von PPLT 
		beinhaltet. Wechseln sie auf der Konsole in 
		das enpackte Verzeichnis. Dieses sollte PPLT hei&szlig;en. In diesem 
		Verzeichnis liegt eine Datei mit dem Namen <i>setup.py</i>.  Geben sie 
		nun <i>python setup.py install</i> ein.
 		Nun sollte die Bibliothek installiert werden.</p>

		<p>Sind die Bibliothek und die Scripte (werden automatisch installiert) 
		installiert, m&uuml;ssen sie daf&uuml;r sorgen, dass diese von ihrer 
		Kommandozeile auch gefunden werden.
		Wenn sie mit Linux arbeiten, k&ouml;nnen sie diesen Schrit 
		&uuml;berspringen, da Python die Scripte in das Verzeichnis 
		<i>/usr/bin</i> oder <i>/usr/local/bin</i> kopiert hat und
		die Kommandozeile mei&szlig;t in diesen Verzeichnissen sucht. Unter 
		Windows m&uuml;ssen sie zun&auml;chst nach diesen schripten suchen. 
		Sie liegen im allgemeinen in dem Verzeichnis 
		<i>Scripts</i> in dem Python-Verzeichnis. Meist w&auml;re das 
		<i>C:\PYTHON23\Scripts</i> oder <i>C:\Programme\PYTHON23\Scripts</i>. 
		Oder suchen sie nach einer Datei, die 
		<i>PPLTModInstall.py</i> hei&szlig;t. Haben sie das Verzeichnis, in dem 
		diese Datei liegt gefunden, m&uuml;ssen sie den vollen Pfad zu diesem 
		Verzeichnis zu der <i>PATH</i> 
		Umgebungsvariable hinzuf&uuml;gen. Das tuen sie, indem sie zum Beispiel 
		<i>PATH = PATH;C:\PATHON23\Scripts</i> 
		in ihrer Kommandozeile eingeben. Diese wird aber Variable gel&ouml;scht, 
		sobald sie die Kommandozeile schlie&szlig;en. Wie sie dies verhindern 
		k&ouml;nnen, h&auml;ngt stark von ihrer Windows-Version ab. Schlagen 
		sie bitte dazu im 
		Windows-Handbuch oder in der Hilfe unter dem Thema "Umgebungsvariablen" nach</p>
	
		<p>Jetzt sollten sie die Kern-Module, Ger&auml;te und Server 
		installieren, damit sie PPLT &uuml;berhaupt einsetzen k&ouml;nnen. 
		Die Kern-Module stellen die Unterst&uuml;zung f&uuml;r eine Schnittstelle
		oder ein Protokoll zur Verf&uuml;gung. Ein "Ger&auml;t" ist eine Datei, 
		in der beschrieben wird, wie diese Kern-Module zu kombinieren sind, 
		damit ein bestimmes Ger&auml;t, zum Beispiel eine
		Steuerung angesprochen werden kann. Server stellen dann die 
		verf&uuml;gbaren Informationen anderen Systemen wie zum Beispiel 
		Visualisierungen oder einfach einem Web-Browser bereit. <br>
		Diese Module sind in einem ZIP Archiv zusammen gefasst. Entpacken sie 
		das Archiv in ein Verzeichnis und wechseln auf der Konsole in dieses. 
		Geben sie nun 
		<i>PPLTModInstall.py setup.xml</i> ein. Nun sollten alle darin 
		enthaltenen Modul-, Ger&auml;te- und Server-Dateien in das PPLT System 
		installiert werden. 
		Damit ist die Installation der PPLT abgeschlossen.</p>
	</div>
	
	<div class="Head">Erste Schritte</div>
	<div class="Text">
		<p>Es ist nun alles vorbereitet die ersten Schritte zu tun. Und f&uuml;r diese ist 
		keine besondere Hardware n&ouml;tig, auch wenn dadurch die Beispiele etwas 
		unspektakul&auml;r sind. Sollten sie jedoch im Besitz von Ger&auml;ten sein, die von
		der PPLT unterst&uuml;tzt werden, sollten sie so bald wie m&ouml;glich diese versuchen an
		zusprechen. Bei allen Beispielen werde ich den Zufallsgenerator als Datenquelle 
		nutzen. Wie gesagt, etwas unspektakul&auml;r. Jedoch sollten sie immer im Hinterkopf
		behalten, dass es vom Aufwand her v&ouml;llig egal ist, ob sie nun einen Zufallsgenerator
		auslesen oder eine Industrie-Steuerung oder eben ein digitales Oszilloskop. Es &auml;dern
		sich schlicht der Name und ein paar Parameter. Die Handhabung jedoch bleibt immer die selbe.</p>

		<p>Ich werde ihnen zun&auml;chst zeigen, wie sie mit der PPLT eigene Scripte schreiben. Dazu sollten
		sie ein wenig mit Python vertraut sein. Aber wirklich nur elementares Wissen, wie eine Bedingung in
		Python realisiert wird, Schleifen und vieleicht was eine Funktion oder Methode ist.</p>
	</div>

	<div class="Head">Ger&auml;te laden</div>
	<div class="Text">	
		<p>Ich m&ouml;chte damit anfangen, ihnen zu zeigen, wie sie die PPLT Bibliothek laden und
		das PPLT-System starten. Dazu ein Quelltext-Schnipsel:
<pre>
import PPLT;
psys = PPLT.System();
</pre>
		In diesem Beispiel sehen die, wie die PPLT Bibliothek geladen wird, n&auml;mlich  mit <i>import PPLT </i>
		wenn sie ein wenig mit Python vertraut sind wird ihnen dies sehr bekannt vor kommen. Wenn jedoch nicht, 
		empfehle ich ihnen einen Python Einf&uuml;hrungskurs. Keine Angst, Python ist wohl die Programmiersprache,
		die am schnellsten gelernt ist.<br>
		Mit <i>psys = PPLT.System()</i> erzeugen sie eine Instanz der Klasse <i>System</i> aus der Bibliothek 
		<i>PPLT</i> und speicher diese in <i>psys</i>. Eine Instanz nennt man in 
		anderen Programmiersprache auch gerne Objekt. So ein Objekt hat auch
		meist so genannte Methoden. Das sind Funktionen, die zu diesem Objekt geh&ouml;ren.<br>
		Ich habe jetz also ein Objekt (<i>psys</i>) welches das gesammte PPLT-System 
		representiert und jede Aktion wird über das Aufrufen einer Methode dieses
		Objektes iniziiert. Oder salop gesagt, wenn ich ein Ger&auml;t einbinden
		m&ouml;chte, rufe ich die Methode "LoadDevice()" auf.</p>

		<p>Und genau das mache ich jetzt. Ich lade also das "Ger&auml;t" 
		<i>RandomGenerator</i>.
<pre>
import PPLT

psys = PPLT.System();
psys.LoadDevice("Debug.RandomGenerator", "zufall", {});
</pre>
		Dies ist der Code um das "Ger&auml;t" <i>RandomGenerator</i> zu laden. 
		Das <i>Debug</i> bedeutet nich viel ist aber wichtig. Es ist der Kontainer,
		in dem das "Ger&auml;t" aufbewart wird. Au&szlig;erdem dient so ein Kontainer der
		Klassifizierung. Das hei&szlig;t, alle Ger&auml;te, die irrgendwas miteinander
		zu tun haben, liegen in dem selben Kontainer. Tun sie am besten so, als 
		w&uuml;rde das <i>Debug</i> zum Namen dazugeh&ouml;ren. Was hat nun die 
		Zeichenkette <i>"zufall"</i> zu sagen? Nun, ich habe damit dem Ger&auml;t 
		einen <u>eindeutigen</u> Namen gegeben. Wenn ich nun sp&auml;ter genau dieses
		Ger&auml;t wieder ansprechen m&ouml;chte, dann brauche ich diesen Namen um
		es Indentifizieren zu k&ouml;nnen, wenn ich es zum beispiel wieder l&ouml;schen 
		m&ouml;chte.</p>

		<p>Bevor ich das tue, m&ouml;chte ich aber noch auf ein paar andere Dinge zu 
		sprechen kommen. Da w&auml;ren zum Beispiel die geschweiften Klammern oder was
		passiert, wenn es beim Laden einen Fehler gibt. Doch zun&auml;chst zu den 
		Klammern. An dieser Stelle sind die Parameter, die das Ger&auml;t ben&ouml;tigt,
		einzusetzen. Da jedoch der Zufallsgenerator keine Parameter ben&ouml;tigt,
		bleiben diese leer. Sind jedoch Werte anzugeben, sollte es so aussehen:
		<i>{"Parameter1":"Wert", "Parameter2":"Wert"}</i>.</p>

		<p>Nun was passiert aber, wenn es beim Laden eines Moduls ein Fehler auftritt?
		Im allgemeinen nichts. Das Ger&auml;t wird nicht geladen und die Methode gibt
		<i>False</i> zur&uuml;ck. Und im Falle des Erfolges <i>True</i>. Diese Boolschen
		Werte kann man mit einer "If" Bedingung abfragen. Im Beispiel von oben.
<pre>
import PPLT;
import sys;

psys = PPLT.System();
if not psys.LoadDevice("Debug.RandomGenerator","zufall",{}):
	print "Fehler beim Laden...";
	sys.exit();
</pre>
		Die "If" Bedingung in der 4. Zeile pr&uuml;ft ob die Methode "Wahr" zur&uuml;ck
		gegeben hat. Ist dies nicht der Fall, dann wird der einger&uuml;ckte Block
		ausgef&uuml;hrt. Der Aufruf <i>sys.exit()</i> bedeutet, dass an dieser Stelle
		die Ausf&uuml;hrung des Programmes abgebrochen wird.</p>

		<p>Das Entladen der Ger&auml;te ist sogar noch einfacher als das Laden. Wie immer,
		ist diese Aktion ein Aufruf einer Methode. Wie auch beim laden, k&ouml;nnen dabei
		Fehler auftreten, die das Entladen verhindern. Wenn sie zum Beispiel versuchen
		ein Ger&auml;t zu entladen, das sie noch garnicht geladen haben. Doch zun&auml;chst
		ein Beispiel Script:
<pre>
import PPLT;
import sys;

psys = PPLT.System();
if not psys.LoadDevice("Debug.RandomGenerator","zufall",{}):
	print "Fehler beim Laden...";
	sys.exit();
print "geladen...";

print "entlade...";
if not psys.UnLoadDevice("zufall"):
	print "Fehler beim entladen";
	sys.exit();
print "ok...";
</pre>
		Ich denke dass sich dieses Beispiel selbst erkl&auml;rt. Vieleicht w&auml;re es an der Zeit ein Kommentar
		zu den Semikolon zu geben. Diese werden vom Python-Interpreter schlich weg ignoriert. Ich selber
		Progrmmiere noch sehr viel C, so dass ich diese Semikolon am Zeilenende eher aus Reflex setze als
		aus &Uuml;berlegung.
		</p> 
		
		<p>Ich m&ouml;chte damit dieses Kapitel &uuml;ber das Ent-/Laden von Ger&auml;ten abschlie&szlig;en.
		Sie sollten nun wissen, wie sie Ger&auml;te in das System einbinden k&ouml;nnen und wie sie diese
		auch suber wieder los werden. Im n&auml;chsten Abschnitt will ich ihnen zeigen wie sie nun auf die
		Werte, die das Ger&auml;t liefern kann, zugreifen.</p>
	</div>

	<div class="Head">Der Symbol Baum</div>
	<div class="Text">
		<p>Bis jetzt ging es ja recht beschaulich zu. Sie haben gelernt, wie man das 
		System startet, ein Ger&auml;t l&auml;d und wie man dieses wieder entl&auml;d.
		Jedoch ist dies so spannend wie die Vorlesungen meines Informatik 
		Professors.</p>

		<p>Ich kann ihnen Versprechen, dass es nicht wirklich aufregender wird, insofern 
		sie keine Hardware haben, die sie mit diesem System auslesen k&ouml;nnen. Zu mindest
		werden jetzt so etwas wie Ergebnisse sichtbar. Nicht nur eine Methode, die
		behauptet, sie habe etwas getan.</p>

		<p>In der &Uuml;berschrift habe ich schon den zentralen Begriff dieses Kapitels
		genannt: <b>Symbol Baum</b>. Ich m&ouml;chte zu n&auml;chst versuchen zu erkl&auml;ren,
		was ein Symbol Baum &uuml;berhaut ist. Nat&uuml;rlich hat dieser Baum nicht sehr viel
		mit den gr&uuml;nen Objekten au&szlig;erhab ihres Raumes zu tun. Sondern eher mit dem
		Begriff des Baumes in der Informatik. Wenn sie mehr dazu wissen wollen empfehle ich
		ihnen den <a href="http://www.wikipedia.de">Wikipedia</a> Artikel zu diesem Thema. Ich bin
		mir aber auch sehr sicher, dass sie von solchen B&auml;umen schon einmal geh&ouml;rt
		haben. Und zwar im Zusammenhang mit ihrem Datiesystem. Ein Verzeichnisbaum, wie der 
		ihres Betriebsystems, kommt der Vorstellung des Symbolbaumes recht nahe. Der 
		Symbolbaum ist so zu sagen ein mini (virtuelles) Dateisystem. Es kennt 
		Verzeichnisse oder Ordner, besitzt aber anstatt Dateien so genannte Symbole.
		Diese Symbole beinhalten Werte. So ein Wert, kann zum Beispiel eine Zufallszahl
		oder aber auch der Zustand eines Ventils sein.<p>
	
		<p>Befor ich darauf zu sprechen kommen, wie die Symbole ihre Werte bekommen,
		m&ouml;chte ich ihnen noch etwas mehr &uuml;ber die Verzeichnisse und Symbole
		erz&auml;hlen. Wenn sie schon einmal mit einem Linux oder Unix System gearbeitet
		haben, wird ihnen dieses virtuelle Dateisystem irrgentwie bekannt vorkommen.</p>
	
		<p>Wenn sie das System laden, wird der SymbolBaum leer sein. Und es ist ihre 
		Aufgabe diesen mit leben zu f&uuml;llen. Das unterste Verzeichnis (auch 
		Wurzel genannt) hei&szlig; <i>/</i>. Ein Verzeichnis mit dem Namen <i>abc</i>,
		das direkt im Wurzelverzeichnis liegt, hat dann den Pfad <i>/abc</i> und ein 
		Symbol mit dem Namen <i>123</i>, das im Verzeichnis <i>/abc</i> liegt, hat den
		Pfad <i>/abc/123</i>. Als Merksatz: Verzeichnisebenen werden durch <i>/</i>
		getrennt, wobei <i>/</i> das Wurzelverzeichnis ist. Desweiteren: 
		Verzeichnisse, so auch das Wurzelverzeichnis, k&ouml;nnen Verzeichisse und 
		Symbole aufnehmen. Symbole stellen die "Dateien" dieses Dateisystems dar und
		k&ouml;nnen daher keine weiteren Symbole oder gar Verzeichnisse aufnehmen.</p>

		<p>Ich hoffe, meine Ausf&uuml;hrungen waren verst&auml;ndlich und sie ahnen 
		wozu dieser Symbolbaum existiert. Er spielt eine zentrale Rolle in dem ganzen
		System. Mit diesem Baum kontrolieren sie wer auf welchen Wert wie zugreifen darf.
		Wenn sie aus einem Symbol lesen, lesen sie eigentlich aus einem Ger&auml;t. Da
		sie, wenn sie in ein Symbol schreiben, damit auch in das Ger&auml;t schreiben,
		sollten nat&uuml;rlich nicht alle Werte, die das Ger&auml;t besitzt, gelesen oder
		geschrieben werden d&uuml;rfen. Es kann also generell nur auf die Werte lesend
		oder schreibend zugegriffen werden, die durch ein Symbol explizit zur 
		Verf&uuml;gung stehen. Und jetzt der kn&uuml;ller: sie k&ouml;nnen 
		Zugriffsrechte vergeben und damit sehr genau regeln, welcher Benutzter
		auf welche Symbole und damit auf Ger&auml;te, wie zugreifen darf.
		Doch dies ist leider nicht Inhalt dieses Tutoriums. Ich m&ouml;chte
		nur, dass sie wissen, das das m&ouml;glich ist.</p>

		<p>Nach all dieser Theorie werde ich ihnen endlich zeigen, wie sie
		nun konkret Symbole erzeugen. Wie immer ist dies ein Aufruf einer
		Methode. Also gleich einmal ein Beispiel:
<pre>
import PPLT;
import sys;

psys = PPLT.System();
if not psys.LoadDevice("Debug.RandomGenerator","zufall",{}):
	print "Fehler beim Laden...";
	sys.exit();

if not psys.CreateSymbol("/rand_zahl","zufall::Generator::DWord","DWord"):
	print "Fehler beim anlegen eines Symbols";
	sys.exit();
</pre>
		Jetzt k&ouml;nnte es etwas kompliziert werden. Wie sie sehen, werden 3 Zeichenketten
		als Parameter der Methode <i>CreateSymbol</i> &uuml;bergeben. Die erste ist recht 
		einfach zu verstehen. Sie gibt den Pfad des zu erzeugenden Symbols an. Also, wenn
		alles gut geht, dann exisitiert nach diesem Aufruf ein Symbol im Wurzelverzeichnis
		mit dem Namen <i>rand_zahl</i>. Der letzte String gibt den Type des Symbols an. 
		In diesem Fall ist es <i>DWord</i> was so viel wie "Doppel Wort" bedeutet. Das ist
		eine 32Bit Zahl, die mit dem Integer Typ der Programmiersprache C zu vergeichen ist.
		Von solchen Typen gibt es nat&uuml;rlich noch mehr. Da w&auml;ren <i>Bool</i> 
		was ein einzelnes Bit dartstellt. <i>Byte</i> Was 8 Bit also ein Byte darstellt.
		Ich h&auml;tte da noch <i>Word</i> eine 16Bit Zahl. Die Zahlen mit Komma 
		hei&szlig;en <i>Float</i> und <i>Double</i> und zuletzt noch die Zeichenkette
		die <i>String</i> hei&szlig;t.</p>

		<p>Der Zeichenkette in der Mitte m&ouml;chte ich einen eigenen Absatz widmen. 
		Dieser String beschreibt, woher das Symbol seine Werte zu holen hat. Er 
		besteht immer aus 3 Teilen, die durch zwei Doppelpunkte getrennt werden.
		Der erste Teil gibt den Namen des Ger&auml;tes an, auf dessen Daten 
		wir zugreifen wollen. Welche der vielen Daten das Symbol zu holen hat,
		sagen die n&auml;chsten 2 Teile. Der erste nennt sich Namensraum und
		soll uns nicht so sehr interessieren. Zun&auml;chst ist der letzte Teil
		wichtig. In diesem Fall hei&szlig;t der <i>DWord</i>. Ich gebe zu, dass 
		ich diesen Namen recht dumm gew&auml;hlt habe. Er ist zu leicht mit der
		Typangabe zuverwechseln. Was er aber zu bedeuten hat, will ich ihnen
		wie folgt erkl&auml;ren. Stellen sie sich bitte das Ger&auml;t als
		eine Box vor mit einigen Anschl&uuml;ssen. In diesem Fall ist die Box 
		ein Zufallsgenerator und hat einige Anschl&uuml;sse. Einer zum Beispiel
		hei&szlig;t <i>Bool</i> und liefert einen boolschen Zufallswert. Ich habe
		in dem oberen Script den "Anschluss" <i>DWord</i> gew&auml;hlt, welcher einen
		Zufallswert des Typs Doppelwort liefert. Was ich auch noch betonen m&ouml;chte
		ist, dass diese Anschluss Namen nicht immer etwas &uuml;ber den Typ der Wertes	
		aussagen. Dies ist lediglich bei dem Zufallsgenerator der Fall.</p>
  	
		<p>Die Notwendigkeit eines Namesraumes ist vielleicht etwas verwirrend. So ein Ger&auml;t,
		wie der Zufallsgenerator eines ist,  besteht im innern meist aus mehreren so 
		genannten "Modulen". Nun kann es vorkommen, dass all diese Module Werte liefern k&ouml;nnen
		und vor allem, dass sich bei diesen "Anschl&uuml;ssen" einige Namen &uuml;berschneiden 
		k&ouml;nnen. Desshalb gibt es diesen Namensraum, der all diese Anschl&uuml;sse voneinander
		trennt. Die technischen Details sollen hier nicht weiter von Interesse sein. Welche 
		Namesr&auml;ume der Ger&auml;t besitzt und welche Anschl&uuml;sse der jeweilige Namesraum
		bietet, entnehmen sie bitte der Dokumentation.</p>

		<p><u><b>Zusammenfassung:</b></u> Sie erzeugen ein Symbol, indem sie den 
		gew&uuml;nschten Pfad als ersten Parameter, den qualifizierten (also den
		vollst&auml;ndigen) Namen des Anschlusses als zweiten Parameter und
		schlie&szlig;lich den Type als letzten Parameter &uml;bergeben.</p>
	</div>

	<div class="Head">Werte auslesen/schreiben</div>
	<div class="Text">
		<p>Nun endlich werde ich ihnen zeigen, wie sie an die nun verf&uuml;gbaren Werte gelangen. Der
		Aufruf ist so einfach wie logisch:
<pre>
import PPLT;
import sys;

psys = PPLT.System();

if not psys.LoadDevice("Debug.RandomGenerator","zufall",{}):
	print "Fehler beim laden...";
	sys.exit();

if not psys.CreateSymbol("/rand_zahl","zufall::Generator::DWord", "DWord"):
	print "Fehler beim Erzeugen eines Symbols";
	sys.exit();

print "Lese:"
print psys.GetValue("/rand_zahl");
</pre>
		Nun sollte eine Zufallszahl zwischen 0 und 100 ausgegeben werden. Im Fehler 
		Fall gibt die Method <i>GetValue()</i> <i>None</i>
		zur&uuml;ck.  Nun, als einziger Parameter wird dieser Mehtode der <u>volle</u> 
		Pfad zum Symbol &uuml;bergeben.</p>
		
		<p> Das Schreiben in so ein Symbol ist dem lesen sehr &auml;hnlich. Sehen sie 
		selbst:
<pre>
[...]
if not psys.SetValue("/rand_zahl",1):
	print "Fehler beim Schreiben...";
	sys.exit();
</pre>
		Wenn sie jedoch dies ausprobieren, werden sie feststellen, dass jedes mal 
		beim Schreiben ein Fehler ausgegeben wird. Dies hat die Bewandnis,
		dass aus dem Zufallsgenerator nur gelesen werden darf. Es ist nicht 
		m&ouml;glich den Zufall zu beeinflussen. Wie sie sehen, wird der Methode
		der Pfad des Symbols und der zu schreibene Wert &uuml;bergeben. Wenn alles
		gut geht, wird die Methoe <i>True</i> zur&uuml;ck geben. Im Fehlerfall wieder
		<i>False</i> was im Beispiel mit der <i>if</i> Anweisung &uuml;berpr&uuml;ft 
		wird.</p>
	</div>

	<div class="Head">Einen Server starten</div>
	<div class="Text"><p>Nun sind sie in der Lage ein oder mehrere Ger&auml;te 
		zuladen, einige Symbole zu erzeugen und diese zu lesen oder zu schreiben.
		Wenn sie diesen Erfolg mit anderen Menschen teilen m&ouml;chten oder
		diese sehr wichtigen Informationen durch andere Programme 
		weiterverarbeiten m&ouml;chten, m&uuml;ssen sie eine Schnittstelle
		schaffen, die diese Informationen anderen Programmen zur 
		Verf&uuml;gung stellt. Solche Schnittstelle sind in dem PPLT
		System schon vorbereitet und hei&szlig;en "Server". Intern
		haben die Server sehr viel &Auml;hnlichkeit mit den schon 
		verwendeten Ger&auml;ten. Sie bestehen mei&szlig;t auch aus ein
		oder mehreren Modulen. Sie werden wie die Ger&auml;te auch
		durch den Aufruf einer Mehtode geladen.</p>

		<p>Mit diesen Servern tangiere ich jetzt einen Bereich des Systems,
		den ich voher komplett au&szlig;er Acht gelassen habe: Das Rechte
		Management. Da sie, wenn sie einen Server laden, nicht 100%-ig
		sagen k&ouml;nnen wer auf diesen Zugriff hat, ist in das PPLT
		System ein Sicherheitsmechanismus eingebaut, der versucht
		unerw&uuml;nschte Zugriffe zu verhindern, damit sie die Kontrolle
		dar&uuml;ber behalten, wer welche Werte lie&szlig;t oder setzt.</p>

		<p>Befor ich mit der Theorie fortfahre, werde ich ihnen ein kutzes 
		Beispiel geben, wie so ein Server zu laden ist.
<pre>
[...]
if not psys.LoadServer("Web.PPLTWebServer",
                       "web",
                       "admin",
                       {"Address":"127.0.0.1","Port":"4711"}):
	print "Fehler beim Laden des Servers";
	sys.exit();

#Endlosschleife:
while True:
	pass;
</pre>
		In diesem Beispiel (und wie in den folgenden auch) wird der WebServer
		geladen. Dann k&ouml;nnen sie mittels Webbrowser den Symbolbaum 
		durchforsten. Dies ist nat&uuml;rlich sehr angenehm, da sie keinerlei
		Zusatzsoftware ben&ouml;tigen.</p>

		<p>Der erste und zweite Parameter d&uuml;rfte ihnen schon schon aus
		dem Abschnitt "Ger&auml;te laden" bekannt sein. Dies ist der Name des 
		Servers und das Alias welches dieser bestimme Server nach dem Laden 
		bekommt. Ebenso beinhalten die geschweiften Klammern die Parameter,
		die der Server zum Starten ben&ouml;tigt. In diesem Fall wird der 
		Parameter <i>Address</i> auf "127.0.0.1" gesetzt, was den Server
		dazu veranlasst nur auf dem sog. LoopBackDevice zu h&ouml;ren,
		also dass der Server nur von Programmen erreichbar ist, die auf
		dem selben System laufen. Der zweite Parameter <i>Port</i> gibt
		den Port an, auf dem der Server auf neue Verbindungen warten soll.
		In diesem Fall wartet der Server auf dem Port 4711. Um den
		Server zu erreichen, geben sie in ihren Browser in der 
		Adresszeile <i>http://127.0.0.1:4711</i> an. Dann sollte
		eine vom Server generierte Webseite erscheinen.</p>

		<p>Lediglich die Angabe <i>admin</i> in dritter Stelle ist neu. Hier
		wird ein Standartbenutzter fest gelegt. Um das verst&auml;ndlicher
		zu machen, will ich zuna&auml;chst eine kleinen Ausflug in den 
		Sicherheitsapparat des Systems machen.</p>
		
		<p>Jeder, der auf den Symbolbaum zu greifen will, muss sich ihm 
		gegen&uuml;ber authentifizieren. Das hei&szlig;t er muss dem 
		System mittels Benutzernamen und Password zeigen, das er derjenige
		ist, f&uuml;r den er sich aus gibt. Erst danach kann er auf den
		Symbolbaum zugreifen. Nun gibt es Server, die keine Authentifizierung
		kennen. F&uuml;r diese Server gibt man einen solchen Standardbenutzter
		an. Wenn also jemand eine Anfrage an einen solchen Server stellt,
		besitzt er die Rechte dieses Standart Benutzers. Der WebServer ist
		so ein Fall, zwar gibt es die M&ouml;glichkeit via HTTP eine
		Authentifizierung durchzuf&uuml;hren, dennoch habe ich bei diesem
		Server darauf verzichtet, da er nur zu Demonstrationszwecken gedacht
		ist. Der Server oben, wo jeder Benutzter, der darauf zu greift, mit
		Administratorenrechten arbeitet, ist normalerweise ein riesiges
		Sicherheitsloch. Da jeder, der den Server erreichen kann, sofort
		mit den Rechten des Administrators arbeitet. Ich habe dennoch
		mit Absicht dieses Beispiel gew&auml;hlt, da jedes Symbol, das
		neu erzeugt wird, dem Administrator geh&ouml;rt und nur dieser
		auf das Symbol zugreifen darf.</p>

		<p>Ich wollte damit verhindern, das sie sich mit der Rechteverwaltung
		des Systems von Anfang an auseinander setzen m&uuml;ssen. Sie m&uuml;ssen
		sich dennoch merken: <u>Der Standardbenutzer muss immer der unpreviligierteste
		Benutzer des Systems sein!</u></p>
		
		<p>Zum Abschluss will ich ihnen noch ein vollst&auml;ndiges Beispiel mit
		auf den Weg geben. Es stellt die Zusammesfassung der Beispiele im Text
		dar:
<pre>
import PPLT;
import sys;

psys = PPLT.System();

if not psys.LoadDevice("Debug.RandomGenerator","zufall",{}):
	print "Fehler beim laden des Generators";
	sys.exit();

if not psys.CreateSymbol("/rand_zahl","zufall::Generator::DWord","DWord"):
	print "Fehler beim erzeugen des Symbols"
	sys.exit();

if not psys.LoadServer("Web.PPLTWebServer",
                       "web",
                       "admin",
                       {"Address":"","Port":"4711"}):
	print "Fehler beim laden des Servers";
	sys.exit();

while True:		#Endlosschleife
	pass;
</pre>

		Eine Kleinigkeit, gege&uuml;ber dem oberen Beispiel zum Server ist, 
		dass ich statt der Adresse einen leeren String angegeben habe.
		Dies veranlasst den Server auf allen verf&uuml;gbaren 
		Netzwerkschnittstelle auf Verbindungen zu warten.</p>
	</div>

	<div class="Head">Erweitertes Beispiel</div>
	<div class="Text"><p>Bei diesem Beispiel werde ich den aktuellen Ladestand
		eines GSM konformen Handys (getestest mit einem Siemens S55/ME45) und
		gleichzeitig das erste Ausgangsbit einer NAiS FP0 oder FP2 via 
		PPLTWebServer exportieren. Dies soll die m&auml;chtigkeit des Systems
		veranschaulichen. Aus Gr&uuml;nden der Lesbarkeit habe ich alle
		Fehler&uuml;berpr&uuml;fungen weg gelassen.
<pre>
import PPLT;

psys = PPLT.System();

psys.LoadDevice("Mobile.GSMMobilePhone","handy",{"Port":"0","Speed":"9600"});
psys.LoadDevice("PLC.NAiS_FPX","nais",{"Port":"1","Address":"1"});

psys.CreateSymbol("/bat","handy::GSM::battery","DWord");
psys.CreateSymbol("/y0","nais::Marker::Y0","Bool");

psys.LoadServer("Web.PPLTWebServer","web","admin",{"Address":"","Port":"4711"});

#Endlosschleife:
while True:
	pass;		
</pre>
		Vielleicht sollte ich hier noch kurz die Parameter f&uuml;r die 
		Ger&auml;te	erkl&auml;ren. Das Handy brauch 2 Parameter, zun&auml;chst
		die serielle Schnittstelle an die es angeschlossen ist. In diesem
		Fall is es die Erste (Port:[0=COM1/1=COM2...]). Der zweite Parameter
		ist die Geschwindigkeit in Baud.<br>
		Die beiden Parameter f&uuml;r die NAiS Steuerung geben wieder die
		serielle Schnittstelle und die Adresse der Steuerung innerhalb
		des Buses an. Das verwendete Busprotokoll hei&azlig;t MEWTOCOL-COM
		und wird auch bei dem sog. ToolPort verwendet. Wenn sie die
		Seteuerung &uuml;ber den ToolPort ansprechen, ist die Adresse egal.</p>
	</div>		
</div>
