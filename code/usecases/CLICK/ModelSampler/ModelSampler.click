//
// sample packets between eth2 and eth1 at 20000 packets per second. send
// sampled packets up to linux device "sampler", created by FromHost.
// This configuration will only run in the kernel (so you must use
// 'click-install sampler.click').
//

elementclass RatedSampler {
// $rate |
  input -> mrs :: RatedSplitter($rate);
  mrs [0] -> mt :: Tee;
  mt [0] -> [0] output;
};

elementclass RatedSampler2 {
// $rate |
  input -> mrs2 :: RatedSplitter($rate);
  mrs2 [1] -> [1] output;
  mrs2 [0] -> mt2 :: Tee;
  mt2 [0] -> ms4 :: RatedSampler(20000);
  ms4 [0] -> [0] output;		  
};

PollDevice(eth2) -> ms1 :: RatedSampler2(20000);
ms1 [0] -> mc ::  Queue -> ToDevice(eth2);
ms1 [1] ->  mc2 :: Queue -> ToDevice(eth2);










