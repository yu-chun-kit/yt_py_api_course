from random import randrange
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


my_posts = [
    # Post(id=1, title="Post Title 1", content="Post Content 1", published=False),
    {"id": 1, "title": "Post Title 1", "content": "Post Content 1", "published": False},
    # Post(id=2, title="Post Title 2", content="Post Content 2", published=False),
    {"id": 2, "title": "Post Title 2", "content": "Post Content 2", "published": False},
]


def find_post_by_id(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None


# generate crud logic of post(include get all of the post), but not include rating
@app.post("/posts")
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1_000_000)
    # post_dict["id"] = len(my_posts)
    my_posts.append(post)
    return post


@app.get("/posts/{id}")
async def get_post(id: int):
    print(type(id))
    # filter and find first post by id
    post = find_post_by_id(id)
    if post != None:
        return {"post_detail": post}
    return {"error": "post not found"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    curr_post = find_post_by_id(id)
    if curr_post != None:
        curr_post = post
        curr_post.id = id
        return curr_post
    return {"error": "post not found"}


@app.delete("/posts/{id}")
async def delete_post(id: int):
    return my_posts.pop(id)


@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"post_detail": post}