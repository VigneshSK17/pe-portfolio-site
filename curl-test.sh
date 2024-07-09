#!/bin/bash

POST=$(curl -sS -X POST http://127.0.0.1:5000/api/timeline_post -d 'name=Vignesh&email=vigneshsureshkumar30@gmail.com&content=This is a random post from curl-test.sh')
echo "Created random post."

GET=$(curl -sS http://127.0.01:5000/api/timeline_post)
echo "Retrieved all posts."

if [[ "$GET" =~ "$POST" ]]; then
    echo "Random post successfully created."
else
    echo "Random post not created." >&2
    exit 1
fi

DELETE=$(curl -sS -X DELETE http://127.0.0.1:5000/api/timeline_post/latest)
echo "Post successfully deleted."
