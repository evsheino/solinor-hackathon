# solinor-hackathon

## Importing world city data
1. Download data from https://www.maxmind.com/en/free-world-cities-database and extract it
2. Convert it to UTF-8 (`iconv -f ISO-8859-15 -t UTF-8 -o /tmp/cities.txt /tmp/worldcitiespop.txt`)
3. Filter illegal characters (`sed 's/"//' cities.txt > cities-fixed.txt`)
4. Import it to database (for PostgreSQL use `\copy crawler_location (country,city,city_accent,region,population,latitude,longitude) FROM '/tmp/cities-fixed.txt' DELIMITER ',' CSV HEADER;`)
