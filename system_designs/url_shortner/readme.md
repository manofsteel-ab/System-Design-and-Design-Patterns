# Designing a URL Shortening service like TinyURL

## why we need URL Shortening?

To create short url.

## Basic Requirements

*** Functional Requirements

- system should be able to generate short and unique url.
- when user access a short link, it should redirect to origin URL
- short url should expire after some default timespan

optional - use should optionally be able to pic custom name for short URL
optional - user can set expire time for short url
optional - Analytics for admin, like shortening rate, how many times redirection
           happened


*** Non-Functional Requirements

-  System should be highly available
-  Redirection should be real time
-  Non guessable short link

# Capacity estimation and constraints( assume 100:1 read/write ratio)

Suppose we are generating 200 new url per second.

so no of reads will be, 100*200/sec = 20K/sec

For storage, let's calculate for 5 years

per sec new_url = 200
so for 1 day = 24*3600 * 200
so for for 1 month = 30*24*3600 * 200
so for 1 year = 12*30*24*3600 * 200
so for 5 years = 5*12*30*24*3600 * 200 = 1800 * 24 * 3600 * 200 = 18*24*36*2* 10^6 = 36*36*24 M(million)

which is around 30K million = 30B(billion)

if we assume each stored record take 500 bytes
then total storage required for 5 years = 30B * 500 bytes = 15000 billion bytes = 15TB
