from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
    """
        This model is used to store the customers of the tender (Заказчик)
    """

    REGION_CHOICES = (
        ('75', 'г. Алматы', (
            ('751110000', 'Алмалинский район'),
            ('751210000', 'Алатауский район'),
            ('751310000', 'Ауэзовский район'),
            ('751410000', 'Бостандыкский район'),
            ('751510000', 'Жетысуский район'),
            ('751710000', 'Медеуский район'),
            ('751810000', 'Наурызбайский район'),
            ('751910000', 'Турксибский район'),
        )),
        ('19', 'Алматинская область', (
            ('191000000', 'Қонаев Г.'),
            ('191600000', 'Капчагай Г.'),
            ('192600000', 'Текели Г.'),
            ('193200000', 'Аксуский район'),
            ('193400000', 'Алакольский район'),
            ('193600000', 'Балхашский район'),
            ('194000000', 'Енбекшиказахский район'),
            ('194200000', 'Жамбылский район'),
            ('194400000', 'Кегенский район'),
            ('194600000', 'Кербулакский район'),
            ('194800000', 'Коксуский район'),
            ('195000000', 'Каратальский район'),
            ('195200000', 'Карасайский район'),
            ('195600000', 'Панфиловский район'),
            ('195800000', 'Райымбекский район'),
            ('196000000', 'Саркандский район'),
            ('196200000', 'Талгарский район'),
            ('196400000', 'Ескельдинский район'),
            ('196600000', 'Уйгурский район'),
            ('196800000', 'Илийский район'),
        )),
        ('33', 'область Жетису', (
            ('331000000', 'Талдыкорган Г.'),
            ('331800000', 'Текели Г.'),
            ('333200000', 'Аксуский район'),
            ('333400000', 'Алакольский район'),
            ('333600000', 'Ескельдинский район'),
            ('334000000', 'Кербулакский район'),
            ('334200000', 'Коксуский район'),
            ('334400000', 'Каратальский район'),
            ('334600000', 'Панфиловский район'),
            ('334800000', 'Саркандский район'),
        )),
        ('00', 'Unknown')
    )

    bin = models.CharField(
        max_length=20, 
        null=True, 
        default=None,
        unique=True
    )
    name_ru = models.CharField(max_length=255)
    name_kz = models.CharField(max_length=255, null=True, default=None)
    address = models.TextField(null=True, default=None)
    region = models.CharField(
        max_length=11,
        choices=REGION_CHOICES,
        null=True,
        default=None
    )


    def is_kato_code_in_choices(self, kato_code):
        """
            Check if the provided KATO code exists in the REGION_CHOICES.
        """
        for top_level_choice in self.REGION_CHOICES:
            if kato_code == top_level_choice[0]:  # Check if key matches top-level choice
                return True
            elif len(top_level_choice) == 3:  # Check if there are sub-choices
                for sub_choice in top_level_choice[2]:
                    if kato_code == sub_choice[0]:  # Check if key matches sub-choice
                        return True
        return False


class ConstructionCompany(Subject):
    """
        This model is used to store the participants of the tender
    """

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


class ContructionObject(models.Model):

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
    # General information
    id_goszakup = models.CharField(max_length=15) # Идентификатор в Госзакупках
    name = models.TextField(max_length=100) # Наименование
    description = models.TextField(
        null = True,
        default = None
    ) # Описание
    address = models.TextField() # Адрес
    customer = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT
    ) # Заказчик
    financial_year = models.IntegerField(
        validators=[MinValueValidator(1992), MaxValueValidator(2025)], 
        default=2010
    ) # Год сдачи

    # ==================================================================
    # Characteristics of the object
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
    

    class Meta:
        abstract = True


class Tender(models.Model):
    """
        This model is used to store the tender info
    """

    # ==================================================================
    # General info
    id_goszakup = models.CharField(max_length=15) # Идентификатор в Госзакупках
    tender_number = models.CharField(max_length=15) # Номер объявления
    name = models.TextField(max_length=100) # Наименование
    total_sum = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100000000000)], # 100 billion
    )

    status = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class OngoingObject(ContructionObject):
    """
        This model is used to store the ongoing objects
    """

    class Status_choices(models.TextChoices):
        DOCUMENTATIONCHANGED = 'DocumentationСhanged', 'Изменена документация'
        PUBLISHED = 'Published', 'Опубликовано'
        PUBLISHEDORDERTAKING = 'PublishedOrderTaking', 'Опубликовано (прием заявок)'
        PUBLISHEDADDITIONDEMANDS = 'PublishedAdditionDemands', 'Опубликовано (дополнение заявок)'
        PUBLISHEDPRICEOFFERS = 'PublishedPriceOffers', 'Опубликовано (прием ценовых предложений)'
        BIDREVIEW = 'BidReview', 'Рассмотрение заявок'
        BIDADDITIONALREVIEW = 'BidAdditionalReview', 'Рассмотрение дополнений заявок'
        COMPLETE = 'Complete', 'Завершено'
        REFUSALOFPURCHASE = 'RefusalOfPurchase', 'Отказ от закупки'
        CANCELED = 'Canceled', 'Отменено'
        ONAPPELLATION = 'OnAppellation', 'На обжаловании'
        BEFOREREVIWEPI = 'BeforeReviwePI', 'Принятие решение об исполнении уведомления'

    lot_number = models.CharField(max_length=10) # Номер лота
    tender = models.ForeignKey(
        Tender,
        on_delete=models.CASCADE
    ) # Тендер
    participants = models.ManyToManyField(
        ConstructionCompany, 
        through="Competition"
    ) # Участники
    amount = models.DecimalField(   
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100000000000)], # 100 billion
        default=0
    ) # Стоимость
    status = models.CharField(
        max_length=25,
        choices=Status_choices.choices,
        default=Status_choices.PUBLISHED
    ) # Статус


class FinishedObject(ContructionObject):
    """
        This model is used to store the finished objects
    """
    
    class SupplierStatus_choices(models.TextChoices):
        CHIEFCONTRACTOR = 'CHIEF', 'Генподрядчик'
        SUBCONTRACTOR = 'SUB', 'Субподрядчик'

    contractor = models.ForeignKey(
        ConstructionCompany, 
        on_delete=models.CASCADE
    ) # Застройщик
    contractor_status = models.CharField(
        max_length=4,
        choices=SupplierStatus_choices.choices,
        default=SupplierStatus_choices.CHIEFCONTRACTOR,
    ) # Статус поставщика


class Competition(models.Model):
    """
        This model is used to store the competition info of the participant
        in the tender

        @attention - participant field is protected as it is the main Model
                        Really strange, as I am not going to delete the Company.
    """

    # ==================================================================
    # The linker between the participant and the lot
    participant = models.ForeignKey(
        ConstructionCompany, 
        on_delete=models.SET_NULL,
        null=True,
    )
    lot = models.ForeignKey(
        OngoingObject, 
        on_delete=models.SET_NULL,
        null=True,
    )
    
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
    score_address = models.BooleanField(
        default=False
    )
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

