import graphene
from blogbackend.app.post import Query as PostQuery

class Query(
    PostQuery
):
    pass


# class Mutation(
#     ConferenceMutation,
#     TalkMutation,
#     HumanMutation,
#     TagMutation
# ):
#     pass


schema = graphene.Schema(query=Query)
# schema = graphene.Schema(query=Query, mutation=Mutation)