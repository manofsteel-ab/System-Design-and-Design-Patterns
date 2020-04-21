## Abstract factory

Let’s try to understand the concept through an example, assume we want to build
factory which can manufacture computers. There are several types of computers
we would like to build like Laptop, Desktop, Server. So for each type we need a
factory. Having one factory which does all the job may not be a good idea, it
can mess up or slow down the process, rather we can have several sub-factories,
each responsible for manufacturing one type of computer.

Abstract Factory is almost like a Factory Method Design Pattern except the
factory protocol. It is actually abstraction on top of Factory Method Pattern.
