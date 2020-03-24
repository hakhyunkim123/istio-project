#!/usr/bin/python

# Copyright 2018 Istio Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Python script generates a JWT signed with custom private key.

Example:
./gen-jwt.py  --iss example-issuer --aud foo,bar --claims=email:foo@google.com,dead:beef key.pem -listclaim key1 val2 val3 -listclaim key2 val3 val4
"""
from __future__ import print_function
import argparse
import time

from jwcrypto import jwt, jwk


def gen_jwt_token():
    args = { 'key' : './key.pem',
		'iss' : 'testing@secure.istio.io',
		'sub' : None,
		'expire' : '3600',
		'aud' : None
    }
    """Generates a signed JSON Web Token from local private key."""
    with open(args['key']) as f:
        pem_data = f.read()
    f.closed

    pem_data_encode = pem_data.encode("utf-8")
    key = jwk.JWK.from_pem(pem_data_encode)

    if 'jwks' in args:
        with open(args['jwks'], "w+") as fout:
            fout.write("{ \"keys\":[ ")
            fout.write(key.export(private_key=False))
            fout.write("]}")
        fout.close

    now = int(time.time())
    payload = {
        # expire in one hour.
        "exp": now + int(args['expire']),
        "iat": now,
    }
    if 'iss' in args:
        payload["iss"] = args['iss']
    if 'sub' in args:
        payload["sub"] = args['sub']
    else:
        payload["sub"] = args['iss']

    if 'aud' in args:
        if "," in str(args['aud']):
            payload["aud"] = args['aud'].split(",")
        else:
            payload["aud"] = args['aud']

    if 'claims' in args:
        for item in args['claims'].split(","):
            k, v = item.split(':')
            payload[k] = v

    if 'listclaim' in args:
        for item in args['listclaim']:
            if (len(item) > 1):
                k = item[0]
                v = item[1:]
                payload[k] = v

    token = jwt.JWT(header={"alg": "RS256", "typ": "JWT", "kid": key.key_id},
                    claims=payload)

    token.make_signed_token(key)

    return token.serialize()


def get_jwt_token():
	return gen_jwt_token()
