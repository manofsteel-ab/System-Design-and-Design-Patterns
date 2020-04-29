# Design elevator

Before coding, We need to understand the product/system properly.

To understand the product/system -
- we should know why and where we need this product - Purpose
- who are the users - Product Users
- how users will use this product - User needs

Now, let's talk about why and where we need elevator ?

## Where we need this ?

In multi-floor Buildings. It could be office buildings, residential buildings,
or malls.

Let's take office buildings as examples.

## Why we need this?
We are not superman, obviously we need something to go from one floor to
another or move some items from one floor to another.
One solution is use stairs, but obviously it's very tiring,
gonna take lots of effort and time.
That's why we need elevator to reduce our effort and save times.

## who are the users?

If we talk about office buildings, then users could be employee, boss,
maintenance person etc..

## User needs?

- User want to figure out which lift to take
- User request for the lift
- User gets the lift
- User enter the lift
- User goes up/down
- User gets off the lift
- User need to know which floor lift is on, or in which direction lift is moving


Let's start with small feature


## What are the elements that you can think of about an elevator?

- Elevator controller(control all the events and moves car)
- Car
- Button
  - CarCallButton
  - FloorButton
- Display
  - Position indicator display
  - Direction indicator display
