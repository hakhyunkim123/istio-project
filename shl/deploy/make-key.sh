openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -subj '/O=hhk Inc./CN=hhk.com' -keyout hhk.com.key -out hhk.com.crt

openssl req -out test.hhk.com.csr -newkey rsa:2048 -nodes -keyout  test.hhk.com.key -subj "/CN=test.hhk.com/O=hhkim94 organization"

openssl x509 -req -days 365 -CA hhk.com.crt -CAkey hhk.com.key -set_serial 0 -in test.hhk.com.csr -out test.hhk.com.crt

mv *.key /home/hh/git/istio-project/pki
mv *.crt /home/hh/git/istio-project/pki
mv *.csr /home/hh/git/istio-project/pki

