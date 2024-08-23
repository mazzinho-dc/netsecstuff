# IOS XE SSH Best Practice

Default
```cisco
SSH Enabled - version 1.99
Authentication methods:publickey,keyboard-interactive,password
Authentication Publickey Algorithms:x509v3-ssh-rsa,ssh-rsa,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,ssh-ed25519,x509v3-ecdsa-sha2-nistp256,x509v3-ecdsa-sha2-nistp384,x509v3-ecdsa-sha2-nistp521,rsa-sha2-256,rsa-sha2-512
Hostkey Algorithms:x509v3-ssh-rsa,rsa-sha2-512,rsa-sha2-256,ssh-rsa
Encryption Algorithms:chacha20-poly1305@openssh.com,aes128-gcm@openssh.com,aes256-gcm@openssh.com,aes128-gcm,aes256-gcm,aes128-ctr,aes192-ctr,aes256-ctr
MAC Algorithms:hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-sha1
KEX Algorithms:curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group14-sha1
Authentication timeout: 120 secs; Authentication retries: 3
Minimum expected Diffie Hellman key size : 2048 bits
IOS Keys in SECSH format(ssh-rsa, base64 encoded): TP-self-signed-2851517665
Modulus Size : 2048 bits
```


Create RSA Key at least 4096 bits in length
```cisco
crypto key generate rsa modulus 4096 label RSA4096_SSH_KEY

ip ssh rsa keypair-name RSA4096_SSH_KEY
ip ssh version 2
ip ssh server algorithm authentication keyboard
```

In today’s digital landscape, prioritize AES encryption with a 256-bit key length for top-tier security. When it comes to efficiency, GCMP outshines CCMP. And within CCMP, it’s better to go with CTR mode over CBC for added security.
```cisco
ip ssh server algorithm encryption aes256-gcm aes256-ctr
```

When it comes to Message Integrity, you should always use SHA2 (over SHA1 or MD5 which is deprecated in current standards).
```cisco
ip ssh server algorithm mac hmac-sha2-512 hmac-sha2-256
```

Speaking of key exchange algorithms, Elliptic Curve Diffie-Hellman takes the lead. For optimal security, go with NIST P-521 and NIST P-384, which are endorsed by the NSA.
```cisco
ip ssh server algorithm kex ecdh-sha2-nistp521 ecdh-sha2-nistp384
```

public key to match same NIST P-curves
```cisco
ip ssh server algorithm publickey ecdsa-sha2-nistp521 ecdsa-sha2-nistp384
```

Server algorithm hostkeys
```cisco
ip ssh server algorithm hostkey rsa-sha2-512 rsa-sha2-256
```

In summary here are all the CLI to match that cisco best practices
```cisco
crypto key generate rsa modulus 4096 label RSA4096_SSH_KEY
ip ssh rsa keypair-name RSA4096_SSH_KEY
ip ssh version 2
ip ssh server algorithm authentication keyboard
ip ssh server algorithm mac hmac-sha2-512 hmac-sha2-256
ip ssh server algorithm encryption aes256-gcm aes256-ctr
ip ssh server algorithm kex ecdh-sha2-nistp521 ecdh-sha2-nistp384
ip ssh server algorithm hostkey rsa-sha2-512 rsa-sha2-256
ip ssh server algorithm publickey ecdsa-sha2-nistp521 ecdsa-sha2-nistp384
```

SSH Security Best Practice:
```Cisco
WLC#sh ip ssh
SSH Enabled - version 2.0
Authentication methods:keyboard-interactive
Authentication Publickey Algorithms:ecdsa-sha2-nistp521,ecdsa-sha2-nistp384
Hostkey Algorithms:rsa-sha2-512,rsa-sha2-256
Encryption Algorithms:aes256-gcm,aes256-ctr
MAC Algorithms:hmac-sha2-512,hmac-sha2-256
KEX Algorithms:ecdh-sha2-nistp521,ecdh-sha2-nistp384
Authentication timeout: 120 secs; Authentication retries: 3
Minimum expected Diffie Hellman key size : 2048 bits
IOS Keys in SECSH format(ssh-rsa, base64 encoded): RSA4096_SSH_KEY
Modulus Size : 4096 bits
```

In case you want to roll-back your changes, here are the CLI commands to put default settings.
```cisco
  default ip ssh server algorithm encryption
  default ip ssh server algorithm hostkey
  default ip ssh server algorithm kex
  default ip ssh server algorithm mac
  default ip ssh server algorithm authentication
  default ip ssh server algorithm publickey
  ```

If you are keen on IOS (not IOS-XE), please find the [best practices document](https://community.cisco.com/t5/security-knowledge-base/guide-to-better-ssh-security/ta-p/3133344)
