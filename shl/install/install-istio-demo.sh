#istioctl manifest apply --set profile=demo

istioctl manifest apply --set profile=demo \
  --set values.global.mtls.auto=false \
  --set values.global.mtls.enabled=true \
  --set values.global.sds.enabled=true
