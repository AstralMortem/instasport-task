from graphene_django import DjangoObjectType
from .models import Training

class TrainingType(DjangoObjectType):
    class Meta:
        model = Training
        fields = ("id", "title", "scheduled_at")

class TrainingDetailType(DjangoObjectType):
    class Meta:
        model = Training
        field = "__all__"