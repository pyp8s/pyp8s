VERSION := $(shell cat version.py | cut -d "=" -f 2 | tr -d "'")
PWD := $(shell pwd)
BUILD_DIR = $(PWD)/dist
PROG := pyp8s-$(VERSION)-py3-none-any.whl
PROG_EGG := pyp8s-$(VERSION)-py3.10.egg

.PHONY: all version build clean install

build: $(BUILD_DIR) $(BUILD_DIR)/$(PROG) $(BUILD_DIR)/$(PROG_EGG)
	@echo "Last steps"

$(BUILD_DIR)/$(PROG):
	@echo target is $@
	python3 setup.py sdist bdist_wheel

$(BUILD_DIR)/$(PROG_EGG):
	@echo target is $@
	python3 setup.py sdist bdist_egg

install:
	python3 -m pip install --upgrade --user "$(BUILD_DIR)/$(PROG)"

test:
	PYTHONPATH="$(BUILD_DIR)/$(PROG_EGG)" python3 -m pytest

version:
	@echo "Version: $(VERSION)"

clean:
	[ -f "$(BUILD_DIR)/$(PROG)" ] && rm -vf "$(BUILD_DIR)/$(PROG)" || :

$(BUILD_DIR):
	mkdir -p "$(BUILD_DIR)"
