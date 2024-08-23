# 9800 RMI+RP High Availability

The redundancy management interface is a virtual interface that is created using the “**redun-management interface**” command. The RMI is a secondary interface used for dual-active detection, monitoring the reachability of the standby controller, and supports **Gateway Reachability Detection**. Using RMI+RP along with Gateway Reachability Detection is now considered best practice.

Both WLCs are reachable with basic configuration done

- Enable redundancy on both controllers
```cisco
   redundancy
	   mode sso
```
- Update priority on primary (higher value becomes primary)
```cisco
chassis 1 priority 2
```
- Update chassis number on secondary
```cisco
chassis 1 renumber 2
```
- Form cluster with redun-management command on both controllers
```cisco
redun-management interface Vlan40 chassis 1 address 192.168.1.253 chassis 2 address 192.168.1.251
```
- enable gateway check
```cisco
management gateway-failover enable
```
- save config


Controllors will reload and form cluster, check with
```cisco
show chassis
show redundancy
```

Manual switch over
```cisco
redundancy force-switchover
```

The standby console is not accessible by default, issue the following commands to enable:
```cisco
redundancy
	main-cpu
	standby console enable
```
