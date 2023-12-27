from django.db import models

# Finished

class Address(models.Model):
    """
        @todo   Get all possible fields from the documentation
                each katocode has a name
        @todo   Rewrite "create" method to put katoName automatically

        @detail     used in Customer class, Participant, Tender
    """
    name = models.CharField(max_length=200)
    countryCode = models.IntegerField()
    katoCode = models.CharField(max_length=200)
    katoName = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.katoCode}: {self.name}"
    

class Customer(models.Model):
    bin = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=200)
    address = models.OneToOneField(Address, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.bin}: {self.name}"


# ==================================================
# Unfinished

class Tender(models.Model):
    helloWorld = models.CharField(max_length=200)

    def __str__(self):
        return self.helloWorld


class Lot(models.Model):
    number = models.CharField(primary_key=True, max_length=200)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):  
        return self.helloWorld

# Do I need make it unique. I don't think


class Files(models.Model):
    filePath = models.CharField(max_length=200)
    originalNamee = models.CharField(max_length=200)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    

    isLot = models.BooleanField()
    isTender = models.BooleanField()

    def __str__(self):
        return self.helloWorld
    