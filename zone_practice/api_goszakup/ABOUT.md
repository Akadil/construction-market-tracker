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

> FUCKING SHEEP! <br>
> It appeared that there are GraphQL functionality enabled!
> I just have to take my data from there!!! and it's fucking HUGE!

## The GraphQL functionality

> There are just everything, fucking sheep

- <b>POST</b> request to make [/v3/graphql](/v3/graphql)
  - content-type: application/json
  - authorization: Bearer {token}
- It allows to filter out data by values, and dates
- Also, it has links for tender files

<details>
<summary><b>TrdBuy</b> (projects)</summary>

```graphql
type TrdBuy {
- id: Int # Уникальный идентификатор
- numberAnno: String # Номер объявления
- nameRu: String # Наименование на русском языке
- totalSum: Float # Общая сумма запланированная для закупки (Сумма закупки)
- customerBin: String # БИН Заказчика
- customerNameRu: String # Наименование заказчика на русском языке
- orgBin: String # БИН Организатора
- orgNameRu: String # Наименование организатора на русском языке
- startDate: String # Дата начала приема заявок
- endDate: String # Дата окончания приема заявок
- publishDate: String # Дата и время публикации
- itogiDatePublic: String # Дата публикации итогов
- idSupplier: Int # ID поставщика из одного источника
- biinSupplier: String # БИН/ИИН поставщика из одного источника
- isConstructionWork: Int # Закупка с признаком СМР
- lastUpdateDate: String # Дата последнего изменения
- finYear: [Int] # Финансовый год
- kato: [String] # Место поставки (КАТО)
- Lots: [Lots] # Лоты
- Organizer: Subject # организатор
- Files: [FileTrdBuy] # Документ закупки (документы лотов перенесены в объект Lots)
- RefTradeMethods: RefTradeMethods # Способ закупки
- RefSubjectType: RefSubjectType # Вид предмета закупки
- RefBuyStatus: RefBuyStatus # Статус объявления
- RefTypeTrade: RefTypeTrade # Тип закупки (первая, повторная)
}
```

</details>

<details>
<summary>Lots</summary>
</details>

<details>
<summary>FileTrdBuy</summary>

```graphql
type FileTrdBuy {
  id: Int # ID
  filePath: String # Путь до файла
  originalName: String # Оригинальное имя файла
  objectId: [Int] # ID объекта
  nameRu: String # Наименование документа на русском языке
  nameKz: String # Наименование документа на государственном языке
  indexDate: String # Дата индексации
  systemId: Int # Уникальный идентификатор системы
}
```

</details>

<details>
<summary>FileTrdBuy</summary>

```graphql
type FileLots {
  id: Int # ID
  filePath: String # Путь до файла
  originalName: String # Оригинальное имя файла
  objectId: Int # ID объекта
  nameRu: String # Наименование документа на русском языке
  nameKz: String # Наименование документа на государственном языке
  indexDate: String # Дата индексации
  systemId: Int # Уникальный идентификатор системы
}
```

</details>
