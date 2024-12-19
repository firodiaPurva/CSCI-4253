|     Method        |   Local   |  Same-Zone   |  Different Region   |
|-------------------|-----------|--------------|---------------------|
|   REST add        | 2.1501 ms | 2.5016 ms    | 295.5087 ms         |
|   gRPC add        | 0.0707 ms | 0.0830 ms    | 14.5388 ms          |
|   REST rawimg     | 4.2392 ms | 6.0803 ms    | 1193.3485 ms        |
|   gRPC rawimg     | 0.7897 ms | 0.8937 ms    | 19.7601 ms          |
|   REST dotproduct | 2.7758 ms | 3.1286 ms    | 296.9792 ms         |
|   gRPC dotproduct | 0.0913 ms | 0.1001 ms    | 14.5381 ms          |
|   REST jsonimg    | 38.3464 ms| 41.4534 ms   | 1339.5616 ms        |
|   gRPC jsonimg    | 2.1223 ms | 2.7828 ms    | 22.3624 ms          |
|   PING            | 0.046 ms  | 1.041 ms     | 141.902 ms          |


***Ping***

The biggest difference in latency comes from the difference regions(US to Europe).

***Local (No Network Latency)***

REST: REST shows considerably higher latency than gRPC for all operations. This is largely due to REST's overhead of creating a new TCP connection for each operation, even in a local setup where network latency is negligible.

gRPC: gRPC outperforms REST by orders of magnitude, as it uses a persistent TCP connection to minimize connection setup costs.

In local setups, Python and processing overhead seem to dominate REST's execution time.

***Same Zone (Low Network Latency)***

REST: Although the same-zone network adds minimal latency (~0.45ms in ping), REST's overhead remains significant due to its repeated connection establishment for each API call.

gRPC: Despite the small network latency, gRPC continues to deliver low-latency performance by maintaining a single, persistent TCP connection.

Overall, the network latency in the same zone is small but still exacerbates REST’s inefficiency compared to gRPC.

***Different Region(Europe)***

REST: In the different-region setup, the impact of network latency becomes extremely pronounced. The ping time of 142ms significantly adds to REST's already high overhead, resulting in much higher latency (e.g., REST add takes ~296ms).

gRPC: gRPC still performs remarkably well, keeping the overhead extremely low (e.g., gRPC add takes only 0.143 ms), despite the large network latency. The single TCP connection helps gRPC avoid the repetitive overhead of creating new connections, a major advantage in cross-region scenarios.

Network Latency: The difference in performance between REST and gRPC is most visible in high-latency scenarios, with REST taking several hundred milliseconds longer than gRPC due to the new TCP connection for every request.

***Summary of Observations:***

Local: gRPC drastically outperforms REST in a local setup due to lower overhead. REST suffers from its repeated connection establishment, even with negligible network latency.

Same-Zone: In environments where both server and client are in the same zone, REST’s overhead persists, while gRPC continues to maintain low latency thanks to its persistent connection. The difference is relatively smaller but still significant.

Different-Region: The performance difference between REST and gRPC is most extreme when the server and client are in different regions. Network latency compounds REST’s overhead due to the establishment of new TCP connections for each request, while gRPC maintains much better performance with a persistent connection, minimizing the impact of network delay.

***In conclusion, gRPC provides a massive performance advantage over REST, particularly when network latency increases. overall results support the use of gRPC for faster performing web services.***
