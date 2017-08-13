// decapsulate on one direction
FromDevice(0) -> VLANDecap() -> ToDevice(1);

// encapsulate in the other direction
FromDevice(1) -> VLANEncap(100) -> ToDevice(0);

