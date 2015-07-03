tag:
	time ./tag-export.py

bun:
	time ./bundle-export.py

web:
	time ./html-export.py

all:
	make bun
	make web
	make tag

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
