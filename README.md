## Settings
### Cron settings:
To check today birthdays via cron, add cron-job to host machine:

```shell
crontab -e
```
```shell
0 12,18 * * *  docker compose --file /home/birthdaygram/birthday_reminder_bot/docker-compose.yml exec birthdaygram python cron.py
```
After --file specify the path to docker-compose.yml.
This cron job will run cron task on 12 AM and 6 PM every day.