# A code to perfrom the VPC validation of a nexus device
A python code to perform the VPC(virtual port channel validation) which check the parameters required for the switch to in VPC.

## What we are achieving through this code.
```
We have taken two device on which we will performing the validation.
What is vpc ?
A virtual PortChannel (vPC) allows links that are physically connected to two different devices to appear as a single PortChannel to a third device.
Through this code we are checking the below features.
1.Domain
2.Peer link adjacency
3.Peer keep alive link
4.Reachability of the other switch
5.vpc system mac 
6.Port channel summary of the vpc peer link.
---
