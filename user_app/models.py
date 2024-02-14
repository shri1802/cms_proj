from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Policy(models.Model):

    POLICY_TYPE_CHOICES = [
        ('health', 'Health'),
        ('life', 'Life'),
        ('auto', 'Auto'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    policy_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=100, choices=POLICY_TYPE_CHOICES)    
    lumpsum = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    verification = models.BooleanField(default=False)


    def is_verified(self):
        return self.verification
    
    def __str__(self):
        return f"USER: {self.user} | POLICY TYPE: {self.type} | POLICY NO. : {self.policy_number}"


class Claim(models.Model):
    STATUS_CHOICES = (
        ('A', 'Accepted'),
        ('B', 'Rejected'),
        ('C', 'Initiated'),
    )

    claim_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    policy_number = models.UUIDField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='C')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    res_amt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amt = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(default="--")

    def __str__(self):
        return f"USER: {self.user} | Claim Amount: {self.amt} | Claim ID: {self.claim_id}"