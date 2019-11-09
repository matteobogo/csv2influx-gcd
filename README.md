Data is stored separately for each machine in the cluster. One time series per machine is built.
Every time series has a fixed number of sampling intervals of 300 seconds, starting from a Google "genesis" time 
(i.e. 01/02/2011 00:00:00) and covering a month of cluster usage. Each sampling interval contains a mean of the 
resources consumption, the number of tasks and the number of unique jobs running on the machine during the sampling
interval. Data is then aggregated and sent to InfluxDB HTTP API in a JSON format.

Notes:
- BATCH_SIZE: InfluxDB can ingest a batch of points for every http request. The size of the batch can be configured,
but it can not exceed 10k due to InfluxDB limitations. Big sizes can lead to unexpected crashes.

Additional information: 
https://community.influxdata.com/t/what-is-the-highest-performance-method-of-getting-data-in-out-of-influxdb/464/5

- SKIP-FIRST: Useful if we restart the computation and we don't have the previous chunk of unprocessed data.
We need to restart from the previous file that precedes the one where the computation has stopped, because we don't 
have the last chunk of the previous of the previous, we must skip the first interval (assuming it has been already 
computed), otherwise we have inconsistent data for the first interval.

--processing--> ... [file i-1] --split-on-bottom--> [temp_chunk] <--merge-on-top-- [file i] ... --processing-->

temp_chunk contains the last interval of file i-1 and the first interval of file i