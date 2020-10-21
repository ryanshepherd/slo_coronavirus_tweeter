# About the Project

This is an Azure Function app that sends out daily texts and tweets about coronavirus stats in San Luis Obispo county.

# Architecture

The project kicks off with a timer function, and then daisy-chains to a series of other functions via queues. It could easily be done with a single script on a timer, but it was also an opportunity for me to explore Azure functions.

An alternative to the daisy chain architecture could be to use durable functions to enable one "orchestrator" function that calls the others.

Event           | Triggers         | Action 
----------------|------------------|-----------------------------
Timer: at 3:30  | SloPageRetriever | If the page is new: Store the blob. Add a parse-queue item.
parse-queue     | SloPageParser    | Parse the page. Update DB. Add a calc-stats-queue item.
calc-stats-queue| StatsCalculator  | Calculate some stats. Post the results message to text-queue and tweet-queue
tweet-queue     | Tweeter          | Send out the message in a tweet, using the tweepy module.
text-queue      | TextSender       | Text the message to all subscribers, using Twilio.

Additionally, I have a Twilio phone number for receiving texts, which forwards the message on to the HTTP endpoint that triggers the TextReceiver function.