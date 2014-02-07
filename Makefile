all:

clean:
	cd html && (ls -1 | grep '.html' | xargs -n1 rm)