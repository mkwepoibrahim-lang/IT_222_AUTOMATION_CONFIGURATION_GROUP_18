# Assignment 18 – Pharmaceutical Distribution Network

## Project Overview

This project implements a pharmaceutical distribution network connecting two
facilities, Site A and Site B.

The network separates Warehouse terminals and Management systems using VLANs.
Routing between VLANs is provided using router-on-a-stick, while OSPF is used
to provide communication between the two sites.

The network is configured and tested using GNS3 and automated where appropriate
using Python and Netmiko.

---

## Network Topology

The network consists of:

- 2 Routers
  - R1 – Site A
  - R2 – Site B

- 2 Switches
  - SW1 – Site A
  - SW2 – Site B

- 4 PCs
  - PC1 – Site A Warehouse
  - PC2 – Site A Management
  - PC3 – Site B Warehouse
  - PC4 – Site B Management

### Logical Topology

                    Site A
              ┌─────────────────┐
              │       R1        │
              │                 │
              │ Gi0/1           │
              └───────┬─────────┘
                      │
                    Trunk
                      │
                   ┌──┴───┐
                   │ SW1  │
                   └─┬─┬──┘
                     │ │
                    PC1 PC2
                 Warehouse Management
                  VLAN 63   VLAN 73


                10.18.18.0/30
                 R1 ↔ R2


                    Site B
              ┌─────────────────┐
              │       R2        │
              │                 │
              │ Gi0/1           │
              └───────┬─────────┘
                      │
                    Trunk
                      │
                   ┌──┴───┐
                   │ SW2  │
                   └─┬─┬──┘
                     │ │
                    PC3 PC4
                 Warehouse Management
                  VLAN 63   VLAN 73

---

## VLAN Configuration

| VLAN | Name | Purpose |
|------|------|---------|
| 63 | WAREHOUSE | Warehouse terminals |
| 73 | MANAGEMENT | Management systems |

---

## IP Addressing

### Site A

| Device | Network | IP Address |
|--------|---------|------------|
| R1 VLAN 63 | 172.26.63.0/24 | 172.26.63.1 |
| R1 VLAN 73 | 172.26.73.0/24 | 172.26.73.1 |
| PC1 | 172.26.63.0/24 | 172.26.63.10 |
| PC2 | 172.26.73.0/24 | 172.26.73.10 |

### Site B

| Device | Network | IP Address |
|--------|---------|------------|
| R2 VLAN 63 | 172.27.63.0/24 | 172.27.63.1 |
| R2 VLAN 73 | 172.27.73.0/24 | 172.27.73.1 |
| PC3 | 172.27.63.0/24 | 172.27.63.10 |
| PC4 | 172.27.73.0/24 | 172.27.73.10 |

### Router-to-Router Link

| Device | Interface | IP Address |
|--------|-----------|------------|
| R1 | Gi0/0 | 10.18.18.1/30 |
| R2 | Gi0/0 | 10.18.18.2/30 |

Network:

text
10.18.18.0/30