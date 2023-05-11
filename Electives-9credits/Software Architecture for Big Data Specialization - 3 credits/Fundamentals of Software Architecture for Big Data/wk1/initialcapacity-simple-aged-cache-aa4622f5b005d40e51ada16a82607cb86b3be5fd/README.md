# Simple aged cache

An exercise to help individuals new to modern software engineering practices understand the basics of
 test driven development.

## Background

The simple aged cache was one of the first bits of code that I paired on in the early 2000s while working at a
 telecommunications company. Ever since, I've been a fan of test driven development and pair programming.

Over the years that followed, I've attempted to introduce variations of the cache as part of the interview process
 at several companies. Most early attempts were fairly unsuccessful.

While working at Gnip in 2009, the team heard about the now infamous Pivotal pairing interview.
In response, we began interviewing candidates using a linked list. Which, as you may know, isn’t too far from
 implementing a cache. Unfortunately, the linked list also proved challenging mainly because we asked candidates
  to do all the typing.

In response, we introduced the simple aged cache as a whiteboard problem rather than as a live coding exercise. The move
 to a whiteboard was very successful, resulting in several new hires who ultimately led to Gnip’s success.
  Rumor has it, the simple aged cache is still used as part of Twitter's technical interview after the Twitter
   acquisition of Gnip.

### The exercise

Fast-forward to today, the simple aged cache presented here combines both whiteboard and coding approaches.

The exercise - get the tests to pass!

- Explore using an inner class `ExpirableEntry`
- Try not using built in collection classes; Lists, Maps, or Sets.
- Try both Java and Kotlin examples.

```java
package io.collective;

import java.time.Clock;

public class SimpleAgedCache {

    public SimpleAgedCache(Clock clock) {
    }

    public SimpleAgedCache() {
    }

    public void put(Object key, Object value, int retentionInMillis) {
    }

    public boolean isEmpty() {
        return false;
    }

    public int size() {
        return 0;
    }

    public Object get(Object key) {
        return null;
    }
}
```
Hope you enjoy the exercise!

Thanks, @barinek

© 2021 by Initial Capacity, Inc. All rights reserved.

