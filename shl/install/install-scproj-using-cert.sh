# 1. deploy svc/pod
# 2. deploy ingress gateway
# 3. deploy virtual service, destination rule
# 4. deploy peer authentication
# 5. make key
# 6. make certification(secret)

deploy=/home/hh/git/istio-project/shl/deploy

sh $deploy/deploy-svc.sh
sh $deploy/deploy-ingress.sh
sh $deploy/deploy-vsdr.sh
sh $deploy/deploy-peer-auth.sh
sh $deploy/make-key.sh
sh $deploy/deploy-secret.sh

kubectl get svc -n istio
kubectl get pods -n istio
kubectl get secret -n istio-system
kubectl get peerauthentication -n istio
kubectl get requestauthentication -n istio
