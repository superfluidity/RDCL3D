define($IP 10.10.0.3);
define($MAC 00:15:17:15:5d:75);

source :: FromDevice(0);
sink   :: ToDevice(0);
// classifies packets
c :: Classifier(
    12/0806 20/0001, // ARP Requests goes to output 0
    12/0806 20/0002, // ARP Replies to output 1
    12/0800, // ICMP Requests to output 2
    -); // without a match to output 3

arpq :: ARPQuerier($IP, $MAC);
arpr :: ARPResponder($IP $MAC);

source -> Print -> c;
c[0] -> ARPPrint -> arpr -> sink;
c[1] -> [1]arpq;
Idle -> [0]arpq;
arpq -> ARPPrint -> sink;
c[2] -> CheckIPHeader(14) -> ICMPPingResponder() -> EtherMirror() -> sink;
c[3] -> Discard;

