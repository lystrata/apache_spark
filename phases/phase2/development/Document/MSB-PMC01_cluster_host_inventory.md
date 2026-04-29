root@msb-pmc01-01:~# lscpu; lsblk; lsmem  
Architecture:                x86_64  
  CPU op-mode(s):            32-bit, 64-bit  
  Address sizes:             46 bits physical, 48 bits virtual  
  Byte Order:                Little Endian  
CPU(s):                      24  
  On-line CPU(s) list:       0-23  
Vendor ID:                   GenuineIntel  
  BIOS Vendor ID:            Intel(R) Corporation  
  Model name:                Intel(R) Xeon(R) Gold 6136 CPU @ 3.00GHz  
    BIOS Model name:         Intel(R) Xeon(R) Gold 6136 CPU @ 3.00GHz  CPU @ 3.0GHz  
    BIOS CPU family:         179  
    CPU family:              6  
    Model:                   85  
    Thread(s) per core:      2  
    Core(s) per socket:      12  
    Socket(s):               1  
    Stepping:                4  
    CPU(s) scaling MHz:      62%  
    CPU max MHz:             3700.0000  
    CPU min MHz:             1200.0000  
    BogoMIPS:                6000.00  
    Flags:                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nons  
                             top_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowpref  
                             etch cpuid_fault epb cat_l3 cdp_l3 pti intel_ppin mba tpr_shadow flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm cqm mpx rdt_a avx512f avx512dq rdseed adx smap clflushopt clw  
                             b intel_pt avx512cd avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local dtherm ida arat pln pts hwp hwp_act_window hwp_pkg_req vnmi pku ospke  
Virtualization features:  
  Virtualization:            VT-x  
Caches (sum of all):  
  L1d:                       384 KiB (12 instances)  
  L1i:                       384 KiB (12 instances)  
  L2:                        12 MiB (12 instances)  
  L3:                        24.8 MiB (1 instance)  
NUMA:  
  NUMA node(s):              1  
  NUMA node0 CPU(s):         0-23  
Vulnerabilities:  
  Gather data sampling:      Vulnerable: No microcode  
  Indirect target selection: Not affected  
  Itlb multihit:             KVM: Mitigation: Split huge pages  
  L1tf:                      Mitigation; PTE Inversion; VMX conditional cache flushes, SMT vulnerable  
  Mds:                       Vulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable  
  Meltdown:                  Mitigation; PTI  
  Mmio stale data:           Vulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable  
  Reg file data sampling:    Not affected  
  Retbleed:                  Vulnerable  
  Spec rstack overflow:      Not affected  
  Spec store bypass:         Vulnerable  
  Spectre v1:                Mitigation; usercopy/swapgs barriers and __user pointer sanitization  
  Spectre v2:                Mitigation; Retpolines; STIBP disabled; RSB filling; PBRSB-eIBRS Not affected; BHI Not affected  
  Srbds:                     Not affected  
  Tsa:                       Not affected  
  Tsx async abort:           Vulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable  
  Vmscape:                   Vulnerable  
