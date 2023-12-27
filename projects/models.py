from django.db import models

# Create your models here.
class Tender(models.Model):
    helloWorld = models.CharField(max_length=200)

    def __str__(self):
        return self.helloWorld
    

class Lots(models.Model):
    helloWorld = models.CharField(max_length=200)

    def __str__(self):  
        return self.helloWorld
    
class Files(models.Model):
    helloWorld = models.CharField(max_length=200)

    def __str__(self):
        return self.helloWorld
    

class Address(models.Model):
    helloWorld = models.CharField(max_length=200)

    def __str__(self):
        return self.helloWorld
    

