
source0 :: FromDevice(0);
sink0   :: ToDevice(1);
source1 :: FromDevice(1);
sink1   :: ToDevice(0);

vlandecapsulator :: VLANDecap();
vlanencapsulator :: VLANEncap(100);

source0 -> vlandecapsulator -> sink0;
source1 -> vlanencapsulator -> sink1;

