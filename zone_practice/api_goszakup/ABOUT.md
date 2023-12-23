## The structure of the project

API to call is [/v3/trd-buy/bin/050140006873](/v3/trd-buy/bin/050140006873)

### The response

```json
{
  "total": 32,
  "limit": 50,
  "next_page": "",
  "items": [
    {
      "id": 415500,
      "number_anno": "415500-1",
      "name_ru": "Демонстрация Камеральный контроль (Аукцион)",
      "ref_trade_methods_id": 7,
      "publish_date": "2018-01-08 05:01:18",
      "start_date": "2018-01-08 05:01:18",
      "end_date": "2018-01-08 05:01:18",
      "total_sum": 10000,
      "ref_buy_status_id": 230
    }
  ]
}
```
- Additionally required fields:
  - <b>ref_subject_type_id</b> - Вид предмета закупок
  - <b>customer_bin</b> - БИН Заказчика
  - <b>is_construction_work</b> - Закупка с признаком СМР
  - <b>customer_name_ru</b> - Наименование заказчика на русском языке
- <b>next_page</b> will be an empty string if there are no next page
- "ref_buy_status_id" categories. Статус обьявления
  - 210 - опубликовано
  - 220 - Опубликовано (прием заявок)
  - 250 - Рассмотрение заявок
  - 190 - Изменена документация
  - 350 - Завершено
  - 310 - Формирование протокола преддопуска
  - 410 - Отказ от закупки
- "ref_trade_methods_id" categories. Тип оценки
  - 2 - Открытый конкурс
  - 188 - Конкурс с использованием рейтингово-балльной системы
  - 3 - Запрос ценовых предложений
  - 132 - Первый этап конкурса с использованием рамочного соглашения
  - 6 - Из одного источника по несостоявшимся закупкам
