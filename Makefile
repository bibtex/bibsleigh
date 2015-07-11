ex:
	make bun
	make web
	make tag
	make ppl

tag:
	time ./export-tags.py

bun:
	time ./export-bundles.py

web:
	time ./export-web.py

ppl:
	time ./refine-people.py
	time ./refine-whowrote.py
	time ./export-people.py

norm:
	time ./refine-sortJson.py
	time ./refine-normValues.py
	time ./refine-lowerVenue.py
	time ./refine-giveNames.py
	time ./refine-hyperlinks.py
	time ./refine-retag.py

run:
	time ./library.py
	sort venues.lst | uniq > venues.unq
	./newvenues.py
	rm -f venues.unq

prep: dblp.xml
	./deentitify dblp.xml

clean:
	rm -rf __pychache__
	find .. -name ".DS_Store" | xargs rm
