all:
	./done2csv.py *.txt scraped-by-grammarware.csv
	grep 'Univ' scraped-by-grammarware.csv

sense:
	@echo 'All makes sense'
	ls -1 *.txt | xargs -n1 ./makesense.py

