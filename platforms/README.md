# DevSoc Subcommittee Recruitment: Platforms
Your task is to send a direct message to the matrix handle `@chino:oxn.sh` using the Matrix protocol. However, this message must be sent over a self hosted instance such as through the Conduwuit implementation or the slightly more complicated Synapse implementation .

For this to work your server must be federated, but you do not have to worry about specifics such as using your domain name as your handle (a subdomain will do!) or have other 'nice to have' features. Just a message will do!

**You should write about what you tried and your process in the answer box below.**

If you don't manage to get this working we'll still want to hear about what you tried, what worked and what didn't work, etc. Good luck!

---

> ANSWER BOX
```
    Initially, Platforms was gonna be my first preference, but, even after researching and some trial and error, I didn't end up finishing this task, so I moved it down from my preferences. Here's everything I learnt for this technical assessment (I didn't know anything about hosting or about matrix beforehand).

    I started of with making a subdomain on desec.io, which wasn't too difficult. But I ran into a problem when trying to open ports for matrix. I don't have a router, I'm using my phone as a hotspot device for my laptop and I wasn't exactly able to forward a port. From a bit of research i found that you can do this with a VPS, but because of time constraints, I didn't have the time to learn how to set it up. I also found that you can use a VPN that supports port forwarding, but most of them require a subscription.

    For hosting the server, I was going to use Synapse as it seemed to have the most documentation. Since I don't have linux on my laptop, I'd probably use docker to host matrix. The next step would be to make a config file, run synapse and generate user. And once set up, I think I'd have to use a matrix client like element and I should be able to send a message to the matrix handler.

    Unfortunately, I didn't think I had enough time to do this technical assessment fully so I decided focus on the other ports. 

    One thing I found really interesting about Matrix is that with bridges, you could send messages to any supported third-party platform. Overall, even though I didn't end up finishing this technical assessment, I do think that I am going to try hosting a Matrix homeserver on my own someday in the future.


```