from django.core.management.base import BaseCommand, CommandError
from projects.models import Tender

class Command(BaseCommand):
    help = "Feed the database with initial data"

    def handle(self, *args, **options):
            
        # Get the last updated tender
        last_id, tenders_to_update = self.get_last_update()

        # 

        # Print the results
        self.stdout.write(
            self.style.SUCCESS('Successfully fed the database! "%s"' %last_id)
        )
        for tender in tenders_to_update:
            self.stdout.write(
                self.style.SUCCESS('Successfully fed the database! "%s"' %tender)
            )


    def get_last_update(self):
        last_id: str = None
        tenders_to_update: list = []

        # Get the last updated tender
        if (Tender.objects.count() == 0):
            return last_id, tenders_to_update
        else:
            last_id = Tender.objects.order_by("-id").first().id_goszakup
        
        # Get all the tenders that need to be updated
        tenders_to_update = Tender.objects.filter(
            status__in=[
                "Published",
                "PublishedOrderTaking",
                "PublishedAdditionDemands",
                "PublishedPriceOffers",
                "BidReview",
                "BidAdditionalReview",
                "CompleteWaiting",
                "OnAppellation",
                "BeforeReviwePI",
            ]
        ).values_list('id', flat=True)

        return last_id, tenders_to_update
