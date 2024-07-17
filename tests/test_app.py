# tests/test_app.py
import unittest
import os
from app import TimelinePost, app

os.environ['TESTING'] = 'true'

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        TimelinePost.delete().execute()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
    
        # Check profile and about me sections
        self.assertIn('Vignesh Suresh Kumar', html)
        self.assertIn('Software Developer & Junior @ Georgia Tech', html)
        self.assertIn('src="./static/img/profile.png"', html)
        self.assertIn('mailto:vignesh.sureshkumar@gatech.edu', html)

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

    def test_timeline_page(self):
        # Request the timeline page
        response = self.client.get("/timeline")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('<h1 class="title">Timeline</h1>', html)  # Checks if the Timeline header is present
        self.assertIn('Add To Timeline', html)  # Checks for form header
        self.assertIn('name="timeline_form"', html)  # Form should be correctly named
        self.assertIn('action="/api/timeline_post"', html)  # Form action should be correct
        self.assertIn('method="post"', html)  # Form method should be POST
        
    # Test the retrieval of the timeline posts
    def test_get_timeline_posts(self):
        TimelinePost.create(name="Test User", email="test@example.com", content="This is a test post.")

        # Now test retrieving posts
        get_response = self.client.get("/api/timeline_post")
        assert get_response.status_code == 200
        assert get_response.is_json
        json_data = get_response.get_json()
        assert "timeline_posts" in json_data
        assert len(json_data["timeline_posts"]) > 0  # Ensure the post was added

    # Test creating and then immediately deleting a post
    def test_delete_timeline_post(self):
        # First create a new post
        self.client.post("/api/timeline_post", data={
            "name": "Delete User",
            "email": "delete@example.com",
            "content": "Delete this post."
        })
        # Fetch the posts to find the latest
        posts_before_delete = self.client.get("/api/timeline_post").get_json()
        latest_post_id = posts_before_delete['timeline_posts'][0]['id']

        # Now delete the latest post
        delete_response = self.client.delete(f"/api/timeline_post/latest")
        assert delete_response.status_code == 200
        assert delete_response.is_json

        # Check the post is actually deleted
        posts_after_delete = self.client.get("/api/timeline_post").get_json()
        assert len(posts_after_delete['timeline_posts']) == len(posts_before_delete['timeline_posts']) - 1
        
    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

if __name__ == '__main__':
    unittest.main()
