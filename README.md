# kopi-meets-donut-bot
LifeHack Submission, @KopiMeetsDonutBot

Done by Justine Koh, Samantha Wong, Woo Bo Tuan and Tay Weida

Try it at @KopiMeetsDonutBot!

Video Demonstration: 

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/gSMkludM2vI/0.jpg)](https://www.youtube.com/watch?v=gSMkludM2vI)

Base Logic Flow:

![kopimeetsdonuts](https://user-images.githubusercontent.com/70256674/126865130-2bceda17-c08f-4d85-b71b-487ddc386b25.png)

## Inspiration
Lonely during COVID-19 Times? Very bored staying at home and no one to chat up with during Heightened Alert Phase 2? Or have no friends jio-ing you out of the house to makan when its 2 pax dine-in?

Fret no more! With our telegram bot, it provides a quick and easy way for users to connect to potential partners, and thus be able to hang out amidst COVID-19 measures.

Kopi Meets Donut (which is totally not inspired by Coffee Meets Bagel) allows matching and anonymous chatting with such partners!

## What it does
It allows you to add your bio and has a simple algorithm that matches you to your preferred partner type. This enables a quick and fuss-free way to choose your partner. Once you register your profile, you can go and match a donut! The matching of Donuts uses a simple algorithm to find your preferred partner and displays their bio and name. You can then click on their name to select their profile and send a request to them. The other user has to press /accept to start a private chat with them through the bot, or /reject if they are not interested. If you are tired of talking to them, type /cancel and then /start again so you can re-edit your bio or simply try to match with a new person!

## How we built it
We built it using python and MongoDB as the backend, storing the users bio and their personal details online. This way we can access and display the content to the next user when they are attempting to match to others. We used codewithme to collaborate on the single main.py script and split work amongst ourselves to ensure the bot was able to function well and on time.

## Challenges we ran into
Due to time constraints, we were unable to implement a timeout function that times out the request after 1hr (we wanted a quick way for users to keep matching with new people). Moreover, as all of us had no background in making a telegram bot, it was a very tough climb and our lack of experience really slowed us down in the first 12 hours of the Hackathon. However, we did pull through and self-learn everything within these 24 hours.

## Accomplishments that we're proud of
Despite not having any experience in making a telegram bot, we have achieved a user-friendly telegram bot that allows anonymous chat simultaneously through the bot, as well as the use of a database to store their personal details and finally producing an algorithm that could pair people up with their preferences in less than 24 hours.

## What we learned
We learned that we should really learn these things before the Hackathon and not during... Other than that it was very fun and enjoyable when we managed to crack the anonymous chat functions at 5/6am and were ecstatic.

## What's next for Kopi Meets Donuts
Coffee meets bagel?
