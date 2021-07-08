from graphene.types import mutation
from .models import Post as PostModel
from graphene_django import DjangoObjectType
import graphene
from django.contrib.auth.models import User
import uuid

class PostNode(DjangoObjectType):
    class Meta:
        model = PostModel

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    posts = graphene.List(PostNode, id=graphene.String(), first=graphene.Int(), skip=graphene.Int())

    def resolve_posts(self, info, **kwargs):
        posts = PostModel.objects.none()
        first = kwargs.get("first")
        skip = kwargs.get("skip")
        post_id = kwargs.get("id")
        if post_id is not None:
            posts = PostModel.objects.filter(id=post_id)
        else:
            posts = PostModel.objects.all()

        if skip:
            posts = posts[skip:]
        if first:
            posts = posts[:first]
        return posts

class UserInput(graphene.InputObjectType):
    id = graphene.String()

class PostInput(graphene.InputObjectType):
    id = graphene.String()
    title = graphene.String()
    content = graphene.String()
    user_id = graphene.String()

class CreatePost(graphene.Mutation):
    class Arguments:
        post = PostInput(required=True)

    post = graphene.Field(PostNode)

    @staticmethod
    def mutate(root, info, post=None):
        author = User.objects.filter(id=post.user_id).first()
        print(author)
        post_instance = PostModel(
            id=uuid.uuid4(),
            title=post.title,
            content=post.content,
            author = author
        )
        post_instance.save()
        
        return CreatePost(post=post_instance)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)