from django.db import models

class Address(models.Model):
    id = models.IntegerField(primary_key=True)  # Идентификатор
    name = models.CharField(max_length=255)  # Адрес
    katoCode = models.CharField(max_length=255)  # КАТО
    katoName = models.CharField(max_length=255)  # Наименование КАТО на русском языке
    countryCode = models.IntegerField()  # Код страны

    def __str__(self):
        return f"Address: {self.address}, KATO: {self.katoCode}"
    

class Subject(models.Model):
    pid = models.IntegerField(primary_key=True)  # Уникальный идентификатор
    bin = models.CharField(max_length=255)  # БИН
    crdate = models.IntegerField()  # Дата создания
    nameRu = models.CharField(max_length=255)  # Наименование на русском языке
    nameKz = models.CharField(max_length=255)  # Наименование на казахском языке
    address = models.OneToOneField(Address, on_delete=models.PROTECT)  # Адрес

    def __str__(self):
        return f"{self.nameRu} (BIN: {self.bin})"

    
class RefTradeMethods(models.Model):
    id = models.IntegerField(primary_key=True)
    nameRu = models.CharField(max_length=255)
    nameKz = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    type = models.IntegerField()
    symbolCode = models.CharField(max_length=255)
    isActive = models.IntegerField()
    f1 = models.IntegerField()
    ord = models.IntegerField()
    f2 = models.IntegerField()

    def __str__(self):
        return f"{self.nameRu} (ID: {self.id})"

class RefSubjectType(models.Model):
    id = models.IntegerField(primary_key=True)
    nameRu = models.CharField(max_length=255)
    nameKz = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nameRu} (ID: {self.id})"

class RefBuyStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    nameRu = models.CharField(max_length=255)
    nameKz = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nameRu} (ID: {self.id})"

class RefTypeTrade(models.Model):
    id = models.IntegerField(primary_key=True)
    nameRu = models.CharField(max_length=255)
    nameKz = models.CharField(max_length=255)
    refTradeMethodId = models.IntegerField()

    def __str__(self):
        return f"{self.nameRu} (ID: {self.id})"

class Tender(models.Model):
    id = models.IntegerField(primary_key=True)  # Уникальный идентификатор
    numberAnno = models.CharField(max_length=255)  # Номер объявления
    nameRu = models.CharField(max_length=255)  # Наименование на русском языке
    totalSum = models.FloatField()  # Общая сумма запланированная для закупки (Сумма закупки)
    refTradeMethodsId = models.IntegerField() # Код способа закупки
    refSubjectTypeId = models.IntegerField() # Вид предмета закупок
    refBuyStatusId = models.IntegerField() # Статуса объявления
    orgBin = models.CharField(max_length=255)  # БИН Организатора
    orgNameRu = models.CharField(max_length=255)  # Наименование организатора на русском языке
    startDate = models.CharField(max_length=255)  # Дата начала приема заявок
    endDate = models.CharField(max_length=255)  # Дата окончания приема заявок
    publishDate = models.CharField(max_length=255)  # Дата и время публикации
    itogiDatePublic = models.CharField(max_length=255)  # Дата публикации итогов
    biinSupplier = models.CharField(max_length=255)  # БИН/ИИН поставщика из одного источника
    isConstructionWork = models.IntegerField()  # Закупка с признаком СМР
    lastUpdateDate = models.CharField(max_length=255)  # Дата последнего изменения
    finYear = models.IntegerField()  # Финансовый год
    files = models.JSONField(default=list)  # Список файлов

    # Many-to-many relationship with Lots
    # Lots = models.ManyToManyField(Lots)

    # ForeignKey relationships
    RefTradeMethods = models.ForeignKey(RefTradeMethods, on_delete=models.CASCADE)  # Способ закупки
    RefSubjectType = models.ForeignKey(RefSubjectType, on_delete=models.CASCADE)  # Вид предмета закупки
    RefBuyStatus = models.ForeignKey(RefBuyStatus, on_delete=models.CASCADE)  # Статус объявления
    RefTypeTrade = models.ForeignKey(RefTypeTrade, on_delete=models.CASCADE)  # Тип закупки (первая, повторная)

    def __str__(self):
        return f"{self.nameRu} (ID: {self.id})"


class FileTrdBuy(models.Model):
    id = models.IntegerField(primary_key=True)  # ID
    filePath = models.CharField(max_length=255)  # Путь до файла
    originalName = models.CharField(max_length=255)  # Оригинальное имя файла
    objectId = models.JSONField(default=list)  # ID объекта
    nameRu = models.CharField(max_length=255)  # Наименование документа на русском языке
    nameKz = models.CharField(max_length=255)  # Наименование документа на государственном языке
    indexDate = models.CharField(max_length=255)  # Дата индексации
    systemId = models.IntegerField()  # Уникальный идентификатор системы

    def __str__(self):
        return f"{self.nameRu} (ID: {self.id})"
    

class Lots(models.Model):
    id = models.IntegerField(primary_key=True)  # Идентификатор
    lotNumber = models.CharField(max_length=255)  # Номер лота
    refLotStatusId = models.IntegerField()  # Статус лота
    count = models.FloatField()  # Общее количество
    amount = models.FloatField()  # Общая сумма
    nameRu = models.CharField(max_length=255)  # Наименование на русском языке
    descriptionRu = models.TextField()  # Детальное описание на русском языке
    customerId = models.IntegerField()  # Идентификатор заказчика
    customerBin = models.CharField(max_length=255)  # БИН заказчика
    customerNameRu = models.CharField(max_length=255)  # Наименование заказчика на русском языке
    trdBuyNumberAnno = models.CharField(max_length=255)  # Номер объявления
    trdBuyId = models.IntegerField()  # Уникальный идентификатор объявления
    dumping = models.IntegerField()  # Признак демпинга
    plnPointKatoList = models.JSONField(default=list)  # Список мест поставки
    isConstructionWork = models.IntegerField()  # Закупка с признаком СМР
    isDeleted = models.IntegerField()  # Объект удален

    # Assuming PlnPoint and Subject are models that you'll define later
    # Plans = models.ManyToManyField('PlnPoint')  # Пункт плана
    Customer = models.ForeignKey(Subject, on_delete=models.PROTECT)  # Заказчик
    # files = models.OneToOneField('Subject', on_delete=models.CASCADE)  # Заказчик
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)  # Тендер

    def __str__(self):
        return f"Lot {self.lotNumber}"

class FileLots(models.Model):
    id = models.IntegerField(primary_key=True)  # ID
    filePath = models.CharField(max_length=255)  # Путь до файла
    originalName = models.CharField(max_length=255)  # Оригинальное имя файла
    objectId = models.IntegerField()  # ID объекта
    nameRu = models.CharField(max_length=255)  # Наименование документа на русском языке
    nameKz = models.CharField(max_length=255)  # Наименование документа на государственном языке
    indexDate = models.CharField(max_length=255)  # Дата индексации
    systemId = models.IntegerField()  # Уникальный идентификатор системы
    lot = models.ForeignKey(Lots, on_delete=models.CASCADE)  # Лот

    def __str__(self):
        return f"{self.nameRu} (ID: {self.id})"

