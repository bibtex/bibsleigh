all:

run:
	time ./library.py
	sort venues.lst | uniq > venues.unq
	./newvenues.py
	rm -f venues.unq

clean:
	cd html && (ls -1 | grep '.html' | xargs -n1 rm)