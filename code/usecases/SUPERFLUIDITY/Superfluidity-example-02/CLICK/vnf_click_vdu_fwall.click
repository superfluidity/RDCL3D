
fwsource0 :: FromDevice(0);
fwsink0   :: ToDevice(1);
fwsource1 :: FromDevice(1);
fwsink1   :: ToDevice(0);

fwc :: Classifier(
    12/0806, // ARP goes to output 0
    12/0800 15/cc, // IP to output 1, only if QoS == 0xcc
    -); // without a match to output 2

fwsource0 -> fwc;
fwc[0] -> fwsink0;
fwc[1] -> fwsink0;
fwc[2] -> Print -> Discard;

fwsource1 -> Null -> fwsink1;

