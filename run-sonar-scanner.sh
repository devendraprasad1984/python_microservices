/Users/dpadmin/deven/software/sonar-scanner-4.6.2.2472-macosx/bin/sonar-scanner \
  -Dsonar.projectKey=python_microservices_flask \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=1363c35d0b9e0d308f1c3f7ac064e305727a3227


#docker run --rm -e SONAR_HOST_URL="http://localhost:9000" -e SONAR_LOGIN="188056923c014fdd7d007406af88dd4c5813c18c" -v "/app:/app" sonarsource/sonar-scanner-cli


