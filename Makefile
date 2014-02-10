all:

run:
	time ./library.py
	sort venues.lst | uniq > venues.unq
	./newvenues.py
	rm -f venues.unq

clean:
	rm -rf html
	mkdir html
