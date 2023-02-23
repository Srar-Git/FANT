# the Flexible Active in-band Network Telemetry
## Introduction
    The data center network of cloud service providers or Internet companies carries a large amount of dynamic traffic, so it is
challenging to handle network problems such as silent failure and load imbalance. Fine-grained network visibility
helps network administrators promptly locate and solve the
above issues, which is very important for maintaining modern
large networks. Traditional network management protocols
such as SNMP, designed primarily for lower bandwidth
networks, employ inefficient polling measurement mechanisms
that work in controller-driven, per-device polling way. So it
cannot reach the ideal accuracy, coverage, and timeliness for
high-density data center network operations and maintenance
at this stage. INT allows packets to collect fine-grained measurements of the flow and the internal state of the device along
its forwarding path, which is valuable for troubleshooting
[6], traffic engineering, and congestion control. Nowadays,
INT is considered an indispensable feature and is implemented
in silicon and devices from multiple vendors. The main
principle of traditional INT is that the source node inserts an
INT header as a tag into the user flow. When a datagram
with the tag passes through an INT-enabled switch, the switch
will embed its internal-device network state such as port traffic
statistics, queue length, timestamp, etc., into the packet. At the
destination of the INT measurement path, there will be INT
sink nodes to extract the measurement results and remove extra
fields added by INT architecture. When the packet carrying the
INT header is not a tagged service packet but a custom packet
injected by the server, the draft defined this as active INT
(ANT). We refer to the dedicated custom packet as a probe
packet and the server as an INT transceiver. The probe packets
will be queued and processed together with the user traffic so
that they can provide accurate measurements.
    These two INT techniques provide the ability to be visible
to the network status in different ways. Passive INT has finer
granularity and greater overhead. Active INT has large-scale
coverage and lower overhead.No matter what kind of INT
system, each INT instance can only obtain real-time traffic
status of the chain of devices along the packet’s trace. So
the network-wide telemetry coverage for the network dashboard requires a high-level orchestration to provision multiple
INT paths that traverse the entire network. Many researchers
have proposed the combination of SDN and ANT to achieve
network-wide measurements. Their solutions exploit SDN ’s
visibility of the full network topology to guide the ANT in constructing multiple appropriate probe traces. These approaches
are lightweight and easy to deploy and are a hot research topic
in network telemetry.
