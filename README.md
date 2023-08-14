![birthdaygram workflow](https://github.com/melax08/birthdaygram/actions/workflows/birthdaygram-workflow.yml/badge.svg)

## Settings
### Cron settings:
To check today birthdays via cron, add cron-job to host machine:

```shell
crontab -e
```
```shell
0 12,18 * * *  docker compose --file /home/birthdaygram/birthdaygram/docker-compose.yml exec birthdaygram_bot python cron.py
```
After --file specify the path to docker-compose.yml.
This cron job will run cron task on 12 AM and 6 PM every day.