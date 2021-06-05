import graphene
from graphene_django import DjangoObjectType

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


# define mutation class
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    # defines data you can send to the server
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    # this is the mutation method. it creates a link in the DB and then returns the CreateLink class with the data just created
    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        link.save()

        # returns field by field
        return CreateLink(id=link.id, url=link.url, description=link.description)


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()


# create a mutation class with a field to be resolved, which points to our mutation defined above
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