NAME                                                                                                  MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS  
sda                                                                                                     8:0    0 838.3G  0 disk  
└─ceph--991da689--c5fb--4ed1--86db--40e927a49c4d-osd--block--60fedb1e--a4e8--4a0f--ace6--cdfe94942fea 252:3    0 838.3G  0 lvm  
sdb                                                                                                     8:16   0 838.3G  0 disk  
└─ceph--dcadfd2e--9689--486f--9551--42fa71abc3fb-osd--block--9328091d--8800--4b14--9fb0--291e9766c209 252:4    0 838.3G  0 lvm  
sdc                                                                                                     8:32   0 838.3G  0 disk  
└─ceph--33b5952c--de5d--4fcd--80c1--8f7fef9b883f-osd--block--d2f971a2--82e3--49db--8cf1--5c6743fdafae 252:2    0 838.3G  0 lvm  
sdd                                                                                                     8:48   0   1.1T  0 disk  
└─ceph--1d6de83c--d457--45c6--bc69--c13164c588f7-osd--block--4b54b808--6682--4fa4--b82d--886aa8a0f466 252:5    0   1.1T  0 lvm  
sde                                                                                                     8:64   0 447.1G  0 disk  
├─sde1                                                                                                  8:65   0  1007K  0 part  
├─sde2                                                                                                  8:66   0     1G  0 part  
└─sde3                                                                                                  8:67   0   446G  0 part  
sdf                                                                                                     8:80   0 447.1G  0 disk  
├─sdf1                                                                                                  8:81   0  1007K  0 part  
├─sdf2                                                                                                  8:82   0     1G  0 part  
└─sdf3                                                                                                  8:83   0   446G  0 part  
sdg                                                                                                     8:96   0 894.2G  0 disk  
└─ceph--de234667--c54c--4c6d--aa99--e883a0744a05-osd--block--9fb2d1fb--9c3a--4e66--8d97--6612f40b8962 252:1    0 894.2G  0 lvm  
sdh                                                                                                     8:112  0 894.2G  0 disk  
└─ceph--7edc6613--f3d5--4b7b--b0b4--96706ff94f49-osd--block--be162926--e3aa--4af3--b60e--9e458d23d1b5 252:0    0 894.2G  0 lvm  
sdi                                                                                                     8:128  1     0B  0 disk  
sdj                                                                                                     8:144  0   512M  1 disk  
└─sdj1                                                                                                  8:145  0   511M  1 part  
zd0                                                                                                   230:0    0    50G  0 disk  
├─zd0p1                                                                                               230:1    0  49.9G  0 part  
├─zd0p14                                                                                              230:14   0     4M  0 part  
└─zd0p15                                                                                              230:15   0   106M  0 part  
zd16                                                                                                  230:16   0     4M  0 disk  
rbd0                                                                                                  251:0    0    64G  0 disk  
RANGE                                  SIZE  STATE REMOVABLE BLOCK  
0x0000000000000000-0x000000207fffffff  130G online       yes  0-64  
  
Memory block size:         2G  
Total online memory:     130G  
Total offline memory:      0B  
  
---------------------------------------------------------------------------  
root@msb-pmc01-02:~# lscpu;lsblk;lsmem  
Architecture:                x86_64  
  CPU op-mode(s):            32-bit, 64-bit  
  Address sizes:             46 bits physical, 48 bits virtual  
  Byte Order:                Little Endian  
CPU(s):                      40  
  On-line CPU(s) list:       0-39  
Vendor ID:                   GenuineIntel  
  BIOS Vendor ID:            Intel(R) Corporation  
  Model name:                Intel(R) Xeon(R) Silver 4210R CPU @ 2.40GHz  
    BIOS Model name:         Intel(R) Xeon(R) Silver 4210R CPU @ 2.40GHz  CPU @ 2.4GHz  
    BIOS CPU family:         179  
    CPU family:              6  
    Model:                   85  
    Thread(s) per core:      2  
    Core(s) per socket:      10  
    Socket(s):               2  
    Stepping:                7  
    CPU(s) scaling MHz:      77%  
    CPU max MHz:             3200.0000  
    CPU min MHz:             1000.0000  
    BogoMIPS:                4800.00  
    Flags:                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nons  
                             top_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowpref  
                             etch cpuid_fault epb cat_l3 cdp_l3 intel_ppin ssbd mba ibrs ibpb stibp ibrs_enhanced tpr_shadow flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm mpx rdt_a avx512f avx512dq rdseed  
                             adx smap clflushopt clwb intel_pt avx512cd avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local dtherm ida arat pln pts hwp hwp_act_window hwp_pkg_req vnmi pku ospke avx5  
                             12_vnni md_clear flush_l1d arch_capabilities ibpb_exit_to_user  
