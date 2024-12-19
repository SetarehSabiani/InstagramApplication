import json
import requests


def get_post_list():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    if response.ok:
        data = json.loads(response.content)
        return data
    else:
        raise ValueError(response)


def create_post(title, body, user_id):
    response = requests.post("https://jsonplaceholder.typicode.com/posts", data={
        "title": title,
        "body": body,
        "userId": user_id

    })

    if response.ok:
        return True
    else:
        False


def update_post(post_id, new_title, new_body):
    response = requests.put(f"https://jsonplaceholder.typicode.com/posts/{post_id}", data={
        "title": new_title,
        "body": new_body

    })


def delete_post(post_id):
    response = requests.delete(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    return response.ok


def get_comment_list(post_id):
    response = requests.get(f"https://jsonplaceholder.typicode.com/comments?postId={post_id}")

    if response.ok:
        comments = json.loads(response.content)
        return comments
