
.venv/bin/activate: requirements.txt
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt

.PHONY: venv
venv: .venv/bin/activate

build: .venv/bin/activate
	mkdir -p build
	./.venv/bin/python3 -m pip install -r requirements.txt --target build
	cp -r src/* build

dist: build
	mkdir -p dist
	python3 -m zipapp build -p "/usr/bin/env python" -o dist/Steam-Search.pyz

/home/garulf/.config/rofi/scripts/Steam-Search.pyz: dist
	mkdir -p ~/.config/rofi/scripts
	cp dist/Steam-Search.pyz ~/.config/rofi/scripts


.PHONY: install
install: /home/garulf/.config/rofi/scripts/Steam-Search.pyz

run: install
	rofi -modi "Steam-Search" -show "Steam-Search"

.PHONY: uninstall
uninstall:
	rm -f ~/.config/rofi/scripts/Steam-Search.pyz

.PHONY: clean
clean: uninstall
	rm -rf dist
	rm -rf build
	rm -rf .venv


