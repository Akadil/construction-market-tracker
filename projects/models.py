from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ParticipantExperience(models.Model):
    """
        This model is used to store the experience of the participant

        Related to: Participant model
    """

    class SupplierStatus_choices(models.TextChoices):
        CHIEFCONTRACTOR = 'CHIEF', 'Генпроектировщик'
        SUBCONTRACTOR = 'SUB', 'Субподрядчик'
    
    class ConstructionType_choices(models.TextChoices):
        NEW = 'NEW', 'Новое строительство'
        RECONSTRUCTION = 'REC', 'Реконструкция'
        REPAIRMENT = 'REP', 'Капитальный ремонт'

    class ResponsibilityLevel_choices(models.TextChoices):
        FIRST = 'FIRST', 'Первый - повышенный'
        SECOND = 'SECOND', 'Второй - нормальный'
        THIRD = 'THIRD', 'Третий - пониженный'

    class TechnicalComplexity_choices(models.TextChoices):
        COMPLEX = 'COMPLEX', 'Сложный'
        NOTCOMPLEX = 'NOTCOMPLEX', 'Не сложный'

    class FunctionalPurpose_choices(models.TextChoices):
        INDUSTRIAL = 'INDUSTRIAL', 'Промышленные объекты'
        PRODUCTION = 'PRODUCTION', 'Производственные объекты'
        CIVIL = 'CIVIL', 'Жилищно-Гражданское'
        OTHER = 'OTHER', 'Прочие сооружения'

    # ==================================================================
    # Project info
    number = models.CharField(max_length=20) # Номер
    Name = models.TextField() # Наименование
    completion_year = models.IntegerField(
        validators=[MinValueValidator(1992), MaxValueValidator(2025)], 
        default=2010
    ) # Год сдачи
    address = models.TextField() # Адрес
    
    # ==================================================================
    # Contractor (Winner) info 
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE) # Поставщик
    supplier_status = models.CharField(
        max_length = 5, 
        choices = SupplierStatus_choices.choices, 
        default = SupplierStatus_choices.CHIEFCONTRACTOR
    ) # Статус поставщика

    # ==================================================================
    # Tender characteristics
    construction_type = models.CharField(
        max_length=3,
        choices=ConstructionType_choices.choices,
        default=ConstructionType_choices.NEW
    ) # Тип строительства
    responsibility_level = models.CharField(
        max_length=6,
        choices=ResponsibilityLevel_choices.choices,
        default=ResponsibilityLevel_choices.SECOND
    ) # Уровень ответственности
    technical_complexity = models.CharField(
        max_length=9,
        choices=TechnicalComplexity_choices.choices,
        default=TechnicalComplexity_choices.NOTCOMPLEX
    ) # Техническая сложность
    functional_purpose = models.CharField(
        max_length=11,
        choices=FunctionalPurpose_choices.choices,
        default=FunctionalPurpose_choices.CIVIL
    ) # Функциональное назначение

    def __str__(self):
        return f"Participant Experience: {self.name} - {self.participant.name}"

    def full_representation(self):
        return f"Project: {self.number} - {self.name}\n" \
               f"Completion Year: {self.completion_year}\n" \
               f"Address: {self.address}\n" \
               f"Participant: {self.participant.name}\n" \
               f"Supplier Status: {self.get_supplier_status_display()}\n" \
               f"Construction Type: {self.get_construction_type_display()}\n" \
               f"Responsibility Level: {self.get_responsibility_level_display()}\n" \
               f"Technical Complexity: {self.get_technical_complexity_display()}\n" \
               f"Functional Purpose: {self.get_functional_purpose_display()}\n"


