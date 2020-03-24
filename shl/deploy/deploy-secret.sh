kubectl delete secret istio-ingressgateway-certs istio-ingressgateway-ca-certs -n istio-system

kubectl create -n istio-system secret tls istio-ingressgateway-certs --key /home/hh/git/istio-project/pki/test.hhk.com.key --cert /home/hh/git/istio-project/pki/test.hhk.com.crt

kubectl create -n istio-system secret generic istio-ingressgateway-ca-certs --from-file=/home/hh/git/istio-project/pki/hhk.com.crt

kubectl exec -it -n istio-system $(kubectl -n istio-system get pods -l istio=ingressgateway -o jsonpath='{.items[0].metadata.name}') -- ls -al /etc/istio/ingressgateway-certs

