# Designing a URL Shortening service like TinyURL

## why we need URL Shortening?

To create short url.

## Basic Requirements

***Functional Requirements***
- user > registered/anonymous
- system should be able to generate short and unique url.
- when user access a short link, it should redirect to original URL
- short url should expire after some default timespan

optional - user should optionally be able to pic custom name for short URL
optional - user can set expire time for short url
optional - Analytics for admin, like shortening rate, how many times redirection
           happened


***Non-Functional Requirements***

-  System should be highly available
-  Redirection should be real time
-  Non guessable short link


## Capacity estimation and constraints

Because system will be read heavy. Let's assume 100:1 will be the read/write ratio.

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

## what kind of database we should use ?

Since we anticipating a large amount of data and we do not need to use any
relationship between objects, so we can use a NoSQL store like dynmodb.


## Database design

shorturls:

 - original_url
 - short_code (Key)
 - expires_at - datetime
 - created_at - datetime


## API design

shorter/api/v1/urls/ [POST] - To create short_link

{original_url = ""}

shorter/api/v1/urls/short_link="abc"  [GET] TO fetch original url

shorter/api/v1/urls/{short_code} [DELETE]  To delete mappings



## Shortening algorithm (Let's Assume we want to generate 7 char long short code)

Let's explore few solution

***Encoding actual URL - Using MD5 hash function***

In this approach, we pass our original url to md5 hash function(Ex. md5),
that generate 128 bit hash value.

```
Python
from _md5 import md5
original_url = "https://www.youtube.com/watch?v=JQDHz72OA3c"
md5_hash = md5(original_url.encode('utf-8')).hexdigest()
```

But there is problem, that md5 generate very lengthy output, so we have to take
only 7 character from hash value.

But taking seven character from hash value for short code, can cause lots of
collision.So we might end up getting same short code for different urls.

So we have to validate that if the short code is already present in db or not.
But if we do this, it will increase the response time and for huge no of request
it is not scalable.


***Using Base62 conversion***

In this approach, we pass a decimal number to Base62 hash function, and it generate a base 62 encoded string.

Now the question is why base 62 ? why not base 10?

Ans - if we want 7 char long string, then using base 62 we can get trillion possibilities
while with base 10 we will get only some million possibilities.


```
Python

def base62_encoding(num):
    ALPHABETS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if num == 0:
      return ALPHABETS[0]

    encoded_hash = ""

    while num>0:
      remainder = num%62
      encoded_hash += ALPHABETS[remainder]
      num = num//62
    return encoded_hash[::-1]

```

Now the problem with this approach, how do we get decimal number?

- Use random number, but it could also cause collision, and it will not work on scale.
- Use counter - This will avoid the collision but having single counter is not scalable.
Because we could have multiple app server, and each server is requesting a number from the counter
, so will increase the load on counter service and it is also a SPF(single point failure).

- Now let have multiple counter server, each server is having their own range of counting.

for example we have c1 (1-100M) c2(1001M to 200M)....
Now the problem with this is, what will happen if a counter reaches its limit, how
we gonna reset the counter?

So basically we need extra service, who has the information about counters and
responsible for resetting the counter(allocating new range).

Now, how will we manage if user provide his custom short code ?
Think about it.

- Use KGS (key generation service) - Generate hash code before hand and store them in db(key-val).

KGS will make sure all the keys inserted into key-DB are unique.

**Can concurrency cause problems ?**

What if multiple app server is trying to access the keys concurrently ? In this
case we might end up with same key for more than two request.

To solve this problem, server can user KGS to read/mark keys in the database.
It can use two table to store the keys. One for not used code and one for used code.

As soon as KGS gives key to a server, it can move them to used_keys table.

KGS can always keep some keys in memory to full fill the request faster.

**Isn’t KGS a single point of failure?**
Yes, It is. But we can have multiple replicas, so when primary server goes down, the standby server can take over.

**Can each app server cache some keys from key-DB?**
Yes, we can but if server goes down, we will lose those keys.
