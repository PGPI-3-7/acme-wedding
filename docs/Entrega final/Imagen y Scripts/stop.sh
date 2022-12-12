docker stop $(docker ps | grep acmewedding:v1.0 | cut -d' ' -f1)
