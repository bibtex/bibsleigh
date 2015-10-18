python3_path := $(shell which python3)


ex:
	make bun
	make web
	make tag
	time $(python3_path) ./export-people.py

tag:
	time $(python3_path) ./export-tags.py

bun:
	time $(python3_path)  ./export-bundles.py

web:
	time $(python3_path)  ./export-web.py

ppl:
	time $(python3_path)  ./refine-xmatch-people.py
	time $(python3_path)  ./refine-whowrote.py
	time $(python3_path)  ./refine-sortJson.py
	time $(python3_path)  ./export-people.py

norm:
	time $(python3_path)  ./refine-sortJson.py
	time $(python3_path)  ./refine-normValues.py
	time $(python3_path)  ./refine-lowerVenue.py
	time $(python3_path)  ./refine-giveNames.py
	time $(python3_path)  ./refine-hyperlinks.py
	time $(python3_path)  ./refine-retag.py

run:
	time $(python3_path)  ./library.py
	sort venues.lst | uniq > venues.unq
	./newvenues.py
	rm -f venues.unq

prep: dblp.xml
	./deentitify dblp.xml

clean:
	rm -rf __pychache__
	find .. -name ".DS_Store" | xargs rm
