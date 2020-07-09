# k8s setup

gcloud container clusters get-credentials cluster-1 --zone us-central1-a --project entroprise-production

kubectl create secret generic cloudsql-instance-credentials --from-file=credentials.json=credentials.json

kubectl create secret generic cloudsql-db-credentials --from-literal=username=postgres --from-literal=password=$POSTGRE_USER_PASSWORD

wget https://raw.githubusercontent.com/hasura/graphql-engine/stable/install-manifests/google-cloud-k8s-sql/deployment.yaml

entroprise-production:us-central1:entroprise-db

kubectl apply -f deployment.yaml

kubectl get pods

kubectl logs deployment/hasura -c graphql-engine

# expose to the internet

kubectl expose deploy/hasura --port 80 --target-port 8080 --type LoadBalancer

kubectl get service

kubectl logs deployment/hasura -c graphql-engine

kubectl logs deployment/hasura -c cloudsql-proxy

# https load balancer and ingress

gcloud compute addresses create entroprise-hasura --global

gcloud compute addresses describe entroprise-hasura --global

kubectl apply -f hasura-cert.yaml

kubectl apply -f hasura.yaml

kubectl apply -f hasura-ingress.yaml

kubectl get ingress

kubectl describe managedcertificate hasura-cert
