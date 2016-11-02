# improveL2cacheTemporalLocality
In this project, I tried to reduce L2 cache trashing by maintaining useful cache blocks for sufficient time to contribute acceptable hits to L2.
As capacity and complexity of on-chip cache memory hierarchy increases, the service cost to the critical loads from Last
Level Cache (LLC), which are frequently repeated, has become a major concern. The processor may stall for a considerable interval
while waiting to access the data stored in the cache blocks in LLC, if there are no independent instructions to execute. To provide
accelerated service to the critical loads requests from LLC, this work concentrates on leveraging the additional capacity offered by
replacing SRAM-based L2 with Spin-Transfer Torque Random Access Memory (STT-MRAM) to accommodate frequently accessed
cache blocks in exclusive read mode in favor of reducing the overall read service time. Our proposed technique improves the temporal
locality while preventing cache thrashing via sufficient accommodation of the frequently read reused fraction of working set that may
exhibit distant re-reference interval in L2. Our experimental results show that the proposed technique can reduce the L2 read miss ratio
by 51.7% on average compared to conventional STT-MRAM L2 design across PARSEC and SPEC2006 workloads while significantly
decreasing the L2 dynamic energy consumption.
