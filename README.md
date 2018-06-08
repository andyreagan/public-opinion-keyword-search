# public-opinion-keyword-search

There are two parts here

1. Keyword search
2. Adding of matrices

## Keyword search

```
crontab -> cron.sh -> qsub.py -> processTweets.py
```

This passes each 15-minute Tweet file through the processTweets.py script.
A `.dat` file is saved.

## Adding

```
crontab -> cron-add.sh -> qsub-adddays.py -> addDaysAndy.py
```

and this runs on a whole day of the `.dat` files and adds them up.
