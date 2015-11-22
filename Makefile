ex:
	make bun
	make web
	make tag
	time ./export-stems.py
	time ./export-people.py

tag:
	time ./export-tags.py

bun:
	time ./export-bundles.py

web:
	time ./export-web.py

ppl:
	time ./refine-xmatch-people.py
	time ./refine-whowrote.py
	time ./refine-sortJson.py
	time ./export-people.py

norm:
	#time ./refine-sortJson.py
	time ./refine-normValues.py
	time ./refine-lowerVenue.py
	time ./refine-giveNames.py
	time ./refine-hyperlinks.py
	# time ./refine-retag.py

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
