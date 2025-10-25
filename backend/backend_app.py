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


@app.route('/api/posts/<int:id>', methods=['DELETE', 'PUT'])
def handle_post(id):
    # Find the post with the given id
    post = next((post for post in POSTS if post["id"] == id), None)
    if post is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    if request.method == 'DELETE':
        return delete_post(post)
    elif request.method == 'PUT':
        return update_post(post)
    return None


def delete_post(post):
    """Delete a post."""
    POSTS.remove(post)
    return jsonify({
        "message": f"Post with id {post['id']} has been deleted successfully."
    }), 200


def update_post(post):
    """Update a post."""
    data = request.get_json()

    # Check if request has valid JSON
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Update only the fields that are provided
    if 'title' in data:
        post['title'] = data['title']
    if 'content' in data:
        post['content'] = data['content']

    return jsonify(post), 200


@app.route('/api/posts/search')
def search_posts():
    title_query = request.args.get('title')
    content_query = request.args.get('content')

    # At least one search parameter must be provided
    if not title_query and not content_query:
        return jsonify({"error": "At least one query parameter required: 'title' or 'content'."}), 400

    search_results = []
    for post in POSTS:
        match = False
        if title_query and title_query.lower() in post['title'].lower():
            match = True
        if content_query and content_query.lower() in post['content'].lower():
            match = True

        if match:
            search_results.append(post)
        else:
            return jsonify({"error": "No posts found matching the search criteria."}), 404

    return jsonify(search_results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)