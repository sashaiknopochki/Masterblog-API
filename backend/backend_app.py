from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_book_data(data):
    """Validate a single post-payload.
    Expects a dict with at least 'title' and 'content' keys.
    Returns True if valid, False otherwise.
    """
    if not isinstance(data, dict):
        return False
    if "title" not in data or "content" not in data:
        return False
    return True


@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    # POST - Add a new post
    if request.method == 'POST':
        data = request.get_json()
        if not validate_book_data(data):
            return jsonify({"error": "Invalid post data"}), 400

        # Auto-generate ID for the new post
        new_id = max([post["id"] for post in POSTS], default=0) + 1
        data["id"] = new_id

        POSTS.append(data)
        return jsonify(data), 201

    # GET - Return all posts
    invalid_posts = [post for post in POSTS if not validate_book_data(post)]
    if invalid_posts:
        return jsonify({
            "error": "Invalid post data on server",
        }), 500
    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)