# About the name #

PyMei is obviously a pun on [Pai Mei](http://en.wikipedia.org/wiki/Pai_Mei) from [Kill Bill](http://en.wikipedia.org/wiki/Kill_Bill), but it's a short form of `Python Media Interface`.

It's original name was mediaSystem-ng, since it was the second iteration of my homebrew mediaSystem software (first iteration was in Ruby, and a mess).

# About the origins #

PyMei started as a quick hack to browse files and play them, using SDL. The reason I started developing PyMei was that I had grown tired of all _almost-fits_ solutions I found, like [MythTV](http://www.mythtv.org/) - which was very centric towards watching TV and [GeeXbox](http://geexbox.org) - which was very limited since it was basically a linux-distro with a menu implemented inside mplayer (!).
I recall trying others, but not being completely satisfied, and finally I threw together a diskless (NFS-booted) Ubuntu-box to serve as my HTPC. When this was up and running, I realized I needed something more [LIRC](http://www.lirc.org)-friendly - because using a mouse was a hassle.

I sat down and wrote mediaSystem, which was a simple Ruby/SDL-program to browse video-files, and play them with mplayer. After two years of usage and incremental development, mediaSystem became a spaghetti-monster, figuratively speaking, and very unmaintainable.

After this realization, I started writing mediaSystem-ng in Python, using PyGame, applying the experience I had gained from writing mediaSystem in a very ad-hoc fashion. When this started growing, I tried to keep some reins on the beast, and keep the design consistent and manageable.

After a time of development and usage at home, I decided to try to publish it to the world - perhaps someone else could make use of it. I threw together a plugin-system and theme support, got a friend to design a webpage, wrote some docs, renamed it to PyMei and ta-daa! Here it is!

I hope you like it, and decide to contribute - I really want someone elses view on all this.