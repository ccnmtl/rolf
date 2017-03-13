APP=rolf
JS_FILES=media/js/main.js media/js/models/ media/js/collections/ media/js/views/ media/js/utils/

all: jenkins

include *.mk

eslint: $(JS_SENTINAL)
	$(NODE_MODULES)/.bin/eslint $(JS_FILES)

.PHONY: eslint
