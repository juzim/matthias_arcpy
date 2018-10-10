
# -*-coding: UTF-8-*-

"""
     Autor:         Matthias Herbein
     Erstellt:      04.10.2018
     Ueberarbeitet: heute
     Py Version:     3.6
     Beschreibung: Der Nutzer kann einer Feature Class oder einem Layer mit Hilfe dieses Tools neue Felder in der
     Attributtabelle hinzufuegen. Der Nutzer kann dabei mehrere Felder des gleichen Datentyps gleichzeitig anlegen.
     Die Feldnamen werden in diesem Prozess in Abhängigkeit vom Eingabedatensatz automatisch validiert.
     Ist der Datentyp des neuen Feldes "TEXT" kann die Laenge der Felder definiert werden.
     Der default Wert fuer Felder des Typs "Text" ist "no data".
"""

# Import system modules
import arcpy
import sys

# Umgebungseinstellungen
# parallele Verarbeitung


# Variablen
# Eingabedatei (Feature Class oder Layer) festlegen
eingabeFC = arcpy.GetParameterAsText(0)

"""
Workspace muss in Abhängigkeit von eingabeFC abgefragt werden.
Wobei darauf vieleicht auch verzichtet werden kann/sollte.
Nach Aufgabenbeschreibung (Hinweis 3) sollte ich mich aber auf den Eingabe WS beziehen
Aufgabe: Funktion ValidateFieldName nochmal genau anschauen.

"""

eingabeBeschreibung = arcpy.Describe(eingabeFC)
arbeitsverzeichnis = eingabeBeschreibung.path
# arcpy.env.workspace = arbeitsverzeichnis
# kann/muss ich hier noch Fehler wie \neuer Ordner mit dem raw Befehl abfangen??

# Liste der Feldnamen erfassen
eingabeString = arcpy.GetParameterAsText(1)
feldListe = eingabeString.split(";")
feldTyp = arcpy.GetParameterAsText(2)
feldLaenge = arcpy.GetParameterAsText(3)
"""
# f str(z).isdigit() == True:
    print "Z ", z
     # gibt nichts aus weil `z` keine Int ist und kein String der nur Zahlen enthält
"""
"""
# der Datentyp und der Wertebereich des Parameters Feldlaenge werden geprueft.
if arcpy.Exists(feldLaenge):

if arcpy.GetParameterAsText(3) == int or ():
    print('Die Verarbeitung wird gestartet.')
elif arcpy.GetParameterAsText(3) < 254:
    print('Einen kleinen Moment bitte.')
else:
    sys.exit(arcpy.AddMessage('Eine Feldlaenge kann nur für den Datentyp -TEXT- angegeben werden. \n'
                              'Der Wert muss eine ganze Zahl zwischen 1 und 254 sein.\n'
                              ' Der Prozess wurde abgebrochen'))
"""
# Start der Schleife
zaehler = 0
while zaehler < len(feldListe):
    feldName = feldListe[zaehler]
    # Der Feldname wird validiert
    validerName = arcpy.ValidateFieldName(feldListe[zaehler], arbeitsverzeichnis)
    if validerName != feldName:
        arcpy.AddMessage('Der Feldname ' + feldName + ' ist ungueltig. Das Feld wurde in ' + validerName + ' umbenannt')
    else:
        arcpy.AddMessage('Der Feldname ' + feldName + ' ist valide.')
    # Es wird geprüft ob das Feld bereits existiert
    if len(arcpy.ListFields(eingabeFC, feldListe[zaehler])) > 0:
        sys.exit(arcpy.AddMessage('Der Feldname ' + feldName + ' existiert bereits. '
                                                               'Die Verarbeitung wurde abgebrochen'))
    if len(arcpy.ListFields(eingabeFC, validerName)) > 0:
        sys.exit(arcpy.AddMessage('Der Feldname ' + validerName + ' existiert bereits. '
                                                                  'Die Verarbeitung wurde abgebrochen'))

    # Start Prozess, zunaechst fuer valide Namen
    if feldName == validerName:
        for feldName in feldListe:
            # Fuer den Feldtyp TEXT wird auch der Parameter Feldlaenge mit verarbeitet.
            if feldTyp == 'TEXT':
                feldLaenge = int(arcpy.GetParameterAsText(3))
                arcpy.AddField_management(eingabeFC, feldName, feldTyp, {}, {}, {feldLaenge})
                # Fuer Felder des Typs TEXT soll als default Wert statt 'NULL' der Wert 'no data' eingetragen werden
                """# muss bei UpdateCursor die FC oder der Pfad zur FC angegeben werden? Was liefert das erste 
                arcpy.GetParameterAsText(0) zurück?"""
                zeilenFC = arcpy.da.UpdateCursor(eingabeFC, feldName)
                for row in zeilenFC:
                    row[:] = 'no data'
            else:
                arcpy.AddField_management(eingabeFC, feldName, feldTyp)
        arcpy.AddMessage('Das Feld ' + feldName + ' wurde erstellt.')
    # Start Prozess fuer geanderte Namen
    else:
        for validerName in feldListe:
            if feldTyp == 'TEXT':
                arcpy.AddField_management(eingabeFC, validerName, feldTyp, {}, {}, {feldLaenge})
                # Fuer Felder des Typs TEXT soll als default Wert statt 'NULL' der Wert 'no data' eingetragen werden
                zeilenFC = arcpy.da.UpdateCursor(eingabeFC, validerName)
                for row in zeilenFC:
                    row[:] = 'no data'
            else:
                arcpy.AddField_management(eingabeFC, validerName, feldTyp)
        arcpy.AddMessage('Das Feld ' + validerName + ' wurde erstellt.')
    zaehler = zaehler + 1

arcpy.AddMessage('Herzlichen Glueckwunsch! Die Verarbeitung wurde erfolgreich abgeschlossen!')
A4_ScriptTool.py
Displaying A4_ScriptTool.py.
