# Makefile for alip.github.com

JEKYLL:= jekyll
GIT:= git
FORTUNE:= fortune

JEKYLL_FLAGS= --trace
FORTUNE_COUNT= 5
FORTUNE_FLAGS= -l -e
FORTUNE_LIST= art computers linux linuxcookie love magic paradoxum perl science
FORTUNE_FILE= _includes/cookie.html
GIT_HEAD= $(shell $(GIT) rev-parse HEAD)
GIT_HEAD_SHORT= $(shell $(GIT) rev-parse --short HEAD)

# Used by _scripts
export FORTUNE
export FORTUNE_COUNT
export FORTUNE_FLAGS
export FORTUNE_LIST
export FORTUNE_FILE
export GIT_HEAD
export GIT_HEAD_SHORT

all: jekyll

.PHONY: uuid
uuid:
	@for post in $(wildcard _posts/*.markdown); do \
		echo "UUID $$post" >&2 && \
		_scripts/add-uuid.py < "$$post" > "$$post~" && \
		mv "$$post~" "$$post" ;done

cookie:
	@_scripts/fortune.rb
	$(GIT) add --update

data:
	@_scripts/taglist.rb
	@_scripts/tagcloud.rb
	$(GIT) add --update

jekyll: data
	$(JEKYLL) build $(JEKYLL_FLAGS)

jekyll-check: data
	$(JEKYLL) serve $(JEKYLL_FLAGS) -H localhost -P 4000

jekyll-check-auto: data
	$(JEKYLL) serve $(JEKYLL_FLAGS) -H localhost -P 4000 -w

tidy: jekyll
	@_scripts/tidy.bash _site

clean:
	rm -f tidy.log
	rm -fr _site

.PHONY: clean cookie data jekyll jekyll-check tidy
