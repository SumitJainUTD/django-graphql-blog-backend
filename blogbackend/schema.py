import graphene
from blogbackend.app.post import Query as PostQuery

class Query(
    PostQuery
):
    pass

schema = graphene.Schema(query=Query)