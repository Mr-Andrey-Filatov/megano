# Megano
**Описанием проекта:** Интернет магазинт
________________________________
#### Команды для поднятия проекта
##### Стандартные
`pip install requirements.txt`  
`python manage.py migrate`
________________________________

##### Создание пользователей
`python manage.py create_users`  

_После `create_users` нужно указать целое число от 10 до 100_  
_Число количество создаваемых пользователей_  

**Например**: `python manage.py create_users 50`

_По пути  `authapp/management/commands/report.txt`_  
_Будет создан конечный файл в котором можно просмотреть данные для входа._
________________________________

##### Создание каталога
`python manage.py create_categories`  
`python manage.py create_specifications`  
`python manage.py create_tags`

_Параметроа не имеют. `Категории, харктиристики, теги` создадутся автоматически._
  
`python manage.py create_product`  

_После `create_product` нужно указать целое число от 10 до 200_  
_Число количество создаваемых продуктов_  

**Например**: `python manage.py create_product 50`  

`python manage.py create_reviews`  

_Параметроа не имеет. `Отзывы` создадутся автоматически._

`python manage.py create_sales`

_Параметроа не имеет. `Распродажи` создадутся автоматически._
________________________________

##### Создание заказов
`python manage.py create_orders`  

_Параметроа не имеет. `Заказы и Элементы заказов` создадутся автоматически._

`python manage.py create_payments`  

_Параметроа не имеет. `Платежи заказов` создадутся автоматически._
________________________________