# the Flexible Active in-band Network Telemetry
## Introduction

Network management applications require more
comprehensive measurement results to support new features.
Catering to the trend, various switch vendors are constantly
adding network measurement indicators to the telemetry supporting list. The
increase of upload measurement items enables the networkwide telemetry framework to offer multi-directional network
visibility for network managers to locate network anomalies.
But at the same time, it also brings about the processing burden
on the INT controller and larger overhead of the network,
which will impede the network telemetry framework to be
widely deployed.

To solve the above problems, we propose a flexible active
INT (FANT) method, which decouples the solution into a
mechanism and a strategy. The workflow of daily network
troubleshooting is to check the general measurement results,
such as bandwidth and latency from the data center network
of the cloud service provider, to determine whether there is
a problem with the network at first and then analyze other
items such as queue buffers to indicate the specific problems.
Inspired by this troubleshooting process, we divide the entire
measurement sets into two parts: basic measurement and
detailed measurement, according to the relationship between
them. FANT uses ANT architecture to inject many dedicated
packets routed by source routing technology (which we call
the INT probe as follows) to retrieve the basic network
status information from the whole network. Next, the INT
controller classifies the basic network status information and
identifies the abnormal parts. Then based on the abnormal
parts, FANT switches some of the original INT probes to the
probes with special marks in the next measurement cycle for
fetching detailed measurements from the device. Deploying
probe traces for detailed measurements will collect more
specific and comprehensive network status, thereby providing
more excellent assistance for network monitoring and maintenance.
However, detailed measurements will also lead to
network overhead and an increasing load on the INT controller.
Therefore, selecting which INT probes should be switched to
perform detailed measurements is necessary. We propose a
switch instruction policy based on IDA* algorithm to achieve
a solution close to the theoretical optimal value, which can
significantly reduce the network overhead and INT controller’s
load. In addition, under the trend of monitoring and operating
the network more accurately, To make the policy available
when the measurement cycle is further reduced, we also
update the switch instruction policy to a dynamic version.
The dynamic version optimizes the calculation speed at high
sensitivity and reduces the risk of over-control while keeping
a not-bad performance on network overhead reduction.

## Algorithms
- Greedy
- Dynamic Cover
- Optimal Static

## Topology
- FatTree
- SpineLeaf
- BackBone

> the files in `Topology`
> - roads.txt: the probe roads of the topo
> - pathNums.txt: the number of roads of the topo

## Algorithm Structure
The structure include `UploadChanges`, `ExecutionTime`, `HighFrequencyUploadChanges`, `OptimizeDLX` and `OptimizeDynamic`. Everyone of them use `Greedy`, `Dynamic Cover` and `Optimal Static` to compare with.
### Greedy
**greedy.py**

the greedy set cover file.

### Optimial Static
**dancingLink.py**

the optimal static set cover file, uses IDA* and dancing link to cover sets.

### Dynamic
**run.py**

the main function of the dynamic random cover.

**dynamic_update.py**

functions of `insert`, `remove` elements and `updating`.

**random_cover.py**

the random cover function, will be called at two above stages.

## Dependency

All code developed and should run with `Python3.9`
