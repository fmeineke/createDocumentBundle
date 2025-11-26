.PHONY: get post clean distclean

document-bundle.json: conceptmap-kdl-ihe-typecode.xml.json kdl-ihe-classcode.xml.json 
	python3	createDocumentBundle.py

kdl-ihe-classcode.xml.json:
	curl 'https://simplifier.net/ui/packagefile/downloadas?packageName=dvmd.kdl.r4&version=2025.0.0&packageFileId=2744690&format=json' -o $@

conceptmap-kdl-ihe-typecode.xml.json:
	curl 'https://simplifier.net/ui/packagefile/downloadas?packageName=dvmd.kdl.r4&version=2025.0.0&packageFileId=2744691&format=json' -o $@

get: 
	curl 'http://localhost:8080/fhir/Patient/1/$$everything'

post: transaction-bundle.json
	curl -X POST -H "Content-Type: application/fhir+json" -d @$< http://localhost:8080/fhir

clean:
	rm -f document-bundle.json

distclean: clean
	rm -f conceptmap-kdl-ihe-typecode.xml.json kdl-ihe-classcode.xml.json

