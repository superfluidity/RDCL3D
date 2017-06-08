
source0 :: FromDevice(0);
sink0   :: ToDevice(1);
source1 :: FromDevice(1);
sink1   :: ToDevice(0);

c :: Classifier(
    12/0806, // ARP goes to output 0
    12/0800 15/cc, // IP to output 1, only if QoS == 0xcc
    -); // without a match to output 2

source0 -> c;
c[0] -> sink0;
c[1] -> sink0;
c[2] -> Print -> Discard;

source1 -> Null -> sink1;

