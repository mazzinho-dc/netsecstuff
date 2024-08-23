#### Inactive Ports
example not active since 16w
```cisco 
show int | i proto.*notconnect|proto.*administratively down|Last in.* [1][6-9]w|Last in.*[2-9][0-9]w|[0-9]y|disabled|Last input never, output never, output hang never
```

#### Config Backup via archive
In this example every week and on config save, via FTP in root folder
```cisco 
archive  
	log config  
	logging enable  
	hidekeys  
	path ftp://username:password*@10.10.10.11/$h-$t-config.cfg  
	write-memory  
	time-period 10080
```

#### Secure SSH template IOS
```cisco
conf t
crypto key generate rsa modulus 4096 label RSA4096_SSH_KEY

ip ssh rsa keypair-name RSA4096_SSH_KEY
ip ssh version 2
ip ssh server algorithm authentication keyboard
ip ssh server algorithm encryption aes256-ctr
ip ssh server algorithm mac hmac-sha2-512 hmac-sha2-256
```
