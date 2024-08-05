# Makefile

install:
    poetry install

fetch_rss:
    poetry run python fetch_rss.py --config config.toml --output-json rss_data.json

post_run:
	cat rss_data.json

commit:
    git config --global user.email 'action@github.com'
    git config --global user.name 'Github Action'
    git add rss_data.json
    git commit -m 'Update RSS data'
    git push

ci: install fetch_rss post_run
