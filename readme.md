# The Project
This is an Azure Function app that sends out daily texts and tweets about coronavirus stats in San Luis Obispo county. Check out the feed: [@SloCovidTracker](https://twitter.com/SloCovidTracker).

# The Data
Data is scraped from the Emergency SLO website daily. You can view the full history of scraped statistics on this [Google Sheet](https://docs.google.com/spreadsheets/d/1v-iCXfgCTIVd7BcFFJwBY4P3oye3mvqpr4PbWxlk6KE)

I added a new stat for tracking vaccinations (whoo!) on Jan 13, 2021. This stat comes from the [CDC](https://covid.cdc.gov/covid-data-tracker/#vaccinations) and represents the percent of California's population who have received *both* vaccinations.

A Test Positivity statistic was previously included in the tweets, but it dropped off the county dashboard sometime in Dec 2020. This information is still available from [the state](https://covid19.ca.gov/state-dashboard/).


# The Code
The project kicks off with a timer function, and then daisy-chains to a series of other functions via queues.

Event           | Triggers         | Action 
----------------|------------------|-----------------------------
Timer: at 3:30  | SloPageRetriever | If the page is new: Store the blob. Add a parse-queue item.
parse-queue     | SloPageParser    | Parse the page. Update DB. Add a calc-stats-queue item.
calc-stats-queue| StatsCalculator  | Calculate some stats. Post the results message to text-queue and tweet-queue
tweet-queue     | Tweeter          | Send out the message in a tweet, using the tweepy module.
text-queue      | TextSender       | Text the message to all subscribers, using Twilio.

Additionally, there is a Twilio phone number that people can text in order to subscribe. Twilio forwards the message to an HTTP endpoint that triggers the TextReceiver function.
