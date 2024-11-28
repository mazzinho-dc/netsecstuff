# EWC Initial Config
### Step 1 - Configure the Host Name (Optional)
==========================================
WLC7069.5A74.7C78#conf t
WLC7069.5A74.7C78 (config)#hostname <#host-name>
<#host-name>(config)#end

For example:
WLC7069.5A74.7C78#conf t
WLC7069.5A74.7C78(config)#hostname C9800-AP
C9800-AP(config)#end

### Step 2A - Set the administrative username/password
==================================================
C9800-AP#conf t
C9800-AP(config)# username <#username> privilege 15 password <#password>
C9800-AP(config)#end

For example:
C9800-AP#conf t
C9800-AP(config)# username admin privilege 15 password Network123
C9800-AP(config)#end

### Step 2B - Configure the AP Profile
==================================
To configure the AP management username/password for AP profile,
Please use the SAME username/password configured in step 2A.

C9800-AP#conf t
C9800-AP(config)#ap profile default-ap-profile
C9800-AP(config-ap-profile)#mgmtuser username <#username> password 0 <#password> secret 0 <#password>
C9800-AP(config-ap-profile)#end

For example, to configure the AP management username and password
C9800-AP#conf t
C9800-AP(config)#ap profile default-ap-profile
C9800-AP(config-ap-profile)#mgmtuser username admin password 0 Network123 secret 0 Network123
C9800-AP(config-ap-profile)#end

### Step 3A - Configure the Wireless Local Area Network
===================================================
C9800-AP#conf t
C9800-AP(config)#wlan <#wlan-profile-name> <#wlan-id> <#ssid-network-name>
C9800-AP(config-wlan)# no security wpa akm dot1x
C9800-AP(config-wlan)# security wpa psk set-key ascii 0 <#pre-shared-key>
C9800-AP(config-wlan)# security wpa akm psk
C9800-AP(config-wlan)# no shutdown
C9800-AP(config-wlan)#end

For example to configure a PSK WLAN named "employee" with pre-shared key "Cisco123"
C9800-AP#conf t
C9800-AP(config)# wlan employee 1 employee
C9800-AP(config-wlan)# no security wpa akm dot1x
C9800-AP(config-wlan)# security wpa psk set-key ascii 0 Cisco123
C9800-AP(config-wlan)# security wpa akm psk
C9800-AP(config-wlan)# no shutdown
C9800-AP(config-wlan)#end

### Step 3B - Configure the Wireless Profile Policy
===============================================
The wireless profile policy name must be SAME as the <#wlan-profile-name>
configured in step 3A.

C9800-AP#conf t
C9800-AP(config)#wireless profile policy <#wlan-profile-name>
C9800-AP(config-wireless-policy)#no central association
C9800-AP(config-wireless-policy)#no central dhcp
C9800-AP(config-wireless-policy)#no central switching
C9800-AP(config-wireless-policy)#http-tlv-caching
C9800-AP(config-wireless-policy)#session-timeout 86400
C9800-AP(config-wireless-policy)#no shutdown
C9800-AP(config-wireless-policy)#end

For example to configure the profile policy for WLAN profile name "employee"
C9800-AP#conf t
C9800-AP(config)#wireless profile policy employee
C9800-AP(config-wireless-policy)#no central association
C9800-AP(config-wireless-policy)#no central dhcp
C9800-AP(config-wireless-policy)#no central switching
C9800-AP(config-wireless-policy)#http-tlv-caching
C9800-AP(config-wireless-policy)#session-timeout 86400
C9800-AP(config-wireless-policy)#no shutdown
C9800-AP(config-wireless-policy)#end

### Step 3C - Configure the Default Policy Tag
==========================================
To map the WLAN to the Profile Policy, use the SAME <#wlan-profile-name>
configured in step 3A.

C9800-AP#conf t
C9800-AP(config)#wireless tag policy default-policy-tag
C9800-AP(config-policy-tag)#wlan <#wlan-profile-name> policy <#wlan-profile-name>
C9800-AP(config-policy-tag)#end

For example to map the WLAN profile name "employee" to the policy profile
name "employee" in the default policy tag
C9800-AP#conf t
C9800-AP(config)#wireless tag policy default-policy-tag
C9800-AP(config-policy-tag)#wlan employee policy employee
C9800-AP(config-policy-tag)#end

### Step 4 - Turn on the global encryption
======================================
This config is highly recommended for the security.

Without this config, all the credentials are saved as plain text.
With this configuration, all the credentials are saved as encrypted strings.

User needs to input a "key" for password here, It's recommended to use the SAME
administrative password configured in step 2A as the key for password encryption.

C9800-AP#conf t
C9800-AP(config)#service password-encryption
C9800-AP(config)#password encryption aes
C9800-AP(config)#key config-key newpass <#password>
C9800-AP(config)#end

For example, the global encryption can be configured as below
C9800-AP#conf t
C9800-AP(config)#service password-encryption
C9800-AP(config)#password encryption aes
C9800-AP(config)#key config-key newpass Network123
C9800-AP(config)#end

### Step 5 - Save the Configuration
================================

### STOP: IMPORTANT NOTE 1: YOU WILL LOSE CONNECTIVITY NOW
======================================================
When the configuration is saved, the connectivity to the SSH session
will be lost.

### STOP: IMPORTANT NOTE 2: THIS IS HOW YOU CONNECT BACK
====================================================

WEBUI:
To make any further configurations to the device, please use the WEBUI.
In order to access the WEBUI, please connect the wireless client to the
Network configured in step 3A and type the URL "https://mywifi.cisco.com"
in the browser. Please use the credentials (username/password) configured
in step 2A to login to the WEBUI.

SSH:
To SSH to the device going forward, connect to the
Network created in step 3A and please use the admin username/password
configured in step 2A

NOW execute the below command to complete the device provisioning:

C9800-AP# write memory


##############################################################################

