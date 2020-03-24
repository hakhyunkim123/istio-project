kubectl delete requestauthentication -n istio-system jwt-example
kubectl delete AuthorizationPolicy -n istio-system frontend-ingress

kubectl delete requestauthentication -n istio jwt-example
kubectl delete AuthorizationPolicy -n istio frontend-ingress

kubectl delete requestauthentication -n istio jwt-test
kubectl delete AuthorizationPolicy -n istio require-jwt

