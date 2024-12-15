# An ML-Augmented HeavyKeeper-Based Fallback Mechanism for Top-K Estimation in Distributed Data Streams

The project simulates a distributed system using the [1998 World Cup Website Access Logs](). It computes the top-k most 
often accessed URLs for each site. Periodically a node is assumed to have failed. In that case, the fallback mechanism 
is called to estimate the top-k based on the top-k of peer nodes and observed correlations between them. 

To reduce computational overhead, we assume that node 0 is the failing node.

## Input
The datastream was preprocessed to retain only the following columns:
```
[Timestamp TimeDiff] URL SiteCode
```
Sample input:
```
[15/Jun/1998:10:53:39 +0000] /images/hm_score_up_line02.gif 1
[15/Jun/1998:10:53:39 +0000] /english/index.html 2
```
Where the site codes are mapped as follows

    Santa Clara 0
    Plano 1
    Herndon 2
    Paris 3

## Pipeline Overview 
The preprocessed logs are parsed line by line in `main.py`. The log line is passed to `stream_forwarder.py` 
where it is attributed to the right `site_processor` based on the code. Each site has an associated `heavy_keeper` instance. 
Once the top-k is ready to be reported it is forwarded to the `NetworkMonitor`. The network monitor trains an instance of 
`FallbackMechanism` and estimates the next top-k in `network_monitor.fallback_mechanism()`. 

## Output
The current setup returns the inferred top-k list and the actual list for comparison. For better visibility and reduced verbosity,
the URLs are returned as an encoded list, but they can be decoded if necessary. 

```
2024-12-15 19:20:15,394 WARNING: Predicted Top-K URLs for Node 0:[[5, 4, 8, 3, 6, 9, 7, 1, 0, 2]]
2024-12-15 19:20:15,396 WARNING: Actual Top-K URLs for Node 0:[[5, 4, 3, 2, 9, 7, 1, 4, 33, 10]]
```
