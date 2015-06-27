all: AST.py Templates.py JSON.py Fancy.py

AST.py:
	cp ../engine/AST.py .

JSON.py:
	cp ../engine/JSON.py .

Fancy.py:
	cp ../engine/Fancy.py .

Templates.py:
	cp ../engine/Templates.py .

clean:
	rm -f AST.py Templates.py JSON.py Fancy.py