Virtualization features:  
  Virtualization:            VT-x  
Caches (sum of all):  
  L1d:                       640 KiB (20 instances)  
  L1i:                       640 KiB (20 instances)  
  L2:                        20 MiB (20 instances)  
  L3:                        27.5 MiB (2 instances)  
NUMA:  
  NUMA node(s):              2  
  NUMA node0 CPU(s):         0-9,20-29  
  NUMA node1 CPU(s):         10-19,30-39  
Vulnerabilities:  
  Gather data sampling:      Vulnerable: No microcode  
  Indirect target selection: Vulnerable  
  Itlb multihit:             KVM: Mitigation: Split huge pages  
  L1tf:                      Not affected  
  Mds:                       Not affected  
  Meltdown:                  Not affected  
  Mmio stale data:           Vulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable  
  Reg file data sampling:    Not affected  
  Retbleed:                  Mitigation; Enhanced IBRS  
  Spec rstack overflow:      Not affected  
  Spec store bypass:         Mitigation; Speculative Store Bypass disabled via prctl  
  Spectre v1:                Mitigation; usercopy/swapgs barriers and __user pointer sanitization  
  Spectre v2:                Mitigation; Enhanced / Automatic IBRS; IBPB conditional; PBRSB-eIBRS SW sequence; BHI SW loop, KVM SW loop  
  Srbds:                     Not affected  
  Tsa:                       Not affected  
  Tsx async abort:           Mitigation; TSX disabled  
  Vmscape:                   Mitigation; IBPB before exit to userspace  
NAME                                                                                                  MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS  
sda                                                                                                     8:0    0 838.3G  0 disk  
└─ceph--e67eaaee--aeb1--4d10--aa58--ba22de631910-osd--block--3681f02c--4c69--4dc8--8ee4--b88c9a818fa2 252:2    0 838.3G  0 lvm  
sdb                                                                                                     8:16   0 838.3G  0 disk  
└─ceph--c1d73168--94da--4393--8de5--a8153263d22c-osd--block--6f651fb4--14d2--4f4d--b419--c03eeb65d7c1 252:4    0 838.3G  0 lvm  
sdc                                                                                                     8:32   0   1.1T  0 disk  
└─ceph--a886b059--4940--4f7f--9571--7da25d238707-osd--block--2359ac1b--84ae--4e3a--819c--1715e2cb655d 252:3    0   1.1T  0 lvm  
sdd                                                                                                     8:48   0   1.1T  0 disk  
└─ceph--99a2f7df--4774--42b9--b251--1bfa6806c6ac-osd--block--6db327b1--a71c--44ad--a50f--819c74db1af3 252:1    0   1.1T  0 lvm  
sde                                                                                                     8:64   0 447.1G  0 disk  
├─sde1                                                                                                  8:65   0  1007K  0 part  
├─sde2                                                                                                  8:66   0     1G  0 part  
└─sde3                                                                                                  8:67   0   446G  0 part  
sdf                                                                                                     8:80   0 447.1G  0 disk  
├─sdf1                                                                                                  8:81   0  1007K  0 part  
├─sdf2                                                                                                  8:82   0     1G  0 part  
└─sdf3                                                                                                  8:83   0   446G  0 part  
sdg                                                                                                     8:96   0 894.2G  0 disk  
└─ceph--aed3a993--c2ee--46b4--b694--c721dfd0411d-osd--block--b6a2cfa2--dd75--4e03--b65c--2e7aedbffff6 252:0    0 894.2G  0 lvm  
sdh                                                                                                     8:112  0 894.2G  0 disk  
└─ceph--76b3c958--f3fb--461f--98d1--9da27b9bb113-osd--block--1ee053dd--d6dc--49b9--b175--2e52ea75f7cf 252:5    0 894.2G  0 lvm  
sdi                                                                                                     8:128  1     0B  0 disk  
rbd0                                                                                                  251:0    0     1T  0 disk  
└─rbd0p1                                                                                              251:1    0  1024G  0 part  
RANGE                                  SIZE  STATE REMOVABLE BLOCK  
0x0000000000000000-0x000000287fffffff  162G online       yes  0-80  
  
