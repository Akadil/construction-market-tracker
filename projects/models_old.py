from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ProjectCharacteristics(models.Model):

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
    # General info
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
    

class ParticipantProjects(models.Model):
    """
        This model is used to store the experience of the participant

        Related to: Participant model
    """

    class SupplierStatus_choices(models.TextChoices):
        CHIEFCONTRACTOR = 'CHIEF', 'Генпроектировщик'
        SUBCONTRACTOR = 'SUB', 'Субподрядчик'
    
    # ==================================================================
    # Project info
    number = models.CharField(max_length=20) # Номер
    name = models.TextField() # Наименование
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
    characteristics = models.OneToOneField(
        ProjectCharacteristics, 
        on_delete=models.CASCADE
    ) # Характеристики

    def __str__(self):
        return f"Participant Projects: {self.name} - {self.participant.name}"

    def full_representation(self):
        return f"Project: {self.number} - {self.name}\n" \
               f"Completion Year: {self.completion_year}\n" \
               f"Address: {self.address}\n" \
               f"Participant: {self.participant.name}\n" \
               f"Supplier Status: {self.get_supplier_status}\n" \
               f"Construction Type: {self.get_construction_type}\n" \
               f"Responsibility Level: {self.get_responsibility_level}\n" \
               f"Technical Complexity: {self.get_technical_complexity}\n" \
               f"Functional Purpose: {self.get_functional_purpose}\n"


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
    """
        This model is used to store the address of any onject
    """

    name = models.TextField()  # Адрес
    katoCode = models.CharField(max_length=10)  # КАТО
    countryCode = models.CharField(max_length=10)  # Код страны

    def __str__(self):
        return f"Address: {self.katoCode} - {self.name}"


class Subject(models.Model):
    """
        This model is used to store the subject of the tender
    """

    bin = models.CharField(
        primary_key=True, 
        max_length=20
    )  # БИН
    nameRu = models.CharField(max_length=255)  # Наименование на русском языке
    address = models.OneToOneField(Address, on_delete=models.PROTECT)  # Адрес

    def __str__(self):
        return f"Subject: {self.bin} - {self.nameRu}"

    
# @atttention the further tenders will be tracked by their id
class Tender(models.Model):
    """
        This model is used to store the tenders
    """

    number_anno = models.CharField(max_length=20)  # Номер объявления
    name_ru = models.TextField(max_length=255)  # Наименование на русском языке
    total_sum = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )  # Общая сумма запланированная для закупки (Сумма закупки)
    refBuyStatusId = models.IntegerField() # Статуса объявления
    start_date = models.DateTimeField()  # Дата начала приема заявок
    end_date = models.DateTimeField()  # Дата окончания приема заявок
    biin_supplier = models.CharField(max_length=20)  # БИН/ИИН поставщика из одного источника
    fin_year = models.IntegerField(
        validators=[MinValueValidator(1992), MaxValueValidator(2025)]
    )  # Финансовый год

    def __str__(self):
        return f"Tender: {self.number_anno} - {self.name_ru}"

    def full_representation(self):
        return f"Number of Announcement: {self.number_anno}\n" \
               f"Name (Russian): {self.name_ru}\n" \
               f"Total Sum: {float(self.total_sum)}\n" \
               f"Buy Status ID: {self.refBuyStatusId}\n" \
               f"Start Date: {str(self.start_date)}\n" \
               f"End Date: {str(self.end_date)}\n" \
               f"Supplier BIN/IIN: {self.biin_supplier}\n" \
               f"Financial Year: {self.fin_year}" \
                f"Lots: {self.lots.all()}\n"


class Lots(models.Model):
    """
        This model is used to store the lots of the tender
    """

    # ==================================================================
    # Model relations
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)  # Тендер
    participants = models.ManyToManyField(Participant, through="Competition")  # Участники
    Customer = models.OneToOneField(Subject, on_delete=models.PROTECT) # Заказчик
    
    # ==================================================================
    # General info
    number_lot = models.CharField(max_length=255)  # Номер лота
    refLotStatusId = models.IntegerField()  # Статус лота
    amount = models.DecimalField(
        max_digits=14,
        decimals=2
    )  # Общая сумма
    nameRu = models.TextField()  # Наименование на русском языке
    descriptionRu = models.TextField()  # Детальное описание на русском языке

    # ==================================================================
    # Tender characteristics
    characteristics = models.OneToOneField(
        ProjectCharacteristics, 
        on_delete=models.CASCADE
    ) # Характеристики

    def getPercentage(self):
        """ 
            This function is used to identify the maximum allowed percentage
            of the lot
        """

        if self.amount > 200000000 * 3692:
            return 10
        return 5

    def __str__(self):
        return f"Lot: {self.lotNumber} - {self.nameRu}"

    def full_representation(self):
        return f"Lot ID: {self.id}\n" \
               f"Number: {self.lotNumber}\n" \
               f"Status ID: {self.refLotStatusId}\n" \
               f"Amount: {float(self.amount)}\n" \
               f"Name (Russian): {self.nameRu}\n" \
               f"Description (Russian): {self.descriptionRu}\n" \
               f"Tender: {self.tender}\n" \
               f"Participants: {', '.join(str(participant) for participant in self.participants.all())}\n" \
               f"Customer: {self.Customer}"


# class FileTrdBuy(models.Model):
#     tender = models.ForeignKey(Tender, on_delete=models.CASCADE)  # Тендер
#     filePath = models.CharField(max_length=255)  # Путь до файла
#     originalName = models.CharField(max_length=255)  # Оригинальное имя файла

#     def __str__(self):
#         return f"{self.originalName} - {self.filePath}"


# class FileLots(models.Model):
#     lot = models.ForeignKey(Lots, on_delete=models.CASCADE)  # Лот
#     filePath = models.CharField(max_length=255)  # Путь до файла
#     originalName = models.CharField(max_length=255)  # Оригинальное имя файла

#     def __str__(self):
#         return f"{self.originalName} - {self.filePath}"

