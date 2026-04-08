import graphene
from graphql import GraphQLError
from .schema import TrainingType, TrainingDetailType
from .models import Training

class Query(graphene.ObjectType):
    trainings = graphene.List(TrainingType, start=graphene.DateTime(required=False), end=graphene.DateTime(required=False))
    training = graphene.Field(TrainingDetailType, id=graphene.UUID(required=True))

    def resolve_trainings(self, info, start = None, end = None):
        qs = Training.objects.all()

        if start:
            qs = qs.filter(scheduled_at__gte=start)

        if end:
            qs = qs.filter(scheduled_at__lte=end)

        return qs.order_by("scheduled_at")
    
    def resolve_training(self, info, id):
        try:
            return Training.objects.get(id=id)
        except Training.DoesNotExist:
            return None
        

class CreateTraining(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        scheduled_at = graphene.DateTime(required=True)

    training = graphene.Field(TrainingType)

    def mutate(self, info, title, scheduled_at):
        user = info.context.user

        if not user.is_authenticated:
            raise GraphQLError("Authentication required")
        
        if not (user.is_staff or user.is_superuser):
            raise GraphQLError("Permission denied")
        
        training = Training.objects.create(
            title=title,
            scheduled_at=scheduled_at,
            created_by=user
        )

        return CreateTraining(training=training)
    

class Mutation(graphene.ObjectType):
    create_training = CreateTraining.Field()



    
        
schema = graphene.Schema(query=Query, mutation=Mutation)