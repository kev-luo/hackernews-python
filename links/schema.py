import graphene
from graphene_django import DjangoObjectType

from .models import Link, Vote
from users.schema import UserType
from graphql import GraphQLError
from django.db.models import Q


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote


# define mutation class
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    # defines data you can send to the server
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    # this is the mutation method. it creates a link in the DB and then returns the CreateLink class with the data just created
    def mutate(self, info, url, description):
        user = info.context.user or None
        link = Link(url=url, description=description, posted_by=user)
        link.save()

        # returns field by field
        return CreateLink(id=link.id, url=link.url, description=link.description, posted_by=link.posted_by)


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            # raise Exception("You must be logged in to vote!")
            raise GraphQLError("You must be logged in to vote!")

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception("Could not find link!")

        Vote.objects.create(user=user, link=link)

        return CreateVote(user=user, link=link)


class Query(graphene.ObjectType):
    links = graphene.List(LinkType, search=graphene.String())
    votes = graphene.List(VoteType)

    def resolve_links(self, info, search=None, **kwargs):
        # the value sent with the search param will be in the args variable
        if search:
            filter = Q(url__icontains=search) | Q(description__icontains=search)
            return Link.objects.filter(filter)
        return Link.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()


# create a mutation class with a field to be resolved, which points to our mutation defined above
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