Memory block size:         2G  
Total online memory:     162G  
Total offline memory:      0B  
----------------------------------------------------------------------------  
  
  
On Wednesday, April 29, 2026 2:35:51 PM (-06:00), rohn.wood@gmail.com wrote:  
On Wednesday, April 29, 2026 2:35:51 PM (-06:00), rohn.wood@gmail.com wrote:  
  
**Linux msb-pmc01-03 6.8.12-20-pve #1 SMP PREEMPT_DYNAMIC PMX 6.8.12-20 (2026-03-13T08:15Z) x86_64**  
  
**The programs included with the Debian GNU/Linux system are free software;**  
**the exact distribution terms for each program are described in the**  
**individual files in /usr/share/doc/*/copyright.**  
  
**Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent**  
**permitted by applicable law.**  
**Last login: Mon Apr  6 11:04:05 2026**  
**root@msb-pmc01-03:~# lscpu**  
**Architecture:                x86_64**  
**  CPU op-mode(s):            32-bit, 64-bit**  
**  Address sizes:             46 bits physical, 48 bits virtual**  
**  Byte Order:                Little Endian**  
**CPU(s):                      40**  
**  On-line CPU(s) list:       0-39**  
**Vendor ID:                   GenuineIntel**  
**  BIOS Vendor ID:            Intel(R) Corporation**  
**  Model name:                Intel(R) Xeon(R) Silver 4210R CPU @ 2.40GHz**  
**    BIOS Model name:         Intel(R) Xeon(R) Silver 4210R CPU @ 2.40GHz  CPU @ 2.4GHz**  
**    BIOS CPU family:         179**  
**    CPU family:              6**  
**    Model:                   85**  
**    Thread(s) per core:      2**  
**    Core(s) per socket:      10**  
**    Socket(s):               2**  
**    Stepping:                7**  
**    CPU(s) scaling MHz:      52%**  
**    CPU max MHz:             3200.0000**  
**    CPU min MHz:             1000.0000**  
**    BogoMIPS:                4800.00**  
**    Flags:                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nons**  
**                             top_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowpref**  
**                             etch cpuid_fault epb cat_l3 cdp_l3 intel_ppin ssbd mba ibrs ibpb stibp ibrs_enhanced tpr_shadow flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm mpx rdt_a avx512f avx512dq rdseed**  
**                             adx smap clflushopt clwb intel_pt avx512cd avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local dtherm ida arat pln pts hwp hwp_act_window hwp_pkg_req vnmi pku ospke avx5**  
**                             12_vnni md_clear flush_l1d arch_capabilities ibpb_exit_to_user**  
**Virtualization features:**  
**  Virtualization:            VT-x**  
**Caches (sum of all):**  
**  L1d:                       640 KiB (20 instances)**  
**  L1i:                       640 KiB (20 instances)**  
**  L2:                        20 MiB (20 instances)**  
**  L3:                        27.5 MiB (2 instances)**  
**NUMA:**  
**  NUMA node(s):              2**  
**  NUMA node0 CPU(s):         0-9,20-29**  
**  NUMA node1 CPU(s):         10-19,30-39**  
**Vulnerabilities:**  
**  Gather data sampling:      Vulnerable: No microcode**  
**  Indirect target selection: Vulnerable**  
**  Itlb multihit:             KVM: Mitigation: Split huge pages**  
**  L1tf:                      Not affected**  
**  Mds:                       Not affected**  
**  Meltdown:                  Not affected**  
**  Mmio stale data:           Vulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable**  
**  Reg file data sampling:    Not affected**  
**  Retbleed:                  Mitigation; Enhanced IBRS**  
**  Spec rstack overflow:      Not affected**  
**  Spec store bypass:         Mitigation; Speculative Store Bypass disabled via prctl**  
**  Spectre v1:                Mitigation; usercopy/swapgs barriers and __user pointer sanitization**  
**  Spectre v2:                Mitigation; Enhanced / Automatic IBRS; IBPB conditional; PBRSB-eIBRS SW sequence; BHI SW loop, KVM SW loop**  
**  Srbds:                     Not affected**  
**  Tsa:                       Not affected**  
**  Tsx async abort:           Mitigation; TSX disabled**  
**  Vmscape:                   Mitigation; IBPB before exit to userspace**  
Sent with Vivaldi Mail. Download Vivaldi for free at vivaldi.com  
  
------------------------------------------------------------------------------------  
root@msb-pmc01-03:~# lsblk  
root@msb-pmc01-03:~# lsblk  
NAME                                                                                                  MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS  
NAME                                                                                                  MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS  
sda                                                                                                     8:0    0 838.3G  0 disk  
sda                                                                                                     8:0    0 838.3G  0 disk  
└─ceph--b3415bbf--72d8--49d5--a016--0147c6db408c-osd--block--c5815e02--919d--47a6--8060--13bcf97af298 252:4    0 838.3G  0 lvm  
sdb                                                                                                     8:16   0 838.3G  0 disk  
sdb                                                                                                     8:16   0 838.3G  0 disk  
└─ceph--2ab8c87f--a847--44bc--bda5--5fcd27758a76-osd--block--20d32e4a--1867--41c3--a5c3--54e689205b63 252:1    0 838.3G  0 lvm  
└─ceph--2ab8c87f--a847--44bc--bda5--5fcd27758a76-osd--block--20d32e4a--1867--41c3--a5c3--54e689205b63 252:1    0 838.3G  0 lvm  
sdc                                                                                                     8:32   0 838.3G  0 disk  
sdc                                                                                                     8:32   0 838.3G  0 disk  
└─ceph--607010ac--6a58--4ca8--84fb--1c76ace80197-osd--block--45fac88f--849e--4598--a98e--6fa1f78f4a3c 252:3    0 838.3G  0 lvm  
└─ceph--607010ac--6a58--4ca8--84fb--1c76ace80197-osd--block--45fac88f--849e--4598--a98e--6fa1f78f4a3c 252:3    0 838.3G  0 lvm  
sdd                                                                                                     8:48   0   1.1T  0 disk  
└─ceph--d4a908ed--d1e5--4cc9--b9eb--8d2ab1e069c7-osd--block--a9729fc4--c832--40af--a045--a232bd928cf8 252:5    0   1.1T  0 lvm  
└─ceph--d4a908ed--d1e5--4cc9--b9eb--8d2ab1e069c7-osd--block--a9729fc4--c832--40af--a045--a232bd928cf8 252:5    0   1.1T  0 lvm  
sde                                                                                                     8:64   0 447.1G  0 disk  
sde                                                                                                     8:64   0 447.1G  0 disk  
├─sde1                                                                                                  8:65   0  1007K  0 part  
├─sde2                                                                                                  8:66   0     1G  0 part  
├─sde2                                                                                                  8:66   0     1G  0 part  
└─sde3                                                                                                  8:67   0 446.1G  0 part  
sdf                                                                                                     8:80   0 447.1G  0 disk  
sdf                                                                                                     8:80   0 447.1G  0 disk  
├─sdf1                                                                                                  8:81   0  1007K  0 part  
├─sdf1                                                                                                  8:81   0  1007K  0 part  
├─sdf2                                                                                                  8:82   0     1G  0 part  
└─sdf3                                                                                                  8:83   0 446.1G  0 part  
sdg                                                                                                     8:96   0 894.2G  0 disk  
sdg                                                                                                     8:96   0 894.2G  0 disk  
└─ceph--a12382b4--7149--4bd1--a3d0--9e3b896ca38a-osd--block--7d663181--30b9--467b--be03--d88c5426fbe6 252:2    0 894.2G  0 lvm  
└─ceph--a12382b4--7149--4bd1--a3d0--9e3b896ca38a-osd--block--7d663181--30b9--467b--be03--d88c5426fbe6 252:2    0 894.2G  0 lvm  
sdh                                                                                                     8:112  0 894.2G  0 disk  
sdh                                                                                                     8:112  0 894.2G  0 disk  
└─ceph--ca378e97--f39a--4b83--8db6--908697a10e6f-osd--block--f7f9d985--19e4--4bc4--9b96--253ac38756f0 252:0    0 894.2G  0 lvm  
sdi                                                                                                     8:128  1     0B  0 disk  
rbd0                                                                                                  251:0    0     1T  0 disk  
└─rbd0p1                                                                                              251:1    0  1024G  0 part  
└─rbd0p1                                                                                              251:1    0  1024G  0 part  
  
--------------------------------------------------------------------------------------  
--------------------------------------------------------------------------------------  
  
root@msb-pmc01-03:~# lsmem  
RANGE                                  SIZE  STATE REMOVABLE BLOCK  
0x0000000000000000-0x000000287fffffff  162G online       yes  0-80  
0x0000000000000000-0x000000287fffffff  162G online       yes  0-80  
  
Memory block size:         2G  
Memory block size:         2G  
Total online memory:     162G  
Total online memory:     162G  
Total offline memory:      0B  
--------------------------------------------------------------------------------------------  
--------------------------------------------------------------------------------------------  
  
msb-pmc01-04  
  
 lscpu ; lsblk; lsmem  
Architecture:                x86_64  
  CPU op-mode(s):            32-bit, 64-bit  
  Address sizes:             46 bits physical, 48 bits virtual  
  Byte Order:                Little Endian  
CPU(s):                      24  
  On-line CPU(s) list:       0-23  
Vendor ID:                   GenuineIntel  
  BIOS Vendor ID:            Intel(R) Corporation  
  Model name:                Intel(R) Xeon(R) Gold 6136 CPU @ 3.00GHz  
    BIOS Model name:         Intel(R) Xeon(R) Gold 6136 CPU @ 3.00GHz  CPU @ 3.0GHz  
    BIOS CPU family:         179  
    CPU family:              6  
    Model:                   85  
    Thread(s) per core:      2  
    Core(s) per socket:      12  
    Socket(s):               1  
    Stepping:                4  
    CPU(s) scaling MHz:      66%  
    CPU max MHz:             3700.0000  
    CPU min MHz:             1200.0000  
    BogoMIPS:                6000.00  
    Flags:                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nons  
                             top_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowpref  
                             etch cpuid_fault epb cat_l3 cdp_l3 pti intel_ppin mba ibrs ibpb stibp tpr_shadow flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm cqm mpx rdt_a avx512f avx512dq rdseed adx sma  
                             p clflushopt clwb intel_pt avx512cd avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local dtherm ida arat pln pts hwp hwp_act_window hwp_pkg_req vnmi pku ospke ibpb_exit_t  
                             o_user  
Virtualization features:  
  Virtualization:            VT-x  
Caches (sum of all):  
  L1d:                       384 KiB (12 instances)  
  L1i:                       384 KiB (12 instances)  
  L2:                        12 MiB (12 instances)  
  L3:                        24.8 MiB (1 instance)  
NUMA:  
  NUMA node(s):              1  
  NUMA node0 CPU(s):         0-23  
Vulnerabilities:  
  Gather data sampling:      Vulnerable: No microcode  
  Indirect target selection: Not affected  
  Itlb multihit:             KVM: Mitigation: VMX disabled  
  L1tf:                      Mitigation; PTE Inversion; VMX conditional cache flushes, SMT vulnerable  
  Mds:                       Vulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable  
  Meltdown:                  Mitigation; PTI  
  Mmio stale data:           Vulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable  
  Reg file data sampling:    Not affected  
  Retbleed:                  Mitigation; IBRS  
  Spec rstack overflow:      Not affected  
  Spec store bypass:         Vulnerable  
  Spectre v1:                Mitigation; usercopy/swapgs barriers and __user pointer sanitization  
  Spectre v2:                Mitigation; IBRS; IBPB conditional; STIBP conditional; RSB filling; PBRSB-eIBRS Not affected; BHI Not affected  
  Srbds:                     Not affected  
  Tsa:                       Not affected  
  Tsx async abort:           Vulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable  
  Vmscape:                   Mitigation; IBPB before exit to userspace  
NAME                                                                                                  MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS  
sda                                                                                                     8:0    0 447.1G  0 disk  
├─sda1                                                                                                  8:1    0  1007K  0 part  
├─sda2                                                                                                  8:2    0     1G  0 part  
└─sda3                                                                                                  8:3    0 446.1G  0 part  
sdb                                                                                                     8:16   0 447.1G  0 disk  
├─sdb1                                                                                                  8:17   0  1007K  0 part  
├─sdb2                                                                                                  8:18   0     1G  0 part  
└─sdb3                                                                                                  8:19   0 446.1G  0 part  
sdc                                                                                                     8:32   0 894.3G  0 disk  
└─ceph--df994241--b23d--45b1--94e6--5b4ac3421ae6-osd--block--cd1a3831--ad00--4a2e--859f--86521172a3a0 252:1    0 894.3G  0 lvm  
sdd                                                                                                     8:48   0 894.3G  0 disk  
└─ceph--d32b44dc--f005--4447--ba0a--05f0668678e1-osd--block--972c84b0--8977--4baf--9a6b--6032fb18298e 252:0    0 894.3G  0 lvm  
sde                                                                                                     8:64   0 838.4G  0 disk  
└─ceph--519385c5--1fd3--425c--8345--1958abce9931-osd--block--51149ff8--14c2--4c14--b9ea--39fc0e1cbf8f 252:4    0 838.4G  0 lvm  
sdf                                                                                                     8:80   0 838.4G  0 disk  
└─ceph--d03e8525--6398--4c3a--a61a--b62dc0346cfd-osd--block--bd08fd97--6837--4ee1--a137--acfbcfa958d2 252:3    0 838.4G  0 lvm  
sdg                                                                                                     8:96   0 838.4G  0 disk  
└─ceph--b4cfe60b--9b28--4472--b540--825c628386ff-osd--block--966718e4--d1d8--4915--9676--6aab553d1d4b 252:2    0 838.4G  0 lvm  
sdh                                                                                                     8:112  0   1.1T  0 disk  
└─ceph--46ab9f06--7484--4ea7--a5b0--5a3e35f82ad5-osd--block--3d2571c8--ba13--4d5c--9475--83cda640cee4 252:5    0   1.1T  0 lvm  
sdi                                                                                                     8:128  1     0B  0 disk  
sdj                                                                                                     8:144  0   512M  1 disk  
└─sdj1                                                                                                  8:145  0   511M  1 part  
zd0                                                                                                   230:0    0    64G  0 disk  
├─zd0p1                                                                                               230:1    0     1M  0 part  
├─zd0p2                                                                                               230:2    0     1G  0 part  
└─zd0p3                                                                                               230:3    0    63G  0 part  
RANGE                                  SIZE  STATE REMOVABLE BLOCK  
0x0000000000000000-0x000000207fffffff  130G online       yes  0-64  
  
Memory block size:         2G  
Total online memory:     130G  
Total offline memory:      0B  
  
  
  
  
--   
Sent with Vivaldi Mail. Download Vivaldi for free at vivaldi.com  
