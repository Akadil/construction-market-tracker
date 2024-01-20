from django.db import models

class TenderExperience(models.Model):
    Participant = models.ForeignKey('Participant', on_delete=models.CASCADE)

    number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    status_supplier = models.CharField(max_length=255)
    completion_year = models.IntegerField()
    construction_type = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    responsibility_level = models.CharField(max_length=255)
    technical_complexity = models.CharField(max_length=255)
    functional_purpose = models.CharField(max_length=255)

    def __str__(self):
        return f"[{self.bin}] {self.name}"


class Participant(models.Model):
    bin = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    katoCode = models.CharField(max_length=255)

    # Tax related scores
    score_tax_2023 = models.FloatField()
    score_tax_2024 = models.FloatField()
    financial_stability_2023 = models.FloatField()
    financial_stability_2024 = models.FloatField()

    # Experience related scores
    score_new_complex_two = models.FloatField()
    score_new_notComplex_two = models.FloatField()
    score_rep_complex_two = models.FloatField()
    score_rep_notComplex_two = models.FloatField()
    scoer_rec_complex_two = models.FloatField()
    score_rec_notComplex_two = models.FloatField()    
        
    def __str__(self):
        return f"[{self.bin}] {self.name}"


class Konkurs(models.Model):
    Participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    Tender = models.ForeignKey('projects.Tender', on_delete=models.CASCADE)
    price = models.FloatField()
    percentage = models.FloatField()
    score_experience = models.FloatField()
    score_tax = models.FloatField()
    score_address = models.BooleanField()
    score_winner = models.FloatField()
    score = models.FloatField()
    price_score = models.FloatField()
    financial_stability = models.FloatField()
    time_applied = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nameRu} (ID: {self.id})"

""" =================================================================="""

class Address(models.Model):
    name = models.CharField(max_length=255)  # Адрес
    katoCode = models.CharField(max_length=255)  # КАТО
    countryCode = models.IntegerField()  # Код страны

    def __str__(self):
        return f"[{self.katoCode}] {self.address}"


class Subject(models.Model):
    bin = models.CharField(primary_key=True, max_length=255)  # БИН
    nameRu = models.CharField(max_length=255)  # Наименование на русском языке
    address = models.OneToOneField(Address, on_delete=models.PROTECT)  # Адрес

    def __str__(self):
        return f"[BIN: {self.bin}] {self.nameRu}"

    
# @atttention the further tenders will be tracked by their id
class Tender(models.Model):
    numberAnno = models.CharField(max_length=255)  # Номер объявления
    nameRu = models.CharField(max_length=255)  # Наименование на русском языке
    totalSum = models.FloatField()  # Общая сумма запланированная для закупки (Сумма закупки)
    refBuyStatusId = models.IntegerField() # Статуса объявления
    startDate = models.CharField(max_length=255)  # Дата начала приема заявок
    endDate = models.CharField(max_length=255)  # Дата окончания приема заявок
    biinSupplier = models.CharField(max_length=255)  # БИН/ИИН поставщика из одного источника
    finYear = models.IntegerField()  # Финансовый год
    participants = models.ManyToManyField(Participant, through="Konkurs")  # Участники
    responsibilityLevel = models.IntegerField()  # Уровень ответственности
    functionalPurpose = models.IntegerField()  # Функциональное назначение
    technicalComplexity = models.IntegerField()  # Техническая сложность

    def __str__(self):
        return f"{self.nameRu} (ID: {self.id})"


class Lots(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)  # Тендер
    
    lotNumber = models.CharField(max_length=255)  # Номер лота
    refLotStatusId = models.IntegerField()  # Статус лота
    amount = models.FloatField()  # Общая сумма
    nameRu = models.CharField(max_length=255)  # Наименование на русском языке
    descriptionRu = models.TextField()  # Детальное описание на русском языке
    Customer = models.OneToOneField(Subject, on_delete=models.PROTECT)  # Заказчик

    def __str__(self):
        return f"Lot {self.lotNumber}"


class FileTrdBuy(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)  # Тендер
    filePath = models.CharField(max_length=255)  # Путь до файла
    originalName = models.CharField(max_length=255)  # Оригинальное имя файла

    def __str__(self):
        return f"{self.originalName}"


class FileLots(models.Model):
    lot = models.ForeignKey(Lots, on_delete=models.CASCADE)  # Лот
    filePath = models.CharField(max_length=255)  # Путь до файла
    originalName = models.CharField(max_length=255)  # Оригинальное имя файла

    def __str__(self):
        return f"{self.originalName}"

