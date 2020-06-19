# SPELL-APP

### Prerequisites
docker
docker-compose

### install
git clone https://github.com/masakicktashiro/spell_app.git

## Deployment
change the mysql password
22nd line of spell_app/docker-compose.yml
```
MYSQL_ROOT_PASSWORD: yourpassword
```
30th line of spell_app/for_dev/application/app.py
```
password='yourpassword',
```
Then
```
cd spell_app
docker-compose up -d
```