class Participant(models.Model):
    """
        This model is used to store the participants of the tender
    """
    
    # ==================================================================
    # General info
    bin = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    kato_code = models.CharField(max_length=10)

    # ==================================================================
    # Tax related scores
    score_tax_2023 = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        null=True,
        default=None
    )
    score_tax_2024 = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        null=True,
        default=None
    )
    financial_stability_2023 = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        null=True,
        default=None
    )
    financial_stability_2024 = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        null=True,
        default=None
    )

    # ==================================================================
    # Experience related scores
    score_new_complex_two = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        default=None
    )
    score_new_notComplex_two = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        default=None
    )
    score_rep_complex_two = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        default=None
    )
    score_rep_notComplex_two = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        default=None
    )
    scoer_rec_complex_two = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        default=None
    )
    score_rec_notComplex_two = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        default=None
    )    
        
    def __str__(self):
        return f"Participant: {self.name} - {self.bin}"

    def full_representation(self):
        return f"Participant: {self.name}\n" \
               f"BIN: {self.bin}\n" \
               f"KATO Code: {self.kato_code}\n" \
               f"Tax Scores:\n" \
               f"   - 2023: {self.score_tax_2023}\n" \
               f"   - 2024: {self.score_tax_2024}\n" \
               f"Financial Stability:\n" \
               f"   - 2023: {self.financial_stability_2023}\n" \
               f"   - 2024: {self.financial_stability_2024}\n" \
               f"Experience Scores:\n" \
               f"   - New (Complex): {self.score_new_complex_two}\n" \
               f"   - New (Not Complex): {self.score_new_notComplex_two}\n" \
               f"   - Rep (Complex): {self.score_rep_complex_two}\n" \
               f"   - Rep (Not Complex): {self.score_rep_notComplex_two}\n" \
               f"   - Rec (Complex): {self.scoer_rec_complex_two}\n" \
               f"   - Rec (Not Complex): {self.score_rec_notComplex_two}"


class Competition(models.Model):
    """
        This model is used to store the competition info of the participant
        in the tender
    """

    # ==================================================================
    # The linker between the participant and the lot
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    lot = models.ForeignKey('projects.Lot', on_delete=models.CASCADE)
    
    # ==================================================================
    # General info
    price = models.DecimalField(
        max_digits=14, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100000000000)], # 100 billion
        default=lot.amount
    )
    percentage = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(lot.getPercentage())],
        default=0
    )
    score_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(lot.getPercentage())],
        default=0
    )
    score_tax = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        default=0
    )
    score_address = models.BooleanField(default=False)
    score_winner = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0
    ) # Отричательное значение
    score = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(lot.getPercentage() + 3)],
        default=0
    )
    price_score = models.DecimalField(
        max_digits=14, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100000000000)], # 100 billion
        default=lot.amount
    )
    financial_stability = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        default=0
    )
    time_applied = models.DateTimeField()

    def __str__(self):
        return f"Competition: {self.participant} {self.lot}"

    def full_representation(self):
        return f"Participant: {self.participant}\n" \
               f"Lot: {self.lot}\n" \
               f"Price: {float(self.price)}\n" \
               f"Percentage: {float(self.percentage)}\n" \
               f"Experience Score: {float(self.score_experience)}\n" \
               f"Tax Score: {float(self.score_tax)}\n" \
               f"Address Score: {bool(self.score_address)}\n" \
               f"Winner Score: {float(self.score_winner)}\n" \
               f"Total Score: {float(self.score)}\n" \
               f"Price Score: {float(self.price_score)}\n" \
               f"Financial Stability: {float(self.financial_stability)}\n" \
               f"Time Applied: {str(self.time_applied)}"


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
    participants = models.ManyToManyField(Participant, through="Competition")  # Участники
    nameRu = models.CharField(max_length=255)  # Наименование на русском языке
    descriptionRu = models.TextField()  # Детальное описание на русском языке
    Customer = models.OneToOneField(Subject, on_delete=models.PROTECT)  # Заказчик

    def getPercentage(self):
        """ 
            This function is used to identify the maximum allowed percentage
            of the lot
        """

        if self.amount > 200000000 * 3692:
            return 10
        return 5

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

