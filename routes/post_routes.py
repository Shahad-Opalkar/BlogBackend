from flask import Blueprint,request,jsonify
from model import db,Post,User
from schemas import PostSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.role_guard import role_required
from exceptions import NotFoundError,ForbiddenError,BadRequestError



post_bp = Blueprint("post",__name__)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@post_bp.route("/posts", methods=["POST"])
@jwt_required()
@role_required(["author", "admin"])
def create_post():
        data = request.get_json()

        current_user_id = int(get_jwt_identity())   


        if not data.get("title") or not data.get("content"):
            raise BadRequestError("Missing required fields")

    

        new_post = Post(
        title=data["title"],
        content=data["content"],
        user_id=current_user_id )

        db.session.add(new_post)
        db.session.commit()

        return post_schema.jsonify(new_post), 201


@post_bp.route("/posts", methods=["GET"])
@jwt_required()
def get_posts():

    current_user_id = get_jwt_identity()   

    page = request.args.get("page", 1, type=int)

    limit = request.args.get("limit", 10, type=int)

    search = request.args.get("search", "", type=str)

    query = Post.query

    if search:
        query = query.filter(Post.title.ilike(f"%{search}%"))

    posts = query.paginate(
    page=page,
    per_page=limit,
    error_out=False
)

    return jsonify({
        "page": page,
        "limit": limit,
        "total_posts": posts.total,
        "total_pages": posts.pages,
        "posts": posts_schema.dump(posts.items)
    })

@post_bp.route("/my-posts",methods=["GET"])
@jwt_required()
def get_my_posts():
    current_user_id = get_jwt_identity()

    post = Post.query.filter_by(user_id=current_user_id).all()
    return posts_schema.jsonify(post),200

@post_bp.route("/users/<int:user_id>/posts", methods=["GET"])
@jwt_required()
def get_user_posts(user_id):

    current_user_id = get_jwt_identity()   # 👈 ADD THIS HERE

    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("Post not found")

    posts = Post.query.filter_by(user_id=user_id).all()
    return posts_schema.jsonify(posts), 200

@post_bp.route("/posts/<int:post_id>",methods=["PUT"])
@jwt_required()
@role_required(["author", "admin"])
def update_post(post_id):
     current_user_id= int(get_jwt_identity())
     data=request.get_json()

     post = db.session.get(Post, post_id)
     if not post:
        if not post:
            raise NotFoundError("Post not found")
     
     if post.user_id != current_user_id:
        raise ForbiddenError()
     
     if data.get("title"):
        post.title = data["title"]
     if data.get("content"):
        post.content = data["content"]

     db.session.commit()

     return post_schema.jsonify(post), 200

     
@post_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required()
@role_required(["author", "admin"])
def delete_post(post_id):
    current_user_id = int(get_jwt_identity())

    post = Post.query.get(post_id)

    if not post:
        raise NotFoundError("Post not found")

    if post.user_id != current_user_id:
         raise ForbiddenError()

    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted"}), 200
  