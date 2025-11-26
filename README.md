# createDocumentBundle

Eine mögliche Demonstration, wie aus bestehenden Dokumenten KDL Module Document valide DocumentReferences erzeugt werden können.

Alle Dokumente liegen in input. 
Die Datei "metadata.csv" enthält notwendige Metadaten (DocID;PatientID;FallID;KDL_Code;File;DocRefID;Template), wobei
* DocId die lokale Dokumentennummer
* PatID die Patienten-ID
* FallID (optional) die Fall-ID
* KDL_Code der KDL Type Code des Dokuments
* DocRefId (optional) eine lokale Dokumentennummer, auf die mit relatedTo verwiesen werden kann
* Template entschiedet welches json DocumentReference template zu verwenden ist; derzeit sind nur die Werte "deid" oder "semantic" erlaubt

Die Demo wird über ein makefile gesteuert:
* ein reines `make`sollte über python3 eine Datei `documentBundle.json` erzeugen. Die notwendigen KDL nach IHE type und IHE class Mapping-Dateien werden automatisch geladen.
* `template-fhir-semantic.json`  ist das template für semantische Annotation (semantic)
* `template-fhir-deid.json`  ist das template für de-identifizierte Texte (deid)
* `make post` importiert das erzeugte Bundle in eine fhir server (Hier: hapi unter http://localhost:8080/fhir)
* `make get` lädt, zur Kontrolle, per $everything alle Resourcen des Patienten "1" herunter.




  
