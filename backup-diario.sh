usuario=$(jq .usuario ${1})
password=$(jq .password ${1})
ip=$(jq .servidor ${1})
puerto=$(jq .puerto ${1})
authdb=$(jq .authdb ${1})
db=$(jq .db ${1})
colleccion=$(jq .colleccion ${1})
ayer=$(date -d "yesterday" +"%Y-%m-%d")

mongoexport --host=${ip} --port=27017 --authenticationDatabase admin -u ${usuario} -p ${password} --db=dlm --collection=noticias --query='{"fecha":{"$gte":{"$date":"'${ayer}'T00:00:00.000Z"}, "$lte":{"$date":"'${ayer}'T23:59:59.000Z"}}}' --out noticias_${ayer}.json
