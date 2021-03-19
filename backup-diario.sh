usuario=$(jq .usuario ${1})
password=$(jq .password ${1})
ip=$(jq .servidor ${1})
puerto=$(jq .puerto ${1})
authdb=$(jq .authdb ${1})
db_noticias=$(jq .noticias.db ${1})
coleccion_noticias=$(jq .noticias.coleccion ${1})
db_frecuencias=$(jq .frecuencias.db ${1})
coleccion_frecuencias=$(jq .frecuencias.coleccion ${1})
ayer=$(date -d "yesterday" +"%Y-%m-%d")

# mongoexport --host=${ip} --port=27017 --authenticationDatabase ${authdb} -u ${usuario} -p ${password} --db=${db_noticias} --collection=${coleccion_noticias} --query='{"fecha":{"$gte":{"$date":"'${ayer}'T00:00:00.000Z"}, "$lte":{"$date":"'${ayer}'T23:59:59.000Z"}}}' --out ${2}noticias/${ayer}.json

ayer_sin_guion=$(date -d "yesterday" +"%Y%m%d")

mongoexport --host=${ip} --port=27017 --authenticationDatabase ${authdb} -u ${usuario} -p ${password} --db=${db_frecuencias} --collection=${frecuencias} --query='{"fecha":{"$gte":"'${ayer_sin_guion}'", "$lte":"'${ayer_sin_guion}'"}}' --out ${2}frecuencias/${ayer}.json
