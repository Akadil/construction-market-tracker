## The GraphQL functionality

- <b>POST</b> request to make [/v3/graphql](/v3/graphql)
  - content-type: application/json
  - authorization: Bearer {token}
- It allows to filter out data by values, and dates
- Also, it has links for tender files

### Databases: 
<details>

<summary><b>TrdBuy</b> (projects)</summary>

```graphql
type TrdBuy {
    id: Int # Уникальный идентификатор
    numberAnno: String # Номер объявления
    nameRu: String # Наименование на русском языке
    totalSum: Float # Общая сумма запланированная для закупки (Сумма закупки)
    customerBin: String # БИН Заказчика
    customerNameRu: String # Наименование заказчика на русском языке
    orgBin: String # БИН Организатора
    orgNameRu: String # Наименование организатора на русском языке
    startDate: String # Дата начала приема заявок
    endDate: String # Дата окончания приема заявок
    publishDate: String # Дата и время публикации
    itogiDatePublic: String # Дата публикации итогов
    idSupplier: Int # ID поставщика из одного источника
    biinSupplier: String # БИН/ИИН поставщика из одного источника
    isConstructionWork: Int # Закупка с признаком СМР
    lastUpdateDate: String # Дата последнего изменения
    finYear: [Int] # Финансовый год
    kato: [String] # Место поставки (КАТО)
    Lots: [Lots] # Лоты
    Organizer: Subject # организатор
    Files: [FileTrdBuy] # Документ закупки (документы лотов перенесены в объект Lots)
    RefTradeMethods: RefTradeMethods # Способ закупки
    RefSubjectType: RefSubjectType # Вид предмета закупки
    RefBuyStatus: RefBuyStatus # Статус объявления
    RefTypeTrade: RefTypeTrade # Тип закупки (первая, повторная)
}
```

</details>

<details>
<summary>Lots</summary>

```graphQL
type Lots {
    id: Int # Идентификатор
    lotNumber: String # Номер лота
    refLotStatusId: Int # Статус лота
    count: Float # Общее количество
    amount: Float # Общая сумма
    nameRu: String # Наименование на русском языке
    descriptionRu: String # Детальное описание на русском языке
    customerId: Int # Идентификатор заказчика
    customerBin: String # БИН заказчика
    customerNameRu: String # Наименование заказчика на русском языке
    trdBuyNumberAnno: String # Номер объявления
    trdBuyId: Int # Уникальный идентификатор объявления
    dumping: Int # Признак демпинга
    plnPointKatoList: [String] # Список мест поставки
    isConstructionWork: Int # Закупка с признаком СМР
    isDeleted: Int # Объект удален
    Plans: [PlnPoint] # Пункт плана
    Customer: Subject # Заказчик
    Files: [FileLots] # Документ лота
}
```

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
<summary>FileLots</summary>

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

<details>
<summary>Subject</summary>

```graphQL
type Subject {
    pid: Int # Уникальный идентификатор
    bin: String # БИН
    crdate: Int # Дата создания
    nameRu: String # Наименование на русском языке
    katoList: [String] # Массив кодов КАТО
    customer: Int # Флаг Заказчик (1 - да, 0 - Нет)
    organizer: Int # Флаг Организатор (1 - да, 0 - Нет)
    supplier: Int # Флаг Поставщик (1 - да, 0 - Нет)
    Address: [SubjectAddress] # Адреса
}
```
</details>

<details>
<summary>Subject address</summary>

```graphQL
type SubjectAddress {
    id: Int # Идентификатор
    addressType: Int # Тип адреса
    address: String # Адрес
    katoCode: String # КАТО
    RefKato: RefKato # КАТО
}
```
</details>

<details>
<summary>RefTradeMethods</summary>

```graphQL
type RefTradeMethods {
    id: Int
    nameRu: String
    nameKz: String
    code: String
    type: Int
    symbolCode: String
    isActive: Int
    f1: Int
    ord: Int
    f2: Int
}
```
</details>

<details>
<summary>RefSubjectType</summary>

```graphQL
    type RefSubjectType {
        id: Int
        nameRu: String
        nameKz: String
    }
```
</details>

<details>
<summary>RefBuyStatus</summary>

```graphQL
    type RefBuyStatus {
        id: Int
        nameRu: String
        nameKz: String
        code: String
    }
```
</details>

<details>
    <summary>RefTypeTrade</summary>

```graphQL
    type RefTypeTrade {
        id: Int
        nameRu: String
        nameKz: String
        refTradeMethodId: Int
    }
```
</details>


### data needed 

```ts
query($filter: TrdBuyFiltersInput) {
    TrdBuy(filters: $filter) {
        id: Int 
        numberAnno: String 
        nameRu: String 
        totalSum: Float
        refTradeMethodsId: Int
        orgBin: String 
        orgNameRu: String 
        startDate: String 
        endDate: String 
        publishDate: String 
        itogiDatePublic: String 
        biinSupplier: String 
        isConstructionWork: Int 
        finYear: Int 
        kato: String 
        Lots: Lots 
        {
            count: Float 
            amount: Float 
            nameRu: String 
            descriptionRu: String 
            customerBin: String 
            customerNameRu: String 
            isConstructionWork: Int 
            isDeleted: Int 
            Customer: Subject
            {
                bin: String 
                nameRu: String 
                Address: SubjectAddress
                {
                    id: Int 
                    address: String 
                    katoCode: String 
                }
            } 
            Files: FileLots
            {
                filePath: String 
                originalName: String 
                nameRu: String 
            }
        }
        Files: FileTrdBuy
        {
            filePath: String 
            originalName: String 
            nameRu: String 
        }
        RefTradeMethods: RefTradeMethods
        {
            nameRu: String
            code: String
            isActive: Int
        } 
        RefSubjectType: RefSubjectType
        {
            nameRu: String
        }
        RefBuyStatus: RefBuyStatus
        {
            nameRu: String
            code: String
        }
    }
}
```
```python
variables = {
    "filter": {
        "financial_year": [2023, 2024]
    }
}
```
