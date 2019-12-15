# Real Estate Scrapper

If you don't have 'pt_BR' locale installed, follow the steps:

Uncomment the line with 'pt_BR' in /etc/locale.gen
Run `sudo locale-gen && dpkg-reconfigure locales`

Now 'pt_BR' is also a valid locale.

## Run

To run the properties spider, execute:

```bash
scrapy runspider ./olx/spiders/properties/sell.py -a state=<lowercase_state_initials>
```
