import graphene
import json
import uuid
from datetime import datetime


class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()


class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return 'http://cloudinary.com/{}/{}'.format(self.username, self.id)


class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return "world"

    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info, limit=None):
        # None is a fallback value in case a limit is is passed.  hence, making limit optional.
        return [
            User(id="1", username="Fred", created_at=datetime.now()),
            User(id="2", username="George", created_at=datetime.now()),
            User(id="3", username="Maddie", created_at=datetime.now())
        ][:limit]


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        user = User(username=username)
        return CreateUser(user=user)


class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title, content):
        if info.context.get('is_anonymous'):
            raise Exception('Not authenticated!')
        post = Post(title=title, content=content)
        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
#  auto_camelcase=False, pass as 2nd argument in query as the autocamelcase false allows the bellow is_admin to be written in snake case

# ! means it is required

result = schema.execute(
    '''
        query {
        users(limit: 1) {
            id
            username
            createdAt
            avatarUrl
        }
    }
    '''
    
)

# mutation {
#         createPost(title: "Hello", content: "World") {
#             post {
#                 title
#                 content
#             }
#         }
#     }
# ''',
# context={ 'is_anonymous': False}

#   query {
#         users(limit: 1) {
#             id
#             username
#             createdAt
#         }
#     }

#  query getUsersQuery ($limit: Int) {
#         users(limit: $limit) {
#             id
#             username
#             createdAt
#         }
#     }
#     ''',
#     variable_values={'limit': '1'}

#   {
#     mutation ($username: String) {
#         createUser(username: $username) {
#             user {
#                 id
#                 username
#                 createdAt
#             }
#         }
#     }
# }

dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))

# print(result.data.items())
# print(result.data['hello'])
