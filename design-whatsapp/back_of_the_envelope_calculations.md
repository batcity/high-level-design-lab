# Storage:

If there's 2B monthly active users

they have two types of content that need to be stored

1. actual messages - plaintext
2. media (photographs, images, gifs, documents etc)


## Messages:

Now on average im going to assume each user sends about 300 new messages a month (10 new messages a day)

and im going to assume each message has about 50 words or 300 characters

so every month they'd be adding

300 messages * 300 characters = 90000 characters to the system

An ASCII character in UTF-8 is 8 bits (1 byte)

so 90000 characters would equate to 90000 bytes -> 0.1 megabyte

so 0.1 * 2B = 200 TB of messages get added every month

so I'd need to add 200 TB of storage to the system every month either by purchasing cloud storage or actual server racks

Note: I made the mistake of assuming that we'd only be storing the messages once which is terribe for durability

I also missed out on metadata on the messages so that would add storage as well





