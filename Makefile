NAME = steam-search


.venv/bin/activate: requirements.txt
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt
	./.venv/bin/pip install -r requirements-dev.txt

.PHONY: venv
venv: .venv/bin/activate

build: .venv/bin/activate
	mkdir -p build
	./.venv/bin/python3 -m pip install -r requirements.txt --target build
	cp -r src/* build

dist: build
	mkdir -p dist
	python3 -m zipapp build -p "/usr/bin/env python" -o dist/$(NAME).pyz

/home/garulf/.config/rofi/scripts/$(NAME).pyz: dist
	mkdir -p ~/.config/rofi/scripts
	cp dist/$(NAME).pyz ~/.config/rofi/scripts


.PHONY: install
install: /home/garulf/.config/rofi/scripts/$(NAME).pyz

run: install
	rofi -modi "$(NAME)" -show "$(NAME)"

.PHONY: uninstall
uninstall:
	rm -f ~/.config/rofi/scripts/$(NAME).pyz

.PHONY: clean
clean: uninstall
	rm -rf dist
	rm -rf build
	rm -rf .venv


