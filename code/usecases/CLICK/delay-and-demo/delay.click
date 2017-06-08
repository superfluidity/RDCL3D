// BandwidthShaper parameters
// 262144 B/s -> 2   Mb/s
// 131072 B/s -> 1   Mb/s
// 16384  B/s -> 128 Kb/s
// 7168   B/s -> 56  Kb/s

pdd1 :: PollDevice(eth1, true)
  -> SetTimestamp
  -> Queue(8)
  -> DelayShaper(10)
  -> BandwidthShaper(131072B/s) // 1Mb
  -> ToDevice(eth2);

pdd2 :: PollDevice(eth2, true)
  -> SetTimestamp
  -> Queue(8)
  -> DelayShaper(10)
  -> BandwidthShaper(131072B/s) // 1Mb
  -> ToDevice(eth1);
