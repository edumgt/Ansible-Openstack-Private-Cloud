SHELL := /bin/bash

bootstrap:
	./scripts/bootstrap.sh

lint:
	ansible-lint

inventory-aws:
	ansible-inventory -i ansible/inventories/aws/aws_ec2.yml --graph

molecule:
	molecule test
