// Suck stuff in.
PollDevice(eth7) -> c0demo :: Classifier(12/0806 20/0001,
                                     12/0806 20/0002,
                                     12/0800,
                                     -);

out :: Queue(1024) -> ToDevice(eth4);

// ARP request need to be answered, obviously
c0demo[0]
    -> ARPResponder(7.0.0.1 00:C0:95:E1:FC:D6)
    -> out;

// ARP responses are handed to Linux
c0demo[1]
    -> ToHost();

// Non-IP packets are dropped
c0demo[3]
    -> Discard;

// Other IP packets. Split on UDP, TCP and rest
c0demo[2]
    -> Strip(14)
    -> CheckIPHeader()
    -> c1demo :: Classifier(9/17, 9/6, -);


// TCP packets
c1demo[1] -> Print(TCP) -> out;

// UDP packets
c1demo[0]
    -> Print(UDP)
    -> udp_mon :: IPRateMonitor(DST, PACKETS, 0, 10, 30)
    -> udp_block :: Block(20)
    -> out;

// non-UDP and non-TCP packets
c1demo[2] -> Print(UNKNOWN) -> out;
