from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_book_data(data):
    """Validate a single post payload.
    Expects a dict with at least 'title' and 'content' keys.
    Returns True if valid, False otherwise.
    """
    if not isinstance(data, dict):
        return False
    if "title" not in data or "content" not in data:
        return False
    return True


@app.route('/api/posts', methods=['GET'])
def get_posts():
    # Validate each post dict before returning. Do NOT pass a Response to the validator.
    invalid_posts = [p for p in POSTS if not validate_book_data(p)]
    if invalid_posts:
        return jsonify({
            "error": "Invalid post data on server",
            "invalid_ids": [p.get("id") for p in invalid_posts]
        }), 500
    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)