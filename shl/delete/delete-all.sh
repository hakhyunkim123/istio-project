kubectl delete svc -n istio spring-main
kubectl delete svc -n istio spring-login
kubectl delete svc -n istio spring-todo
kubectl delete svc -n istio spring-proj
kubectl delete svc -n istio spring-chat

kubectl delete deployment -n istio spring-main
kubectl delete deployment -n istio spring-login
kubectl delete deployment -n istio spring-todo
kubectl delete deployment -n istio spring-todo-v2
kubectl delete deployment -n istio spring-proj
kubectl delete deployment -n istio spring-chat

kubectl delete gateway -n istio spring-ingress-gateway

kubectl delete vs -n istio spring-ingress-vs
kubectl delete vs -n istio spring-login
kubectl delete vs -n istio spring-todo
kubectl delete vs -n istio spring-proj
kubectl delete vs -n istio spring-chat

kubectl delete dr -n istio spring-main
kubectl delete dr -n istio spring-login
kubectl delete dr -n istio spring-todo
kubectl delete dr -n istio spring-proj
kubectl delete dr -n istio spring-main

kubectl delete sa -n istio spring-main-sa
kubectl delete sa -n istio spring-login-sa
kubectl delete sa -n istio spring-todo-sa
kubectl delete sa -n istio spring-chat-sa
kubectl delete sa -n istio spring-proj-sa

kubectl delete secret -n istio-system istio-ingressgateway-certs
kubectl delete secret -n istio-system istio-ingressgateway-ca-certs

kubectl delete peerauthentication -n istio default
kubectl delete authorizationpolicy -n istio frontend-ingress
kubectl delete requestauthentication -n istio jwt-example

#kubectl delete RequestAuthentication req-auth -n istio
#kubectl delete PeerAuthentication peer-auth -n istio 

