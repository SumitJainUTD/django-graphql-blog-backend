from graphene.types import mutation
from .models import Post as PostModel
from graphene_django import DjangoObjectType
import graphene
from ..users.models import CustomUser as User
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


class CreatePost(graphene.Mutation):
    class Arguments:
        post = PostInput(required=True)

    post = graphene.Field(PostNode)

    @staticmethod
    def mutate(root, info, post=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        author = user  # User.objects.filter(id=post.user_id).first()
        print(user)
        post_instance = PostModel(
            id=uuid.uuid4(),
            title=post.title,
            content=post.content,
            author=author
        )
        post_instance.save()

        return CreatePost(post=post_instance)


class UpdatePost(graphene.Mutation):
    class Arguments:
        post = PostInput(required=True)

    post = graphene.Field(PostNode)

    @staticmethod
    def mutate(root, info, post=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        # check if user is authorized
        actual_post = PostModel.objects.filter(id=post.id)
        if actual_post:
            author = User.objects.filter(id=actual_post.user_id).first()
            print(user)
            print(author)
            if user != author:
                raise Exception('not authorized!')

            if post.title is not None:
                actual_post.title = post.title
            if post.content is not None:
                actual_post.content = actual_post.content,

            actual_post.save()
            return UpdatePost(post=actual_post)
        else:
            return UpdatePost(post=None)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
