
source0 :: FromDevice(0);
sink0   :: ToDevice(1);
source1 :: FromDevice(1);
sink1   :: ToDevice(0);

// VLANDecapsulator :: StripEtherVLANHeader(-1);
// VLANEncapsulator :: VLANEncap(100);
VLANDecapsulator ::VLANDecap()
VLANEncapsulator ::VLANEncap(100)

//source0 -> VLANDecapsulator -> EnsureEther() -> sink0;
source0 -> VLANDecapsulator -> sink0;
source1 -> VLANEncapsulator -> sink1;

