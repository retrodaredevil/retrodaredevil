July 2025 Music Server Brainstorming
========================================


July 15 - Self hosted music server research
------------------------------------------------

Self hosted music server research.

* https://www.reddit.com/r/selfhosted/comments/g4wo4e/experience_with_selfhosted_music_streamers_so_far/

Options

* https://www.subsonic.org/pages/features.jsp

  * Not open source
  * 5 star rating system

* https://www.navidrome.org/docs/overview/

  * 5 star rating system
  * No postgres support https://github.com/navidrome/navidrome/discussions/2820

* https://github.com/epoupon/lms

  * Easy to set up
  * No 5 star rating system in web interface

* https://www.funkwhale.audio/

  * More of a way to share music with your friends. This could supplement one of the other options

* https://github.com/airsonic-advanced/airsonic-advanced

  * A fork of Airsonic, which is a fork of Subsonic.
  * Doesn't look like it's being actively maintained, but it is written in Java
  * From initial looks, codebase is clean

* https://github.com/sentriz/gonic

  * Supports multiple folders. Written in Go. Last release was v0.16.4 in March, 2024
  * tested on `airsonic-refix <https://github.com/tamland/airsonic-refix>`_, `symfonium <https://symfonium.app>`_, `dsub <https://f-droid.org/en/packages/github.daneren2005.dsub/>`_, `jamstash <http://jamstash.com/>`_, `subsonic.el <https://git.sr.ht/~amk/subsonic.el>`_, `sublime music <https://github.com/sublime-music/sublime-music>`_, `soundwaves <https://apps.apple.com/us/app/soundwaves/id736139596>`_, `stmp <https://github.com/wildeyedskies/stmp>`_, `termsonic <https://git.sixfoisneuf.fr/termsonic/>`_, `strawberry <https://www.strawberrymusicplayer.org/>`_, and `ultrasonic <https://gitlab.com/ultrasonic/ultrasonic>`_

I gave LMS a try and it has a nice web interface.
It was simple to add a library, but each library only supports a single root directory.
Maybe that's OK, but I don't think I'll be using this in the long run because there's no 5 star rating system
and it wasn't intuitive to add the currently playing song to a playlist.

Navidrome sounds like it has all the features I want...
Sadly it seems to only support a single music folder: https://github.com/navidrome/navidrome/issues/192
however it looks like that feature is being actively worked on.

I got Navidrome installed.
I like its web interface a lot.
I like that you can download entire albums as zip files.
I like the 5-star rating system.

Clients:

* https://symfonium.app
* https://f-droid.org/en/packages/github.daneren2005.dsub/
* https://github.com/tamland/airsonic-refix - a beautiful web UI
* https://gitlab.com/ultrasonic/ultrasonic

I gave DSub a try.
It seems a little glitchy. No easy way to use the 5-star rating capabilities.
Looks like it has cool caching support, though.
And it has some sort of sync feature, which sounds like it would be great for offline listening.

I gave Ultrasonic a try.
It recognizes that Chat, Shares, Podcasts, Videos, and Jukebox are not supported by Navidrome (or at least its default settings).
It has a "Use five star rating for songs" setting, which is great.
The queue shows "back to" and "up next" in a single view, unlike Plexamp.
I like this.
However, there doesn't seem to be a way to rate a song that is not currently playing.

Let's try out Symfonium...
User rating needs a little customization to get it to be shown while playing.
In Interface > Now playing screens > Expanded player (Portrait) > "Rating Bar Style" to large will give you rating controls.
Rating a song that is not playing takes a few clicks, though.
The UI is beautiful, though. I think I like it more than PlexAmp.
Symfonium also syncs basically all the metadata locally.
This means that searches are near instantaneous.
You can disable half star ratings in the database settings.

Next Steps for Navidrome
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Try out external integrations: https://www.navidrome.org/docs/usage/external-integrations/
* Play with the API to see if I can do things programmatically: https://www.navidrome.org/docs/developers/subsonic-api/
* Try to understand how Navidrome handles deduplication and multiple versions of the same album

Things to try later
^^^^^^^^^^^^^^^^^^^^^^

Funkwhale sounds really cool to set up.

`daphile <https://daphile.com/>`_ sounds like a cool thing to set up in a home.
Multi-zone support! Sounds awesome!


July 17 - My Own Music Server?
---------------------------------

There are so many music servers out there.
There are especially many that implement the Subsonic API.
That means that implementing the Subsonic API shouldn't be that difficult, right?

I know building my own music client would take too much of my free time, but a music server?
That should be easy.

Why would I want to do that?
Well, I'm very particular about managing multiple versions of the same album,
and I especially want my ratings and my playlists to be tied to MusicBrainz Recording IDs, not just files.
To be honest, I'm not exactly sure how something like LMS or Navidrome handle that, but if I had to guess it's probably not exactly what I want.
So... being me... why not make exactly what I want?

Imagine a music server specifically designed to work with music tagged using MusicBrainz IDs.
And also imagine being able to easily manage duplicate tracks and correctly merge them as two recordings get merged in MusicBrainz.
Plus it wouldn't have to tie exactly into MusicBrainz.
There could be some sort of abstraction for that that I would design into the database schema or something.
Imagine a complete history of your rating of a track.
Sometimes when I demote I song from 3 to 2 stars in Plex, I will also add it to a "was once highly rated" playlist.
If we had the history of things being rated, you could also understand when a given song was important to me.
Rather than scrobbling "I listened to this track" to last.fm or Maloja, you could have much deeper insights
into your listening habits.

This software would manage multiple versions of the same album with ease.
Let's say you have the deluxe edition of the album.
Maybe it could also (if you configure it to do so), show the non-deluxe version of the album.
Then you wouldn't have to deal with duplicating that in your file system.
Also, your rating across the same track would sync across all version of an album,
but you should be able to configure which album you prefer for that given recording.
So... when Apple by Charli xcx comes on while shuffling your 3 star playlist, it would show the original brat album,
not the deluxe or the 2CD remix album.

Another thing that's going to be important to me is my ability to transfer my Plex library over and keep statistics
like the instant I modified a rating of a track, and also the first time I added a track to my library.

An advanced feature I would like is the ability to not just make smart playlists,
but make smart stations.
I want the probability of some songs playing to be higher than others.
I believe Symfonium has the idea of "Internet radios".
I'm hoping I would be able to tie into that somehow.
Alternatively I should be able to expose an auto generated playlist through the Subsonic API I would implement,
which might feel a little more janky, but would do the job.

Since this music server manages my playlists and smart playlists,
I should be able to export them into whatever format I would want.
Specifically I should be able to export them as a list of MusicBrainz IDs.
I could also have an integration to create Spotify playlists based off my own playlists.

Maybe I should look into contributing to an existing music server project,
but I really do like the idea of creating my own and making it exactly as I want.
Maybe one day I'll find the time...
