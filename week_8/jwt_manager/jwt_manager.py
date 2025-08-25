import jwt
from jwt.exceptions import InvalidKeyError
import time

class JWT_Manager:
    def __init__(self):
        self.private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAx3E+KEr2yqlVTCoNTj1EvWgeQn20Sc3IX7K6qoYpmVznM4On
XM5Br56MKh9J4qis2iWEZeOwCWb+5kY8X1G4IkFiMrHLwQCysQww8XjgPNfPjR9/
PWfHtF8DP8q/fe6bMPH7HQl6tJUr7zhSB367fBSdssHiVAH5lz48n4KxDLsR3hrd
yU8ADtvPpukX/UsnRN22hI/Fd78KjnFERrqka4FjYS5Llnfu7d+TwTnCXAbVhTsK
HovfnuOzldWUw/Jobt3toClZyfo0AIdwiv1Fg+LBJaT+vi4IJOn4/+jzx9EEgobW
+MZOuSxzB4u1U8MmvqMOeaXm5eZHxNROjoVN4QIDAQABAoIBAC6QZOe5YNc+I7kN
lF+w9EyYc4AooyAcGG0naGeJvUqeIyim0ztauIFNLgJjnbd6lCi2W6wCNcZsMpUG
zu+eP7RXuZqGYkDkbdPiOccW5put8zpKoUVv5nNZP4P0TTMUs00BIhTMcsaYkVJf
vt8bGqDEm3DxzWq5r1E9aaAAPl/vHvIvaZKawuTbw+ubDTppeVhMmAaCSk09F5RQ
+oil7kezfWj6FqODYi2FP+6+BPPJU3/NBO6YaJ3tjgPDU4CVloU5XFt/4LHvuncU
n5wsew+KyhbgOvtvwkX66LX1xVZ653u3gOOc+W9HB7DKVEDc6c4D/joKjYqnr6Qf
VPEYQmUCgYEA/SqDyZgNtkXSA/STvSK2JyRblZ+iuc1+drwbDoPe4ZZ6ZGfzV3k3
mf4KAgJZ6mgzRAfsgGncDeaDk6PZ/8TLZPh1Pknm5QCUTCdYo2zDeahUpZ5SGR8m
rWocx5x9wAqapNb45XkNuS/vzWnJD/cRgm0i1ZANZqp535110Nj0BFMCgYEAyazG
UHlCZp57ADm8wT1IZMRwY2Xh+Q0osE69F0zlyLpC/cLYrriUtgcu+MqjFPkxQbsi
uVyo31Eb+wxYUTAOLt2fwN+RATIgalYLVjtAnl2oR+eWl7pBGQPUOZ9GI1r23Ru4
Bzr+Hfj948ZQ12at8ywk4lRPLRv/vAd2sxt0nnsCgYEAw0Sok7SRVvaxj1V1IpwE
bVpwvY58n91tXr2mDOMP5WYAjzNSkTSw+zjjlTslCVVHvYBzHXUJQzt6X0UxX0L2
MrIlFF9CFX4F5Fsw1hSNDWgVqgzce/34AifnfNsqbxZ+wwgAwFZHjH/58bFXYNYL
jlMJXDoY7Agvqpe0CNteE3sCgYEAuXa/JZBuBQsnWGzAbgEaizivlmlCZ5O3YHP4
pu3bvz2zj8RZGky6za9LfhZz5TzJFIaxBz/0OPJRRgzzRy5nTKgZWvj+U9gyQTgB
0vpIkZrVv9J1BfGOHiAMUjVr/eWQcoQkN9oDibLKYWamP4C45ZEqFk2sRnKiOtuu
SEYud/MCgYEAhELw4xp8+hCJsPrgR8t04dxST5mdIflW+QklHLakeegm3pKtL7du
+pOHZfjeWqDCSjgm4Z+NUOad/4uOioC6L9tcQyIQt9MRRbGFENr4Apz2Ua3Lh9Ct
vPBbdC6pAUT3OYOaWiWjQhv/SOFDxPoiPxXpZnFiqosUPCsDD5bnKGk=
-----END RSA PRIVATE KEY-----"""
        self.public_key = """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAx3E+KEr2yqlVTCoNTj1EvWgeQn20Sc3IX7K6qoYpmVznM4OnXM5B
r56MKh9J4qis2iWEZeOwCWb+5kY8X1G4IkFiMrHLwQCysQww8XjgPNfPjR9/PWfH
tF8DP8q/fe6bMPH7HQl6tJUr7zhSB367fBSdssHiVAH5lz48n4KxDLsR3hrdyU8A
DtvPpukX/UsnRN22hI/Fd78KjnFERrqka4FjYS5Llnfu7d+TwTnCXAbVhTsKHovf
nuOzldWUw/Jobt3toClZyfo0AIdwiv1Fg+LBJaT+vi4IJOn4/+jzx9EEgobW+MZO
uSxzB4u1U8MmvqMOeaXm5eZHxNROjoVN4QIDAQAB
-----END RSA PUBLIC KEY-----
"""

    def encode(self, data):
        try:
            payload = {
                "data": data,
                "iat": int(time.time())
            }
            return jwt.encode(payload, self.private_key, algorithm="RS256")
        except Exception as e:
            print("Error encoding the data: ", e)

    def decode(self, token) :
        try:
            return jwt.decode(token, self.public_key, algorithms=["RS256"])
        except Exception as e:
            print("Error decoding JWT:", e)
            return None
        



jwt_manager = JWT_Manager()