from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Company, InsurancePolicy, MyUser, Vehicle


@receiver(post_save, sender=MyUser, dispatch_uid="assign_to_customer")
def add_doc_vehicle(sender, instance, created, **kwargs):
    if not instance.cache_is_active and instance.is_active:
        if instance.user_type == "1":
            InsurancePolicy.objects.filter(customer_fin=instance.fin_code).update(
                customer=instance
            )
            Vehicle.objects.filter(customer_fin=instance.fin_code).update(
                customer=instance
            )

            # company = Company.objects.filter(
            #     registration_number=instance.registration_number
            # ).last()
            # user = MyUser.objects.filter(pk=instance.pk).update(company=company)
    if instance.is_active and not instance.cache_is_staff and instance.is_staff:
        if instance.user_type in ["2", "3"]:
            company = Company.objects.filter(
                registration_number=instance.registration_number
            ).last()
            user = MyUser.objects.filter(pk=instance.pk).update(company=company)
