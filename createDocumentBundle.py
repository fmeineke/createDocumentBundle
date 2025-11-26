import csv
import os
import base64, hashlib
import re
import json
import mimetypes
import datetime

def file_mime_type(dateiname: str) -> str:
    """
    Gibt den MIME-Type basierend auf der Dateiendung zurück.

    :param dateiname: Dateiname mit Endung (z. B. 'bild.png')
    :return: MIME-Type als String (z. B. 'image/png'), oder 'application/octet-stream' wenn unbekannt
    """
    mime_type, _ = mimetypes.guess_type(dateiname)
    return mime_type or 'application/octet-stream'

def file_creation(dateiname: str) -> str:
    """
    Gibt das Erstellungsdatum einer Datei als ISO-String zurück.

    :param dateiname: Pfad zur Datei
    :return: Erstellungsdatum als String (z. B. '2025-10-29T17:54:00')
    """
    timestamp = os.path.getctime(dateiname)
    datum = datetime.datetime.fromtimestamp(timestamp)
    return datum.strftime('%Y-%m-%d')

def file_data_base64(dateipfad: str) -> str:
    """Liest eine Datei und gibt deren Inhalt als base64-codierten String zurück."""
    with open(dateipfad, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')
    
def file_size(dateipfad: str) -> int:
    return os.path.getsize(dateipfad)

def file_hash(filename, algorithm='sha256'):
    with open(filename, 'rb') as f:
        binary_data = f.read()

    hash_func = getattr(hashlib, algorithm)
    hash_bytes = hash_func(binary_data).digest()

    return base64.b64encode(hash_bytes).decode('utf-8')

def read_csv_dict(csv_pfad) -> list[dict]:
    with open(csv_pfad, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        list = []
        for row in reader:
            # Alle Werte trimmen
            getrimmt = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
            list.append(getrimmt)
        return list

def read_template(pfad: str) -> list[str]:
    """Liest die Template-Datei zeilenweise ein."""
    with open(pfad, 'r', encoding='utf-8') as f:
        return f.readlines()

# Initialize hashmap
kdl_display = {}
ihe_class_display = {}
ihe_type_display = {}
ihe_class_code = {}
ihe_type_code = {}

def ersetze_variablen(zeile: str, daten: dict) -> str:
    """Ersetzt alle Variablen im Format ${NAME} durch die entsprechenden Werte."""
    def ersatz(match):
        key = match.group(1)
        if key == 'FileTitle':
            return os.path.basename(daten['File'])
        elif key == 'FileURL':
            return daten['File']
        elif key == 'FileData':
            return file_data_base64(daten['File'])
        elif key == 'FileHash':
            return file_hash(daten['File'])
        elif key == 'FileSize':
            return str(file_size(daten['File']))
        elif key == 'FileMimeType':
           return file_mime_type(daten['File'])
        elif key == 'FileCreationDate':
           return file_creation(daten['File'])
        elif key == 'IHE_CategoryCode':
           return ihe_class_code[daten['KDL_Code']]
        elif key == 'IHE_TypeCode':
           return ihe_type_code[daten['KDL_Code']]
        elif key == 'IHE_CategoryDisplay':
           return ihe_class_display[daten['KDL_Code']]
        elif key == 'IHE_TypeDisplay':
           return ihe_type_display[daten['KDL_Code']]
        elif key == 'KDL_Dispay':
           return kdl_display[daten['KDL_Code']]
        else:
            return daten.get(key, 'UNKNOWN')
    return re.sub(r'\${(\w+)}', ersatz, zeile)

def init_kdl_ihe_type():
    # Load JSON file
    with open('conceptmap-kdl-ihe-typecode.xml.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Navigate to the elements in the first group
    elements = data.get("group", [])[0].get("element", [])

    # Build the hashmap
    for item in elements:
        code = item.get("code")
        display = item.get("display")
        if code and display:
            kdl_display[code] = display

        targets = item.get("target", [])    
        if code and targets:
            # Take the first target entry
            ihe_class_code[code] = targets[0].get("code", "")
            ihe_class_display[code] = targets[0].get("display", "")

def init_kdl_ihe_class():
    # Load JSON file
    with open('kdl-ihe-classcode.xml.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Navigate to the elements in the first group
    elements = data.get("group", [])[0].get("element", [])

    # Build the hashmap
    for item in elements:
        code = item.get("code")
        targets = item.get("target", [])    
        if code and targets:
            # Take the first target entry
            ihe_type_code[code] = targets[0].get("code", "")
            ihe_type_display[code] = targets[0].get("display", "")


def process_input_row(eintrag: dict, template_zeilen: list[str], f , index: int):
    """Verarbeitet eine einzelne Zeile aus der CSV und erzeugt eine Ausgabedatei."""
   
    neue_zeilen = []
    for zeile in template_zeilen:
        platzhalter = re.findall(r'\${(\w+)}', zeile)
        #if any(eintrag.get(p) == '' for p in platzhalter if p != 'DateiContent' and p != 'DateiName'):
        if any(eintrag.get(p) == '' for p in platzhalter):
            continue  # Zeile entfernen, wenn ein Wert fehlt
        try:
            neue_zeilen.append(ersetze_variablen(zeile, eintrag))
        except FileNotFoundError:
            print(f"Datei nicht gefunden: {eintrag['Datei']}")
            return
    f.write
    f.writelines(neue_zeilen)

bundle_header = """
{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [
"""

bundle_header_test = """
{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [
  {
      "fullUrl": "urn:uuid:P001",
      "resource": {
        "resourceType": "Patient",
        "id": "P001",
        "name": [{ "family": "Müller", "given": ["Anna"] }]
      },
      "request": { "method": "POST", "url": "Patient" }
    },
    {
      "fullUrl": "urn:uuid:E001",
      "resource": {
        "resourceType": "Encounter",
        "status": "finished",
        "class": {
          "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
          "code": "AMB",
          "display": "ambulatory"
        },
        "subject": {
          "reference": "urn:uuid:P001"
        },
        "period": {
          "start": "2025-11-01T09:00:00+01:00",
          "end": "2025-11-01T09:30:00+01:00"
        },
        "reasonCode": [
          {
            "coding": [
              {
                "system": "http://snomed.info/sct",
                "code": "65363002",
                "display": "Otitis media"
              }
            ]
          }
        ]
      },
      "request": {
        "method": "POST",
        "url": "Encounter"
      }
    },
"""
bundle_footer = """
   ]
}
"""


def main():
    csv_pfad = 'input/metadata.csv'
    template_deid_pfad = 'template-fhir-deid.json'
    template_semantic_pfad = 'template-fhir-semantic.json'
    init_kdl_ihe_type()
    init_kdl_ihe_class()

    daten = read_csv_dict(csv_pfad)
    template_deid = read_template(template_deid_pfad)
    template_semantic = read_template(template_semantic_pfad)

    with open("transaction-bundle.json",'w',encoding='utf-8') as f:
        f.write(bundle_header_test)
        for i, eintrag in enumerate(daten, start=1): 
            if eintrag['Template'] == 'deid':
                template = template_deid          
            elif eintrag['Template'] == 'semantic':
                template = template_semantic
            else:
                print(f"Unbekanntes Template: {eintrag['Template']} in Zeile {i}")
                continue
            process_input_row(eintrag, template, f, i)
            f.write(",\n" if i < len(daten) else "")
        f.write(bundle_footer)

if __name__ == '__main__':
    main()
