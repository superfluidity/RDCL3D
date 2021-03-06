//ip64-nat.click
//router and translator: mindwipe
//00:a0:c9:9c:fd:9e, 18.26.4.116, 3ffe:1ce1:2:0:200::1, fe80::2a0:c9ff:fe9c:fd9e
// 6-only node: frenulum ::ffff:0.0.0.2 (mapped 4 address: 1.0.0.1)
// 4-only node: grunt: 18.26.4.125 (test for ping, telnet, finger)
// 4-only node: pdos: 18.26.4.9 (test for http) (amsterdam)
// grunt can ping 1.0.0.1
// frenulum can ping6 ::18.26.4.125
	
//grunt: route delete 1.0.0.1
//grunt: route add 1.0.0.1 18.26.4.116

//mindwipe: in click/userlevel directory:
//mindwipe: ./click ../conf/ip64-nat.click

//frenulum: route delete -inet6 ::18.26.4.125 or route flush -inet6
//frenulum: route add -inet6 ::18.26.4.125 3ffe:1ce1:2:0:200::1

arp::ARPQuerier(18.26.4.116, 00:a0:c9:9c:fd:9e);
arr::ARPResponder(18.26.4.116 00:a0:c9:9c:fd:9e);

nda :: IP6NDAdvertiser(
	3ffe:1ce1:2:0:200::1/128 00:A0:C9:9C:FD:9E, 
	fe80::2a0:c9ff:fe9c:fd9e/128 00:A0:C9:9C:FD:9E); 

nds :: IP6NDSolicitor(
	fe80::2a0:c9ff:fe9c:fd9e, 00:A0:C9:9C:FD:9E);

ip64c :: Classifier(
	12/86dd 20/3aff 54/87,
	12/86dd 20/3aff 54/88,		 
	12/86dd,
	12/0806 20/0001,
	12/0806 20/0002,		
	12/0800 30/01000001,
	-);

rt :: StaticIPLookup(

	18.26.4.116/32 0,
	18.26.4.255/32 0,
	18.26.4.0/32 0,
	18.26.4.125/32 18.26.4.125 1,
	18.26.4.9/32 18.26.4.9 1,
	1.0.0.1/32 1.0.0.1 2,
	18.26.7.0/24 3,
	0.0.0.0/0 18.26.4.1 3);

rt6 :: LookupIP6Route(
	3ffe:1ce1:2::2/128 ::0 0,
	3ffe:1ce1:2:0:200::1/128 ::0 0,
	::ffff:0.0.0.2/128 ::ffff:0.0.0.2 1,
	3ffe:1ce1:2::/80 ::0 2,
	3ffe:1ce1:2:0:200::/80 ::0 2,
	::0/96 ::0 3,
  	::0/0 ::c0a8:1 4);

//at :: AddressTranslator(
//	1,
//	0,
//	::ffff:0.0.0.2 ::1.0.0.1,
//	1,
//	1,
//	0,
//	::ffff:18.26.4.116 1300 1310);

//at :: AddressTranslator(
//	1,
//	0,
//	::ffff:0.0.0.2 ::1.0.0.1,
//	0);

at :: AddressTranslator(
	0,
	1,
	0,
	0,
	::1.0.0.1);


pt64 :: ProtocolTranslator64();
pt46 :: ProtocolTranslator46();	

FromDevice(eth0, 1)
  	-> ip64c;
to_eth0 :: ToDevice(eth0);

ip64c[0] 	-> nda
	//-> Print(nda, 200)
	-> Queue(1024)
	-> to_eth0;
ip64c[1] 	-> [1]nds;
ip64c[2]	//-> Print(before-Strip, 200) 
	-> Strip(14)
	-> CheckIP6Header(3ffe:1ce1:2:0:200::ffff 3ffe:1ce1:2::ffff)
	-> GetIP6Address(24)
	//-> Print(before-rout6, 200) 
	-> rt6;

ip64c[3] 	//-> Print(arr, 200) 
	-> arr	
	-> Queue(1024)
	-> to_eth0;
	
ip64c[4] 	//-> Print(arp-reply, 200) 
	->[1]arp;
	
ip64c[5] 	//-> Print(c5-normal-ip-pkt, 200) 
	-> Strip(14)
	-> CheckIPHeader(BADSRC 18.26.4.255)
	-> GetIPAddress(16)
	-> rt;

ip64c[6]	//-> Print(c6-normal-ip-pkt, 200) 
	->Discard;

rt[0]	->Print(rt0, 200) ->Discard;
rt[1]	//->Print(rt1, 200)
	-> DropBroadcasts
      	-> dt1 :: DecIPTTL
      	-> fr1 :: IPFragmenter(300)
	//->Discard;
	//-> Print(before-arp0, 200) 
	->[0]arp;
rt[2]	//->Print(rt2, 200) 
	->[0]pt46;
rt[3]	->Print(rt3, 200) ->Discard;	
	
rt6[0] 	-> Print(route60-ok, 200) -> Discard;
rt6[1] 	//-> Print(route61-ok, 200) 
	-> dh1:: DecIP6HLIM-> [0]nds;
rt6[2] 	-> dh2:: DecIP6HLIM 
	-> Print(route62-ok, 200)  -> Discard;
rt6[3] 	//-> Print(route63-ok, 200) 
	-> [0]at;	
rt6[4] 	-> Print(route64-ok, 200) -> Discard;

dh1[1]	-> ICMP6Error(3ffe:1ce1:2:0:200::1, 3, 0)
	-> Discard;
dh2[1]	-> ICMP6Error(3ffe:1ce1:2:0:200::1, 3, 0)
	-> Discard;
at[0]  	//-> Print(after-at0, 200) 
	-> [0]pt64;
at[1]  	-> Print(after-at1, 200) 
	-> CheckIP6Header()
	-> GetIP6Address(24)
	-> [0]rt6;
	
pt64[0] //-> Print(after-pt640, 200) 
	-> CheckIPHeader(BADSRC 18.26.4.255 1.255.255.255)
	-> GetIPAddress(16)
	-> [0]rt;
pt46[0]	-> Print(after-pt460, 200) 
	-> [1]at;

arp[0] 	-> Print(arp0, 200)
	-> to_eth0;

nds[0]  //-> Print(nds, 200)
	-> to_eth0;
	
	







