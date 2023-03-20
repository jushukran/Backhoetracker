import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from backhoetracker.models import User, Payment, Job, Client, Task

class UserType(DjangoObjectType):
    class Meta:
        model = User

class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment

class JobType(DjangoObjectType):
    class Meta:
        model = Job

class ClientType(DjangoObjectType):
    class Meta:
        model = Client

class TaskType(DjangoObjectType):
    class Meta:
        model = Task

class CreateUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        id_number = graphene.String(required=True)
        role = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, first_name, id_number, role, password):
        user = User.objects.create(first_name=first_name, id_number=id_number, role=role, password=password)
        return CreateUser(user=user)

class CreatePayment(graphene.Mutation):
    class Arguments:
        payment_type = graphene.String(required=True)
        amount = graphene.Float(required=True)
        reference = graphene.String(required=True)
        job_id = graphene.ID(required=True)

    payment = graphene.Field(PaymentType)

    def mutate(self, info, payment_type, amount, reference, job_id):
        job = Job.objects.get(pk=job_id)
        payment = Payment.objects.create(payment_type=payment_type, amount=amount, reference=reference, job=job)
        return CreatePayment(payment=payment)

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    payments = graphene.List(PaymentType)
    jobs = graphene.List(JobType)
    clients = graphene.List(ClientType)
    tasks = graphene.List(TaskType)

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_payments(self, info):
        return Payment.objects.all()

    def resolve_jobs(self, info):
        return Job.objects.all()

    def resolve_clients(self, info):
        return Client.objects.all()

    def resolve_tasks(self, info):
        return Task.objects.all()

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_payment = CreatePayment.Field()

class MyQuery(graphene.ObjectType):
    my_field = graphene.String()

    @login_required
    def resolve_my_field(self, info):
        user = info.context.user
        return 'Hello, {}'.format(user.username)


schema = graphene.Schema(query=Query, mutation=Mutation)
