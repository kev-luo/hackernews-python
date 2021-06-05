import graphene

import links.schema

# this Query class inherits from the links schema
# this keeps every part of the schema isolated in the apps
class Query(links.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
