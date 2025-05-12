.PHONY: help install-dev install-prod clean build deploy

## Show help
help:
	@echo "Usage:"
	@echo "  make install-dev    Install dev dependencies (includes boto3, pytest)"
	@echo "  make install-prod   Install only prod dependencies (no boto3)"
	@echo "  make clean          Clean up build artifacts"
	@echo "  make build          Build Lambda zip package for Terraform"
	@echo "  make deploy         Run Terraform apply"

## Install dev dependencies
install-dev:
	pip install -r requirements.dev.txt

## Install only prod dependencies
install-prod:
	pip install -r requirements.txt

## Clean build artifacts
clean:
	rm -rf packages function.zip

## Build Lambda zip package (for Terraform to pick up)
build: clean
	mkdir -p packages
	pip install -r requirements.txt -t packages
	cd packages && zip -r ../function.zip .
	cd src && zip -r ../function.zip .
	openssl dgst -sha256 -binary function.zip | openssl base64 > function.zip.base64sha256

## Run Terraform
deploy: build
	cd terraform && terraform apply -var="lambda_zip_hash=$$(cat ../function.zip.base64sha256)"
