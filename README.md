**Sample Blog backend using Django Rest Framework and JWT**
1. Clone/Download the repo
2. Create virtual env using following steps
3. sudo pip3 install virtualenv  (if virtualenv is not installed)
   
    3.1 Create virtual env by 
**virtualenv venv --python=python3**
   
   3.2 Activate the virtual env **source venv/bin/activate** 
4. Do pip install -r requriements.txt
5. cd blog
6. python manage.py makemigrations
7. python manage.py migrate
8. pyhton manage.py runserver 8000
9. user/pwd
    9.1 test/test

Your app is running on now http://127.0.0.1:8000/

End points: 
1. admin - http://127.0.0.1:8000/admin
2. query posts: http://127.0.0.1:8000/graphql
   Request:
   ```
      query{
        posts{
          id
          title
          datePosted
          content
          author{
            username
            firstName
            lastName
          }
        }
      }  
   ```
   Response: 
   ```
      {
     "data": {
       "posts": [
         {
           "id": "fd3c607e-0af1-4179-8424-51d2f04373ad",
           "title": "first post",
           "datePosted": "2021-08-22T22:21:48.911237+00:00",
           "content": "content",
           "author": {
             "username": "user1",
             "firstName": "",
             "lastName": ""
           }
         },
         {
           "id": "be1c73cd-6262-4fce-bfe3-ca1654f714f2",
           "title": "second post",
           "datePosted": "2021-08-22T23:32:49.040204+00:00",
           "content": "content",
           "author": {
             "username": "user1",
             "firstName": "",
             "lastName": ""
           }
         }
         }
       ]
     }
   }
    ```
3. register: http://127.0.0.1:8000/graphql
   ```
      mutation{
        register(
          email:"d@d.com",
          username: "user3"
          password1: "testing321",
          password2: "testing321"
        ){
          success
          errors
          token
          refreshToken
        }
      }
   ```
   Response: 
   ```
    {
     "data": {
       "register": {
         "success": true,
         "errors": null,
         "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIzIiwiZXhwIjoxNjMwMjE1NTgzLCJvcmlnSWF0IjoxNjMwMjE1MjgzfQ.J5j4o_vrKMdOs2kxaDLRXY1MZzXYbWM0pcLIDCC4OoU",
         "refreshToken": "6fd16b6e0d5e8a16994adb1f7f58148867b666d7"
       }
     }
   }
   ```
4. get token/login: 
```
mutation{
  tokenAuth(
    email:"a@a.com",
    password: "testing321"){
    
    token,
    refreshToken,
    success
    errors
  }
}
```
Response:
```
{
  "data": {
    "tokenAuth": {
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIyIiwiZXhwIjoxNjMwMjE1Njk4LCJvcmlnSWF0IjoxNjMwMjE1Mzk4fQ.rYdI16zXij5bl8wPYfCochcORR6IDAVjf0cljOkkHHo",
      "refreshToken": "d55ebd6447206a6f107a0caceda35ddd67b69ba6",
      "success": true,
      "errors": null
    }
  }
}
```
5. refresh token:
```
mutation{
  refreshToken(refreshToken:"15077bcfb121f770c8dec19df2e4548529cd7fd5"){
    token
    refreshToken
    success
    errors
  }
}
```
6. logout
```
mutation{
  logout(refreshToken:"15077bcfb121f770c8dec19df2e4548529cd7fd5"){
    success
  }
}
```
7. create post:   
```
curl --location --request POST 'http://127.0.0.1:8000/graphql' \
--header 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InJ5YW5TdWthbGUiLCJleHAiOjE2MzAxNjQ1MjYsIm9yaWdJYXQiOjE2MzAxNjQyMjZ9.TgcD-abxR7YHZgUrohmgKE7fx1Whl-rFbTKWNh_2Nps' \
--header 'Content-Type: application/json' \
--data-raw '{"query":"mutation{\n  createPost(post:{\n    title: \"fourth post\",\n    content: \"content\",\n  }){\n    post {\n      id\n    }\n  }\n}","variables":{}}'
}'
```

For more auth end points and features - https://django-graphql-auth.readthedocs.io/en/latest/quickstart/



