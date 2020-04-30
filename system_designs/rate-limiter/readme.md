# Rate limiter


## What is rate limiter?

A mechanism to protect our service or api from overuse.


## why do we need rate limiting ?

Without rate limiting, a user can call an api as many time as he wants and this
can lead other user in starvation. It helps us from DOS(denial of service), brute
force password attempts, brute force card transaction, to reduce infrastructure
cost, to stop spam.   

There are actually many different ways to enable rate limiting.

### Leaky bucker (token bucket)

This is a basic approach of rate limit via queue. So when a new request comes,
we append it to end of the queue(at regular interval we keep processing the
request from queue in FIFO manner). If queue is full then we will discard
further request.

*** Advantage ***

The advantage of this algorithm is that, it is very easy to implement, process
all the request approximately average rate.

*** Disadvantages ***

burst of traffic can fill up the queue with old request and starve more recent
requests from being processed, It also provides no guarantee that request get
process in fixed amount of time.

And what if rate limit is different for each api, how we will manage different
api then, are we gonna create separate queue for each api ?


### Fixed window algorithm

In this algorithm, a window size of n sec. (for ex. 60 sec) is used to track the
rate. For each incoming request increments the counter for the window. If the
counter exceed the rate then discard the request.


*** Advantages ***

It insure that recent request get processed without being starved by old request.

*** Disadvantages ***

However single burst traffic that occurs near the boundary can result in twice
the rate of requests being processed, because it will allow the request for
both the current and next window.


### Logging

In this algorithm, we keep the logs of each request time and log with timestamp
beyond the threshold are discarded. So whenever new request comes we calculate
the sum of logs to determine the request rate, If the request would exceed the
threshold rate, then it is held.

*** Advantages ***

This will solve the boundary burst problem. It also solve the sudden rush in
request that we faced in fixed window algorithm.

*** Disadvantages ***

It's very expensive to store these much data and also expensive to compute
because we need timestamp sum to decide request processing.


### Sliding window algorithm

It's actually combination of fixed window and Sliding log algorithm

In this algorithm, the time window considered from the time request made plus
window time. Then we calculate how many request are made between that window,
if threshold already reached, then we discard the current request.
