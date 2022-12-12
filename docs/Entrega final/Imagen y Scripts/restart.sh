docker start $(docker ps -a | grep acmewedding:v1.0 | cut -d' ' -f1)
