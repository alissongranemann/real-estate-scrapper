# Real Estate Scrapper

If you don't have 'pt_BR' locale installed, follow the steps:

Uncomment the line with 'pt_BR' in /etc/locale.gen
Run `sudo locale-gen && dpkg-reconfigure locales`

Now 'pt_BR' is also a valid locale.

## Local environment

First of all, you need to install poetry. To do that, run

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

To get started you need Poetry's bin directory (\$HOME/.poetry/bin) in your `PATH`
environment variable. Next time you log in this will be done
automatically.

To configure your current shell run `source $HOME/.poetry/env`

This project uses `black` as the code formatter and `flake8` as the linter.
To add git-hooks on your enviroment, so you can run `black` and `flake8` on your project for every commit, please execute `pre-commit install`.

Also, you need to configurate the enviroment variables accordingly. Create `env` file in the project's root folder and set the variables following the `.env.example`.

## Development

In order to have the poetry packages in a local virtual environment (in the project root directory), run:

```bash
poetry install
```

To test xpaths while building the scrapper (or changing one), you can use the http://xpather.com/.

The purpose of `runner.py` file is for debug. You can run it on your IDE as a normal python file.

## Run

To run the properties spider, execute:

```bash
scrapy runspider ./olx/spiders/properties/sell.py -a state=<lowercase_state_initials>
```
