# 📄 createDocumentBundle

Eine Demonstration, wie aus bestehenden Dokumenten **KDL Module Document** valide **FHIR DocumentReferences** erzeugt werden können.

---

## 📂 Projektübersicht
- Alle Eingabedokumente liegen im Ordner `input`.
- Die Datei **`metadata.csv`** enthält notwendige Metadaten:

| Feld        | Beschreibung                                                                 |
|-------------|-------------------------------------------------------------------------------|
| **DocID**   | Lokale Dokumentennummer                                                       |
| **PatientID** | Patienten-ID (im Beispiel fix `P001`)                                       |
| **FallID**  | Optionale Fall-ID (im Beispiel fix `E001`)                                    |
| **KDL_Code**| KDL Type Code des Dokuments                                                   |
| **File**    | Dateiname des Dokuments                                                       |
| **DocRefID**| Optionale lokale Dokumentennummer, auf die mit `relatedTo` verwiesen werden kann |
| **Template**| Bestimmt das JSON-Template für die DocumentReference (`deid` oder `semantic`) |

---

## ⚙️ Nutzung mit Makefile
Die Demo wird über ein **Makefile** gesteuert:

- `make`  
  → erzeugt über **Python3** eine Datei `documentBundle.json`.  
  → notwendige KDL → IHE Type & IHE Class Mapping-Dateien werden automatisch geladen.

- `template-fhir-semantic.json`  
  → Template für semantische Annotation (`semantic`).

- `template-fhir-deid.json`  
  → Template für de-identifizierte Texte (`deid`).

- `make post`  
  → importiert das erzeugte Bundle per **POST** in einen FHIR-Server (HAPI unter `http://localhost:8080/fhir`).

- `make post-init`  
  → importiert per **PUT** (create/update) einen Patienten `P001` und ein Demo Encounter `E001`.

- `make get`  
  → lädt zur Kontrolle per `$everything` alle Ressourcen des Patienten `P001` herunter.

---

## 🧪 Getestete Umgebung
- Aktueller **HAPI FHIR Server**

---

## 📋 Voraussetzungen
- **Python 3**
- **curl**

---

## 🚀 Quickstart
```bash
# Bundle erzeugen
make

# Patient & Encounter anlegen
make post-init

# Bundle in FHIR-Server importieren
make post

# Ressourcen des Patienten abrufen
make get
