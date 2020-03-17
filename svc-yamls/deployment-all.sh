kubectl apply -f main.yaml -n istio
kubectl apply -f login.yaml -n istio
kubectl apply -f todo.yaml -n istio
kubectl apply -f proj.yaml -n istio
kubectl apply -f chat.yaml -n istio

kubectl apply -f ingress_msa.yaml -n istio
