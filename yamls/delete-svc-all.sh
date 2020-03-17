kubectl delete svc -n istio spring-main
kubectl delete svc -n istio spring-chat
kubectl delete svc -n istio spring-proj
kubectl delete svc -n istio spring-login
kubectl delete svc -n istio spring-todo

kubectl delete deployment -n istio spring-main
kubectl delete deployment -n istio spring-todo
kubectl delete deployment -n istio spring-login
kubectl delete deployment -n istio spring-proj
kubectl delete deployment -n istio spring-chat


