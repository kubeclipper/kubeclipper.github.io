.PHONY: server
server:
	hugo server

.PHONY: public
public:
	hugo --baseUrl="https://kubeclipper.io"

.PHONY: push-public
push-public:
	git subtree push --prefix=public origin master
