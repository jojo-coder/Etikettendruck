# Motivation

In der Zeitschrift c't 9/2024 wird das Dokumentenmanagementsystem paperless-ngx vorgestellt. Dieses wurde auf einem Linuxserver installiert und wird nun zur Archivierung von Schriftstücken aller Art genutzt.

Um Originaldokumente aufzubewahren, wird empfohlen, auf diesen einen Barcode mit einer eindeutigen Nummer (ASN, archive serial number) aufzukleben. Die Schriftstücke können dann in einer Ablage gestapelt werden. Der Barcode wird von paperless-ngx ausgelesen und den Metadaten des eingescannten Schriftstückes hinzugefügt. So kann man später ohne großen Aufwand das Original anhand der ASN in der Ablage wieder finden.

Im c't Artikel wurde auch eine Webseite (https://tobiasmaier.info/asn-qr-code-label-generator/) erwähnt. Mit Hilfe dieser Seite kann man eine PDF-Datei mit Barcodes (und Klarschrift) mit fortlaufender Nummer erzeugen. Obwohl ich die im Artikel und auf der Webseite erwähnte Etikettensorte (Avery L4731) und den Chromebrowser verwendet habe, konnte ich keine Einstellung im Druckerdialog finden, so dass der Code und die Klarschrift sauber auf die Etiketten gedruckt wurden.

Daher: Erstellung eines kleinen Pythonskriptes, das einem mehr Einstellparameter zur Verfügung stellt.

# Vorbereitung
Zur Erzeugung der qr-Codes wird das Modul `qrcode` verwendet. Die Erstellung einer druckfähigen PDF-Datei gelingt am Einfachsten mit dem Modul `reportlab`. Eine sehr gute Dokumentation des Moduls findet man unter: https://www.reportlab.com/docs/reportlab-userguide.pdf

Erstellung einer virtuellen Umgebung und Installation der benötigten Module `qrcode` und `reportlab`:

```
python -m venv Eti_venv
source Eti_venv/bin/activate
pip install qrcode, reportlab
```
# Ausführung
Das Skript kann über eine Python IDE oder direkt als Aufruf via `python Etiketten.py` ausgeführt werden.

Wichtig: Vor dem Start des Skriptes Anpassung der Startvariablen für die ASN und Entscheidung, ob man einen Rahmen um jedes Etikett haben möchte oder nicht.

Die erzeugte PDF-Datei kann dann über einen PDF-Viewer oder direkt auf einen Drucker geschickt werden. Vor dem richtigen Druck auf das Etikettenpapier sollte man einen Probedruck auf Normalpapier machen. Dann u.U. die Druckparameter oder die Programmparameter im Skript gegebenfalls anpassen.

Eine PDF-Datei ist diesem Repository beigefügt. Sie wurde unter MacOS mit `Vorschau` auf einem Kyocera-Drucker bei einer Vergrößerung von 104% ausgegeben. Die Codes passten genau auf die 189 Etiketten.

# Anmerkungen
* Ich habe die erste ASN bei 10000 beginnen lassen. Dies ist m.E. optisch besser und bereitet keine Probleme bei etwaigen Sortierungen.
* Das Modul `reportlab` setzt den Ursprung (0,0) des Canvas auf einer Seite auf unten links. Daher beginnen die Etiketten auch von unten links an zu zählen. Ist kein Problem, da man die Etiketten sowieso einzeln abzieht. Wen das stört: Entwickle einen Algorithmus, der die ASNs von oben links aus ansteigen lässt (Hausaufgabe... ;). 
