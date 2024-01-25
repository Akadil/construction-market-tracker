from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
    goszakup_id = models.CharField(max_length=15) # Идентификатор в Госзакупках
    name = models.TextField(max_length=100) # Наименование
    description = models.TextField(
        null = True,
        default = None
    ) # Описание
    address = models.TextField() # Адрес
    customer = models.ForeignKey(
        "participants.Subject",
        on_delete=models.PROTECT,
        related_name="%(class)s_customer"
    ) # Заказчик
    financial_year = models.CharField(
        max_length=4,
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
        max_length=10,
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
        "participants.ConstructionCompany", 
        through="participants.Competition"
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

    def getPercentage(self):
        """ 
            This function is used to identify the maximum allowed percentage
            of the lot
        """

        if self.amount > 200000000 * 3692:
            return 10
        return 5


class FinishedObject(ContructionObject):
    """
        This model is used to store the finished objects
    """
    
    class SupplierStatus_choices(models.TextChoices):
        CHIEFCONTRACTOR = 'CHIEF', 'Генподрядчик'
        SUBCONTRACTOR = 'SUB', 'Субподрядчик'

    contractor = models.ForeignKey(
        "participants.ConstructionCompany", 
        on_delete=models.CASCADE,
        related_name="contractor"
    ) # Застройщик
    contractor_status = models.CharField(
        max_length=5,
        choices=SupplierStatus_choices.choices,
        default=SupplierStatus_choices.CHIEFCONTRACTOR,
    ) # Статус поставщика

