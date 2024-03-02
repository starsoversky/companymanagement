from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import InsurancePolicy, MyUser, Vehicle


@receiver(post_save, sender=MyUser, dispatch_uid="assign_to_customer")
def add_doc_vehicle(sender, instance, created, **kwargs):

    if not instance.cache_is_active and instance.is_active:
        InsurancePolicy.objects.filter(customer_fin=instance.fin_code).update(
            customer=instance
        )
        Vehicle.objects.filter(customer_fin=instance.fin_code).update(customer=instance)
