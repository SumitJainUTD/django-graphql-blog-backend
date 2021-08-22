import graphene
from .post.schema import Query as PostQuery
from .users.schema import Query as UserQuery
from .post.schema import Mutation as PostMutation
from .users.schema import Mutation as UserMutation


class Query(
    PostQuery,
    UserQuery
):
    pass


class Mutation(
    PostMutation,
    UserMutation,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
