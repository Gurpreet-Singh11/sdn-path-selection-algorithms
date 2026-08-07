#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time
import os

def install_flows(net):
    """Install flow rules manually on each switch"""
    info('*** Installing flow rules on all switches\n')

    # Get hosts
    h1 = net.get('h1')
    h2 = net.get('h2')
    s1 = net.get('s1')
    s2 = net.get('s2')
    s3 = net.get('s3')
    s4 = net.get('s4')

    # Get MAC addresses
    h1_mac = h1.MAC()
    h2_mac = h2.MAC()

    info(f'*** H1 MAC: {h1_mac}\n')
    info(f'*** H2 MAC: {h2_mac}\n')

    # Clear existing flows on all switches
    for sw in [s1, s2, s3, s4]:
        sw.cmd(f'ovs-ofctl del-flows {sw.name}')

    # === S1 flows ===
    # Traffic from H1 going to H2 -> forward to S2 (Path A)
    s1.cmd(f'ovs-ofctl add-flow s1 "priority=100,dl_dst={h2_mac},actions=output:2"')
    # Traffic from S2/S3 coming back to H1 -> forward to H1
    s1.cmd(f'ovs-ofctl add-flow s1 "priority=100,dl_dst={h1_mac},actions=output:1"')
    # ARP flood
    s1.cmd('ovs-ofctl add-flow s1 "priority=1,arp,actions=flood"')

    # === S2 flows (Path A middle switch) ===
    # Traffic going to H2 -> forward to S4
    s2.cmd(f'ovs-ofctl add-flow s2 "priority=100,dl_dst={h2_mac},actions=output:2"')
    # Traffic coming back to H1 -> forward to S1
    s2.cmd(f'ovs-ofctl add-flow s2 "priority=100,dl_dst={h1_mac},actions=output:1"')
    # ARP flood
    s2.cmd('ovs-ofctl add-flow s2 "priority=1,arp,actions=flood"')

    # === S3 flows (Path B middle switch) ===
    # Traffic going to H2 -> forward to S4
    s3.cmd(f'ovs-ofctl add-flow s3 "priority=100,dl_dst={h2_mac},actions=output:2"')
    # Traffic coming back to H1 -> forward to S1
    s3.cmd(f'ovs-ofctl add-flow s3 "priority=100,dl_dst={h1_mac},actions=output:1"')
    # ARP flood
    s3.cmd('ovs-ofctl add-flow s3 "priority=1,arp,actions=flood"')

    # === S4 flows ===
    # Traffic going to H2 -> forward to H2
    s4.cmd(f'ovs-ofctl add-flow s4 "priority=100,dl_dst={h2_mac},actions=output:3"')
    # Traffic coming back to H1 -> forward to S2
    s4.cmd(f'ovs-ofctl add-flow s4 "priority=100,dl_dst={h1_mac},actions=output:1"')
    # ARP flood
    s4.cmd('ovs-ofctl add-flow s4 "priority=1,arp,actions=flood"')

    info('*** Flow rules installed successfully\n')

def run():
    setLogLevel('info')

    net = Mininet(
        switch=OVSSwitch,
        controller=None,
        link=TCLink,
        autoSetMacs=True
    )

    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')

    info('*** Adding switches\n')
    s1 = net.addSwitch('s1', failMode='standalone')
    s2 = net.addSwitch('s2', failMode='standalone')
    s3 = net.addSwitch('s3', failMode='standalone')
    s4 = net.addSwitch('s4', failMode='standalone')

    info('*** Adding links\n')
    net.addLink(h1, s1)     # h1-eth0 <-> s1-eth1
    net.addLink(s1, s2)     # s1-eth2 <-> s2-eth1
    net.addLink(s1, s3)     # s1-eth3 <-> s3-eth1
    net.addLink(s2, s4)     # s2-eth2 <-> s4-eth1
    net.addLink(s3, s4)     # s3-eth2 <-> s4-eth2
    net.addLink(s4, h2)     # s4-eth3 <-> h2-eth0

    info('*** Starting network\n')
    net.start()

    time.sleep(2)

    # Install flow rules manually
    install_flows(net)

    time.sleep(1)

    info('\n*** Network ready\n')
    info('*** Path A: h1 -> s1 -> s2 -> s4 -> h2\n')
    info('*** Path B: h1 -> s1 -> s3 -> s4 -> h2\n')
    info('*** Type pingall to test connectivity\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
