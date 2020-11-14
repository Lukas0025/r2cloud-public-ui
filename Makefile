build:
	docker build . -t lukasplevac/r2cloud-public-ui:latest

push: build
	docker login
	docker push lukasplevac/r2cloud-public-ui:latest
