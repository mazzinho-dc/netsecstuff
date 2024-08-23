# 9800 Manual Initial Setup


### Zutaten

Jeder Großbuchstabe entspricht einer Einstellung, die Sie vor Verwendung der Konfigurationsvorlage ändern müssen:

| **Erforderlicher Wert**                                      | **Name in Vorlage** | **Beispiel**        |
| ------------------------------------------------------------ | ------------------- | ------------------- |
| WLC Gerätename                                               | [HOSTNAME]          | DE-MYWLC            |
| Out-of-Band-Management-IP                                    | [OOM_IP]            | 192.168.0.25        |
| Out-of-Band Management Default-Gateway                       | [OOM_GW]            | 192.168.0.1         |
| Administrator-Benutzername                                   | [ADMIN]             | admin               |
| Administratorkennwort                                        | [KENNWORT]          | ah1-7k++a1          |
| Enable Secret                                                | [ENASECRET]         | ah1-7k++a1          |
| Benutzername des AP-Administrators                           | [AP_ADMIN]          | admin               |
| AP CLI-Kennwort                                              | [AP_PASSWORT]       | Alkhb90jlih         |
| AP CLI-Secret                                                | [AP_SECRET]         | kH20-9 JJH          |
| Name des Controller-Hosts                                    | [WLC_NAME]          | 9800-bcn-1          |
| Name der Firmendomäne                                        | [DOMÄNE_NAME]       | company.com         |
| Client-VLAN-ID                                               | [CLIENT_VLAN]       | 15                  |
| Client-VLAN-Name                                             | [VLAN_NAME]         | Client_VLAN         |
| VLAN WMI                                                     | [WMI_VLAN]          | 25                  |
| Wireless Management Interface-IP                             | [WMI_IP]            | 192.168.25.10       |
| Wireless Management Interface-Maske                          | [WMI_MASK]          | 255.255.255.0       |
| Standard-GW für Wireless-Verwaltungsschnittstelle            | [WMI_GW]            | 192.168.25.1        |
| NTP-Server                                                   | [NTP_IP]            | 192.168.1.2         |
| Radius-Server-IP                                             | [RADIUS_IP]         | 192.168.0.98        |
| RADIUS-Schlüssel oder gemeinsam genutzter geheimer Schlüssel | [RADIUS_KEY]        | ThisIsASharedSecret |
| WLAN SSID WPA2                                               | [SSID-PSK]          | persönlich          |



hostname [HOSTNAME]
enable secret [ENASECRET]

interface GigabitEthernet0
vrf forwarding Mgmt-intf
ip address dhcp
ip add [OOM_IP] 255.255.255.0  
negotiate auto
exit  

ip route vrf Mgmt-intf 0.0.0.0 0.0.0.0 [OOM_GW]

no ip domain lookup
username [ADMIN] privilege 15 password 0 [PASSWORD]
ip domain name [DOMAIN_NAME]

aaa new-model  
aaa authentication login default local  
aaa authentication login CONSOLE none  
aaa authorization exec default local  
aaa authorization network default local

line con 0  
privilege level 15  
login authentication CONSOLE
logging sync
exit   
crypto key generate rsa modulus 2048
ip ssh version 2
end
wr

cdp run  
int te0/0/0   
cdp ena  
int te0/0/1  
cdp ena

### VLANs erstellen

vlan [CLIENT_VLAN]  
name [VLAN_NAME]  
  
vlan [WMI_VLAN]  
name [WIRELESS_MGMT_VLAN]

### Konfigurieren von Datenschnittstellen - Appliances

interface TenGigabitEthernet0/0/0  
description You should put here your switch name and port   
switchport trunk allowed vlan [CLIENT_VLAN],[WMI_VLAN]  
switchport mode trunk  
no negotiation auto  
channel-group 1 mode active  
  
interface TenGigabitEthernet0/0/1  
description You should put here your switch name and port   
switchport trunk allowed vlan [CLIENT_VLAN],[WMI_VLAN]  
switchport mode trunk  
no negotiation auto  
channel-group 1 mode active  
no shut  
  
int po1  
switchport trunk allowed vlan [CLIENT_VLAN],[WMI_VLAN]  
switchport mode trunk  
no shut

!!Configure the same in switch and spanning-tree portfast trunk  
port-channel load-balance src-dst-mixed-ip-port

### Konfigurieren der Wireless-Verwaltungsschnittstelle

int vlan [WMI_VLAN]  
ip add [WMI_IP] [WMI_MASK]  
no shut  
  
ip route 0.0.0.0 0.0.0.0 [WMI_GW]  
  
!! The interface name will normally be something like Vlan25, depending on your WMI VLAN ID  
wireless management interface Vlan[WMI_VLAN]

### Zeitzone und NTP-Sincronisierung konfigurieren

ntp server [NTP_IP]  
!!This is European Central Time, it should be adjusted to your local time zone  
clock timezone CET 1 0  
clock summer-time CEST recurring last Sun Mar 2:00 last Sun Oct 3:00


### VTY-Zugriff und andere lokale Services

service timestamps debug datetime msec  
service timestamps log datetime msec  
service tcp-keepalives-in  
service tcp-keepalives-out  
logging buffered 512000  
  
line vty 0 15  
transport input ssh  
  
line vty 16 50  
transport input ssh

ap dot11 24ghz cleanair  
ap dot11 5ghz cleanair  
no ap dot11 5ghz SI  

### Radius-Konfiguration
radius server ISE  
address ipv4 [RADIUS_IP] auth-port 1645 acct-port 1646  
key [RADIUS_KEY]  
automate-tester username dummy probe-on   
  
aaa group server radius ISE_GROUP  
server name ISE  
  
aaa authentication dot1x ISE group ISE_GROUP  
  
radius-server dead-criteria time 5 tries 3  
radius-server deadtime 5

### Wireless-Konfiguration

!!Important: replace country list with to match your location  
!!These commands are supported from 17.3 and higher  
wireless country DE

ap profile default-ap-profile  
  mgmtuser username [AP_ADMIN] password 0 [AP_PASSWORD] secret 0 [AP_SECRET]  
  ssh  
  syslog host [AP_SYSLOG]  
  
device classifier

### Erstellen von WLANs - WPA2-PSK

wlan wlan_psk 1 [SSID-PSK]  
security wpa psk set-key ascii 0 [WLANPSK]  
no security wpa akm dot1x  
security wpa akm psk  
no shutdown

### Erstellen von Richtlinien für APs im lokalen Modus

wireless profile policy policy_local_clients  
  description local_vlan  
  dhcp-tlv-caching  
  http-tlv-caching  
  radius-profiling  
  session-timeout 86400  
  idle-timeout 3600  
  vlan [CLIENT_VLAN]  
  no shutdown
  
wireless tag policy default-policy-tag
  description local  
  
wireless tag policy policy_tag_local  
  description "Tag for APs on local mode"  
  !! Include here only the WLANs types from previous sections, that you have defined and are interesting for your organization  
  !! For guest WLANS (CWA/LWA), it is common to use a different policy profile, to map to a different VLAN  
  wlan wlan_psk policy policy policy_local_clients
