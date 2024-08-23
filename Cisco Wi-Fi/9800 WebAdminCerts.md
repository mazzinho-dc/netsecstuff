# 9800 Web Admin Certs

Secure web admin portal with EC based certificate, trsted by own CA. To escape Browser Warning struggle.

Generate Keys and label with name
```cisco
crypto key generate ec keysize 256 label WEBADMIN_KEY
**The name for the keys will be: WEBADMIN_KEY**
```

Define a PKI trustpoint

```cisco
crypto pki trustpoint WEB-ADMIN24
 enrollment terminal pem
 subject-name C=DE, ST=NRW, L=Isselburg, O=IHI, OU=IT, CN=sw-vw-edv.ihi.local
 subject-alt-name sw-vw-edv.ihi.local
 revocation-check none
 eckeypair WEBADMIN_KEY
 hash sha256
```

Enroll and authenticate PKI trust point with CA server
Generate CSR
```cisco
crypto pki enroll WEB-ADMIN24

% Include the router serial number in the subject name? [yes/no]: no
% Include an IP address in the subject name? [no]: no
Display Certificate Request to terminal? [yes/no]: yes

Certificate Request follows:
-----BEGIN CERTIFICATE REQUEST-----
-----END CERTIFICATE REQUEST-----

Redisplay enrollment request? [yes/no]: no
```

Download CA Certificate (Root/Intermediate) Base64
```cisco
crypto pki authenticate WEB-ADMIN24
Enter the base 64 encoded CA Certificate

.
.
.

% Do you accept this certificate? [yes/no]: yes
Trustpoint CA certificate accepted.
% Certificate successfully imported
```

Next import issued certificate for 9800 webadmin
```cisco
crypto pki import WEB-ADMIN24 certificate
Enter the base 64 encoded certificate.
End with a blank line or the word "quit" on a line by itself

-----BEGIN CERTIFICATE-----
.
.
.
-----END CERTIFICATE-----

% Router Certificate successfully imported

```

Connect WEB-ADMIN24 trustpoint to HTTP Access
and restart http service
```cisco
ip http secure-trustpoint WEB-ADMIN24
no ip http server
ip http server
```

