//
// sample packets between eth2 and eth1 at 20000 packets per second. send
// sampled packets up to linux device "sampler", created by FromHost.
// This configuration will only run in the kernel (so you must use
// 'click-install sampler.click').
//

elementclass RatedSampler {
// $rate |
  input -> rs1 :: RatedSplitter($rate);
  rs1 [0] -> [0] output;
  rs1 [1] -> t1 :: Tee;
  t1 [0] -> [0] output;
  t1 [1] -> [1] output;
};

elementclass RatedSampler2 {
// $rate |
  input -> rs2 :: RatedSplitter($rate);
  rs2 [0] -> [0] output;
  rs2 [1] -> t2 :: Tee;
  t2 [0] -> [0] output;
  
};


FromHost(sampler, 192.0.2.0/24) -> Discard;

PollDevice(eth2) -> s0 :: RatedSampler(20000);
s0 [0] -> Queue -> ToDevice(eth1);
s0 [1] -> ToHostSniffers(sampler);

PollDevice(eth1) -> s1 :: RatedSampler(20000);
s1 [0] -> Queue -> ToDevice(eth2);
s1 [1] -> ToHostSniffers(sampler);
