from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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


def find_index_post(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None


@app.get("/")
def root():
    return {"message": "Hello World"}


# generate crud logic of post(include get all of the post), but not include rating
@app.post("/posts")
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1_000_000)
    my_posts.append(post)
    return post


@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    print(type(id))
    # filter and find first post by id
    post = find_post_by_id(id)
    if not post:
        raise HTTPException(status_code=404, detail=f"post not found with id: {id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "post not found with id: {id}"}
    return {"post_detail": post}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    curr_post = find_post_by_id(id)
    if not curr_post:
        raise HTTPException(status_code=404, detail=f"post not found with id: {id}")
    # if curr_post != None:
    #     curr_post = post
    #     curr_post.id = id
    #     return curr_post
    my_posts.index(curr_post)["title"] = post.title
    my_posts.index(curr_post)["id"] = id
    return curr_post


@app.delete("/posts/{id}")
async def delete_post(id: int):
    index = find_index_post(id)
    return my_posts.pop(index)


@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"post_detail": post}
