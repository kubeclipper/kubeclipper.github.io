.PHONY: setup

module-check:
	@git submodule status --recursive | awk '/^[+-]/ {printf "\033[31mWARNING\033[0m Submodule not initialized: \033[34m%s\033[0m\n",$$2}' 1>&2

setup:
	bash -x ./scripts/setup.sh

setup-upstream:
	bash -x ./scripts/setup-upstream.sh

server: setup
	./scripts/build.py --host=http://localhost:1313
	cd public && python3 -m http.server 1313

build:
	./scripts/build.py \
		--host=https://kubeclipper.io \
		--edition=ce \
		--multi-versions
