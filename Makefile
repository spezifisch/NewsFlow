# Makefile

install:
	poetry install

fetch_rss:
	poetry run python fetch_rss.py

commit:
	git config --global user.email 'action@github.com'
	git config --global user.name 'Github Action'
	git add rss_data.json
	git commit -m 'Update RSS data'
	git push

update: install fetch_rss commit
