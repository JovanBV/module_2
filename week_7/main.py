from pprint import pprint

from jwcrypto.jwk import JWK
from jwt import JWT, jwk_from_dict


def generate_keys():
    jwk = JWK.generate(kty="RSA", size=2048, alg="RS256", use="sig", kid="420")
    return jwk.export_private(as_dict=True), jwk.export_public(as_dict=True)


if __name__ == "__main__":
    data = {"sub": "1234567890", "name": "John Doe", "admin": True, "iat": 1516239022}

    private_key, public_key = generate_keys()
    pprint(private_key)
    print()
    pprint(public_key)
    print()
