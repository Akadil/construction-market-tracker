## The GraphQL functionality

- <b>POST</b> request to make [/v3/graphql](/v3/graphql)
  - content-type: application/json
  - authorization: Bearer {token}
- It allows to filter out data by values, and dates
- Also, it has links for tender files
- Necessary links:
    - [Link](https://ows.goszakup.gov.kz/help/v3/schema/) for GraphQL documentation
    - [Link](https://goszakup.gov.kz/ru/developer/ows_v3) for API page
    - [Link](https://habr.com/ru/articles/441438/) for explanation on how the websites GraphQL works

### Databases: 
<details>

<summary><b>TrdBuy</b> (projects)</summary>

```graphql
type TrdBuy {
    id: Int # Уникальный идентификатор
    numberAnno: String # Номер объявления
    nameRu: String # Наименование на русском языке
    nameKz: String # Наименование на государственном языке
    totalSum: Float # Общая сумма запланированная для закупки (Сумма закупки)
    countLots: Int # Количество лотов в объявлении
    refTradeMethodsId: Int # Код способа закупки
    refSubjectTypeId: Int # Вид предмета закупок
    customerBin: String # БИН Заказчика
    customerPid: Int # ИД Заказчика
    customerNameKz: String # Наименование заказчика на государственном языке
    customerNameRu: String # Наименование заказчика на русском языке
    orgBin: String # БИН Организатора
    orgPid: Int # ИД Организатора
    orgNameKz: String # Наименование организатора на государственном языке
    orgNameRu: String # Наименование организатора на русском языке
    refBuyStatusId: Int # Статуса объявления
    startDate: String # Дата начала приема заявок
    repeatStartDate: String # Срок начала повторного предоставления (дополнения) заявок
    repeatEndDate: String # Срок окончания повторного предоставления (дополнения) заявок
    endDate: String # Дата окончания приема заявок
    publishDate: String # Дата и время публикации
    itogiDatePublic: String # Дата публикации итогов
    refTypeTradeId: Int # Тип закупки (первая, повторная)
    disablePersonId: Int # Признак - Закупка среди организаций инвалидов
    discusStartDate: String # Срок начала обсуждения
    discusEndDate: String # Срок окончания обсуждения
    idSupplier: Int # ID поставщика из одного источника
    biinSupplier: String # БИН/ИИН поставщика из одного источника
    parentId: Int # ИД исходного объявления
    singlOrgSign: Int # Закупки Единого организатора КГЗ МФ РК
    isLightIndustry: Int # Закупка легкой и мебельной промышленности
    isConstructionWork: Int # Закупка с признаком СМР
    refSpecPurchaseTypeId: Int # Тип специальной закупки
    lastUpdateDate: String # Дата последнего изменения
    finYear: [Int] # Финансовый год
    kato: [String] # Место поставки (КАТО)
    systemId: Int # ИД системы
    indexDate: String # Дата индексации
    Lots: [Lots] # Лоты
    Organizer: Subject # Организатор
    Commission: [TrdBuyComm] # Конкурсная комиссия
    Cancel: [TrdBuyCancel] # Информация об отмене закупки
    Pause: TrdBuyPause # Информация о приостановлении закупки
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
    lastUpdateDate: String # Дата последнего изменения
    unionLots: Int # Признак объединенного лота
    count: Float # Общее количество
    amount: Float # Общая сумма
    nameRu: String # Наименование на русском языке
    nameKz: String # Наименование на государственном языке
    descriptionRu: String # Детальное описание на русском языке
    descriptionKz: String # Детальное описание на государственном языке
    customerId: Int # Идентификатор заказчика
    customerBin: String # БИН заказчика
    customerNameRu: String # Наименование заказчика на русском языке
    customerNameKz: String # Наименование заказчика на государственном языке
    trdBuyNumberAnno: String # Номер объявления
    trdBuyId: Int # Уникальный идентификатор объявления
    dumping: Int # Признак демпинга
    refTradeMethodsId: Int # Код планового способа закупки
    refBuyTradeMethodsId: Int # Код фактического способа закупки
    psdSign: Int # Признак работы. 1-работа с ТЭО/ПСД, 2-работа на разработку ТЭО/ПСД
    consultingServices: Int # Признак Консультационная услуга
    pointList: [Int] # Список пунктов плана
    enstruList: [Int] # Список ИД ЕНС ТРУ
    plnPointKatoList: [String] # Список мест поставки
    singlOrgSign: Int # Закупки Единого организатора КГЗ МФ РК
    isLightIndustry: Int # Закупка легкой и мебельной промышленности
    isConstructionWork: Int # Закупка с признаком СМР
    disablePersonId: Int # Признак - Закупка среди организаций инвалидов
    isDeleted: Int # Объект удален
    systemId: Int # Уникальный идентификатор системы
    indexDate: String # Дата индексации
    RefLotsStatus: RefLotsStatus # Справочник статусов
    Plans: [PlnPoint] # Пункт плана
    Customer: Subject # Заказчик
    TrdBuy: TrdBuy # Объявление
    RefTradeMethods: RefTradeMethods # Плановый способ закупки
    RefBuyTradeMethods: RefTradeMethods # Фактический способ закупки
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
<summary>TrdBuyCancel</summary>

```graphQL
type TrdBuyCancel {
    id: Int  # Идентификатор
    numberDecision: String  # Номер решения
    dateDecision: String  # Дата решения
    nameAuthority: String  # Наименование органа
    dateCreate: String  # Дата создания
    trdBuyId: Int  # Идентификатор объявления
    actTypeNameRu: String  # Вид акта отмены/приостановления закупки на русском языке
    actTypeNameKz: String  # Вид акта отмены/приостановления закупки на государственном языке
    typeActionsNameRu: String  # Решение по отмене на русском языке
    typeActionsNameKz: String  # Решение по отмене на государственном языке
    typeActionsCode: String  # Решение по отмене
    systemId: Int  # ИД системы
    indexDate: String  # Дата индексации
}
```
</details>

<details>
<summary>TrdBuyPause</summary>

```graphQL
type TrdBuyPause {
    id: Int # Идентификатор объявления
    status: Int # Статус
    dateCreate: String # Дата создания
    datePause: String # Дата приостановления заключения договора
    decideNumber: String # Номер решения пересмотра или отмены закупок
    decideDate: String # Дата решения пересмотра или отмены закупок
    decideDocKz: String # Наименование документа на государственном языке
    decideDocRu: String # Наименование документа на русском языке
    statusNameRu: String # Статус на государственном языке
    statusNameKz: String # Статус на русском языке
    solutionNameRu: String # На основании чего выбрано решение на государственном языке
    solutionNameKz: String # На основании чего выбрано решение на русском языке
    lots: [FieldByKeylots] 
    {
        id: Int
    }
    systemId: Int # ИД системы
    indexDate: String # Дата индексации
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
        id
        numberAnno
        nameRu
        totalSum
        refTradeMethodsId
        orgBin
        orgNameRu
        startDate
        endDate
        publishDate
        itogiDatePublic
        biinSupplier
        isConstructionWork
        finYear
        kato
        Lots
        {
            count
            amount
            nameRu
            descriptionRu
            customerBin
            customerNameRu
            isConstructionWork
            isDeleted
            Customer
            {
                bin
                nameRu
                Address
                {
                    id
                    address
                    katoCode
                }
            } 
            Files
            {
                filePath
                originalName
                nameRu
            }
        }
        Files
        {
            filePath
            originalName
            nameRu
        }
        RefTradeMethods
        {
            nameRu
            code
            isActive
        } 
        RefSubjectType
        {
            nameRu
        }
        RefBuyStatus
        {
            nameRu
            code
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
