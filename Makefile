all:
	time ./json2html.py

run:
	time ./library.py
	sort venues.lst | uniq > venues.unq
	./newvenues.py
	rm -f venues.unq

prep: dblp.xml
	./deentitify dblp.xml

clean:
	rm -rf html
	mkdir html
