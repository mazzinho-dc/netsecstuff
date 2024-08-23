Basic Switchport configuration to reference from.

### Access-Port - User
```cisco
interface GigabitEthernet0/1  
	description Client-VLAN1  
	switchport mode access
	switchport access vlan 1
	switchport voice vlan 150
	switchport port-security  
	switchport port-security maximum 2  
	switchport nonegotiate  
	storm-control broadcast level 25.00  
	spanning-tree portfast  
	spanning-tree bpduguard enable
```

### Access-Port - Printer
```cisco 
interface GigabitEthernet0/1  
	description Printer  
	switchport mode access  
	switchport access vlan 10  
	switchport nonegotiate  
	storm-control broadcast level 25.00  
	switchport port-security  
	spanning-tree portfast edge  
	spanning-tree bpduguard enable
```

### WLAN-Access-Point
```cisco
interface GigabitEthernet0/1
	description Access-Point
	switchport trunk native vlan 80
	switchport trunk allowed vlan 200,210,220,1000
	switchport mode trunk
	switchport nonegotiate
	storm-control broadcast level 25.00
	mls qos trust cos
	srr-queue bandwidth share 1 30 35 5
	priority-queue out
	auto qos trust
	spanning-tree link-type point-to-point
```

### Switch-to-Switch single link
```cisco
interface GigabitEthernet0/1
	description SWITCH
	switchport mode trunk
	switchport trunk native vlan 666
	switchport nonegotiate
	storm-control broadcast level 25.00
	mls qos trust cos
	srr-queue bandwidth share 1 30 35 5
	priority-queue out
	auto qos trust
	spanning-tree link-type point-to-point
```

### Switch-to-Switch Multi link
```cisco
interface port-channel 1
	description LAG-Switch2
	switchport mode trunk
	switchport trunk native vlan 666
	switchport nonegotiate
	spanning-tree link-type point-to-point
	storm-control broadcast level 25.00

interface range GigabitEthernet0/1-2
	description SWITCH2
	switchport mode trunk
	switchport trunk native vlan 666
	switchport nonegotiate
	storm-control broadcast level 25.00
	mls qos trust cos
	srr-queue bandwidth share 1 30 35 5
	priority-queue out
	auto qos trust
	spanning-tree link-type point-to-point
	channel-group 1 mode active
```

