# An ML-Augmented HeavyKeeper-Based Fallback Mechanism for Top-K Estimation in Distributed Data Streams

The project simulates a distributed system using the [1998 World Cup Website Access Logs](http://ita.ee.lbl.gov/html/contrib/WorldCup.html). It computes the top-k most 
often accessed URLs for each site. Periodically a node is assumed to have failed. In that case, the fallback mechanism 
is called to estimate the top-k based on the top-k of peer nodes and observed correlations between them. 

To reduce computational overhead, we assume that node 0 is the periodically failing node.

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
The preprocessed logs are parsed line by line in `main.py`. The log line is passed to `StreamForwarder` 
where it is attributed to the right `SiteProcessor` based on the code. Each site has an associated `HeavyKeeper` instance, that computes the top-k. 
Once the top-k is ready to be reported, it is forwarded to the `NetworkMonitor`. The network monitor trains an instance of 
`FallbackMechanism` and returns the most recent top-k estimate when requested with `network_monitor.fallback_mechanism()`. 

## Output
The current setup returns the inferred top-k list and the actual list for comparison. For better visibility and reduced verbosity,
the URLs are returned as an encoded list, but can be decoded if necessary. 
Additionally, the predicted top-k is evaluated and the F1, positional, and NDCG scores are returned. 

```
2024-12-15 22:29:27,175 WARNING: Simulated Node Failure!!!
2024-12-15 22:29:27,175 WARNING: Predicted Top-K URLs for Node 0:[4, 3, 5, 2, 0, 1]
2024-12-15 22:29:27,176 WARNING: Actual Top-K URLs for Node 0:[1, 3, 2, 23, 13, 5]
2024-12-15 22:29:27,176 WARNING: Estimation scores: 
   F1 - 0.66667; 
   Positional - 0.31944; 
   NDCG - 0.58033
```
