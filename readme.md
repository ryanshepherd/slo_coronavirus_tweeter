# About the Project

This is an Azure Function app that sends out daily texts and tweets about coronavirus stats in San Luis Obispo county.

# Architecture

The project kicks off with a timer function, and then daisy-chains to a series of other functions via queues.

Event           | Triggers         | Action 
----------------|------------------|-----------------------------
Timer: at 3:30  | SloPageRetriever | If the page is new: Store the blob. Add a parse-queue item.
parse-queue     | SloPageParser    | Parse the page. Update DB. Add a calc-stats-queue item.
calc-stats-queue| StatsCalculator  | Calculate some stats. Post the results message to text-queue and tweet-queue
tweet-queue     | Tweeter          | Send out the message in a tweet, using the tweepy module.
text-queue      | TextSender       | Text the message to all subscribers, using Twilio.

Additionally, there is a Twilio phone number that people can text in order to subscribe. Twilio forwards the message to an HTTP endpoint that triggers the TextReceiver function.
