testserver: .env
	.env/bin/python manage.py testserver

.env/.up-to-date: base_requirements.txt flask_app/pip_requirements.txt
	virtualenv .env
	.env/bin/pip install -r base_requirements.txt
	.env/bin/pip install -r flask_app/pip_requirements.txt
	touch .env/.up-to-date

deploy: src_pkg.tar
	ansible-playbook -i ansible/inventories/production ansible/site.yml

deploy_staging: src_pkg.tar
	ansible-playbook -i ansible/inventories/staging ansible/site.yml


deploy_localhost: src_pkg.tar
	ansible-playbook -i 127.0.0.1, --sudo -c local ansible/site.yml

deploy_vagrant: vagrant_up
	ansible-playbook -i ansible/inventories/vagrant ansible/site.yml

vagrant_up:
	vagrant up
.PHONY: vagrant_up

src_pkg.tar:
	python scripts/build_tar.py

.PHONY: src_pkg.tar

travis_install:
	sudo apt-get update
	sudo apt-get install -y build-essential python-dev libevent-dev
	pip install --use-mirrors -r base_requirements.txt
	make deploy_localhost

travis_test: .env/.up-to-date
	.env/bin/pip install nose
	.env/bin/nosetests -w tests --tc www_port:80
