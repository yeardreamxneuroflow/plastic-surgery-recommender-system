import marqo


mq = marqo.Client("http://localhost:8882")
settings = {
    "treat_urls_and_pointers_as_images": True,
    "model": "ViT-L/14",
}
indexes = ["left-eye", "right-eye", "nose", "lips"]

for index in indexes:
    response = mq.create_index(index, **settings)
    print(response)
