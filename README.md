Finally I was unable to use Tortoise ORM due to its migration framework aerich. It failed on init-db command @ https://github.com/tortoise/aerich/blob/dev/aerich/__init__.py#L140
with 
`tortoise.exceptions.ConfigurationError: default_connection for the model <class 'aerich.models.Aerich'> cannot be None`
while it actually creates table in db:
```
jaxel=# \d
 public | quote              | table    | jaxel
 public | quote_quote_id_seq | sequence | jaxel

```
I quit digging to deep and long for test task.
I kept all aerich staff and switched to sqlalchemy


Необходимо реализовать систему из двух микросервисов. Сервисы должны общаться между собой через Kafka (использовать ее как шину). Все взаимодействие должно быть асинхронное. 
БД - Postgres, фреймворк - FastAPI или Starlette.
Система должна разворачиваться через docker-compose.

Микросервис 1: получает данные о курсах обмена валют из внешнего сервиса Garantex (https://garantexio.github.io/#f00f8079b3) для пары USDT/RUB (market=usdtrub) и отправляет эти данные в Микросервис 2. Интервал получения значения курса должен настраиваться через env, значение по умолчанию - 5 секунд.

Микросервис 2: получает данные из Kafka и записывает информацию о курсах в БД. Для работы с БД необходимо использовать Tortoise ORM.
