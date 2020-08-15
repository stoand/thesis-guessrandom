# Introduction

## What are RNGs

Random number generators are essential in many types of programs.
Their uses range from security token generation to deciding what random
virtual items will drop in video games. Random number generators (RNGs) are needed
because the silicon circuits at the core of all computers are mostly deterministic by design.

This is a good thing. If this were not the case a program might act differently
when it is being used by an end user then when a programmer created it.

RNGs are an escape hatch from this determinism. They take entropy from some source
and use it to select a value from a given range (there will more on entropy later).

## Why do RNGs need to be secure

RNGs have a wide variety of uses. Some of these uses require an RNG to be secure.
Using an insecure RNG for a use case where a secure one is needed can lead to malicious users
doing something that was not intended.

An RNG can be considered secure if is unfeasable for an attacker to recover the internal 
state of the RNG and thereby predict future random outputs.

One of the most common uses of secure random number generators is the creation of session tokens.

The following scenario describes how an attacker can exploit an insecure RNG for priviledge escalation:

The attacker logs in multiple times quickly in succession. A brute-force algorithm is then run by the
attack to determine what RNG state could have been used to generate the tokens they recieved.
This RNG state allows future session tokens to be calculated by the attacker. Now the attacker
must simply wait for a legitimate user to log in. With the attacker knowing this user's session token,
they are able to use their session as if they logged in as that user.

## Why do RNGs need Entropy to be secure

The key to making RNGs secure is sufficient entropy. Entropy is a measure of what could be called "randomness".

The greater the entropy, the harder it is for a third party to guess the value.

Entropy is highly context-dependant. For example, one might naively assume that reading the current 32-bit unix
time might always generate 32-bits of entropy. This is obviously not the case however if
a server uses the current 32-bit unix time to generate a random seed. Despite the value having a large range (2^32 to be exact),
the attacker can easily reduce the range they need to search.

If the attacker knows that the current unix time was read no more than 500 milliseconds before they recieved the
request the effective entropy is so low that initial value can be trivially guessed.
