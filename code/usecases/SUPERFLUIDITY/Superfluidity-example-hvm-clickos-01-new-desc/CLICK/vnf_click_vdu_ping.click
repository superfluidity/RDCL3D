define($IP 10.10.0.3);
define($MAC 00:15:17:15:5d:75);

pingsource :: FromDevice(0);
pingsink   :: ToDevice(0);
// classifies packets
pingc :: Classifier(
    12/0806 20/0001, // ARP Requests goes to output 0
    12/0806 20/0002, // ARP Replies to output 1
    12/0800, // ICMP Requests to output 2
    -); // without a match to output 3

arpq :: ARPQuerier($IP, $MAC);
arpr :: ARPResponder($IP $MAC);

pingsource -> Print -> pingc;
pingc[0] -> ARPPrint -> arpr -> pingsink;
pingc[1] -> [1]arpq;
Idle -> [0]arpq;
arpq -> ARPPrint -> pingsink;
pingc[2] -> CheckIPHeader(14) -> ICMPPingResponder() -> EtherMirror() -> pingsink;
pingc[3] -> Discard;

