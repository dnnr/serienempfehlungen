ifndef TXT
$(error Set TXT= to the input text file)
endif

.PHONY: all
all: publish

.PHONY: generate
generate:
	./convert.py $(TXT) index.html

.PHONY: publish
publish: generate
	rsync -av --delete --chmod=a+rX index.html bootstrap* /var/www/serienempfehlung.de/
