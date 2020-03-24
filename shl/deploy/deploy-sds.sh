kubectl delete secret istio-ingressgateway-certs istio-ingressgateway-ca-certs -n istio-system
kubectl -n istio-system delete secret spring-credential

kubectl create -n istio-system secret generic spring-credential --from-file=key=/home/hh/git/istio-project/pki/test.hhk.com.key \
--from-file=cert=/home/hh/git/istio-project/pki/test.hhk.com.crt --from-file=cacert=/home/hh/git/istio-project/pki/hhk.com.crt

