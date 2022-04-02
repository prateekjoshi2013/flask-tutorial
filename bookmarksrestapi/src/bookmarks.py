from flask import Blueprint,request,jsonify
import validators
from http import HTTPStatus
from src.database import Bookmark,db
from flask_jwt_extended import get_jwt_identity,jwt_required


bookmarks=Blueprint("bookmarks",__name__,url_prefix='/api/v1/bookmarks')

@bookmarks.route('/',methods=['POST','GET'])
@jwt_required()
def handle_bookmarks():
    current_user=get_jwt_identity()
    if request.method=='POST':
        body=request.get_json().get('body','')
        url=request.get_json().get('url','')
        if not validators.url(url):
            return jsonify({
                "error":'Enter a valid url'
            }),HTTPStatus.BAD_REQUEST.value
        if Bookmark.query.filter_by(url=url).first() is not None:
            return jsonify({
                "error":"url already exists"
            }),HTTPStatus.CONFLICT.value
        bookmark=Bookmark(url=url,body=body,user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()
        return jsonify({
            'url':bookmark.url,
            'short_url':bookmark.short_url,
            'id':bookmark.id,
            'visits':bookmark.visits,
            'body':bookmark.body,
            'created_at':bookmark.created_at,
            'updated_at':bookmark.updated_at,
        }),HTTPStatus.CREATED.value
    else:
        page=request.args.get('page',1,type=int)
        per_page=request.args.get('per_page',5,type
        =int)
        bookmarks=Bookmark.query.filter_by(
            user_id=current_user).paginate(
                page=page,per_page=per_page)
        data=[]
        for bookmark in bookmarks.items:
            data.append({
            'url':bookmark.url,
            'short_url':bookmark.short_url,
            'id':bookmark.id,
            'visit':bookmark.visits,
            'body':bookmark.body,
            'created_at':bookmark.created_at,
            'updated_at':bookmark.updated_at,
        })
        meta ={
            "page":bookmarks.page,
            "pages":bookmarks.pages,
            "total_count":bookmarks.total,
            "prev_page":bookmarks.prev_num,
            "next_page":bookmarks.next_num,
            "has_next": bookmarks.has_next,
            "has_prev": bookmarks.has_prev
        }
        return jsonify({'data':data , "meta":meta}),HTTPStatus.OK.value


@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    curent_user=get_jwt_identity()
    bookmark=Bookmark.query.filter_by(user_id=curent_user,id=id).first()
    if not bookmark:
        return jsonify({'message':'Item not found'}),HTTPStatus.NOT_FOUND.value
    return jsonify({
            'url':bookmark.url,
            'short_url':bookmark.short_url,
            'id':bookmark.id,
            'visit':bookmark.visits,
            'body':bookmark.body,
            'created_at':bookmark.created_at,
            'updated_at':bookmark.updated_at,
        }),HTTPStatus.FOUND.value

@bookmarks.put('/<int:id>')
@bookmarks.patch('/<int:id>')
@jwt_required()
def  edit_bookmark(id):
    curent_user=get_jwt_identity()
    bookmark=Bookmark.query.filter_by(user_id=curent_user,id=id).first()
    if not bookmark:
        return jsonify({'message':'Item not found'}),HTTPStatus.NOT_FOUND.value
    body=request.get_json().get('body','')
    url=request.get_json().get('url','')
    if not validators.url(url):
        return jsonify({
            "error":'Enter a valid url'
        }),HTTPStatus.BAD_REQUEST.value
    bookmark.url=url
    bookmark.body=body
    db.session.commit()
    return jsonify({
            'url':bookmark.url,
            'short_url':bookmark.short_url,
            'id':bookmark.id,
            'visit':bookmark.visits,
            'body':bookmark.body,
            'created_at':bookmark.created_at,
            'updated_at':bookmark.updated_at,
        }),HTTPStatus.OK.value


@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    curent_user=get_jwt_identity()
    bookmark=Bookmark.query.filter_by(user_id=curent_user,id=id).first()
    if not bookmark:
        return jsonify({'message':'Item not found'}),HTTPStatus.NOT_FOUND.value
    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({}),HTTPStatus.NO_CONTENT.value


@bookmarks.get('/stats')
@jwt_required()
def get_stats():
    data=[]
    user=get_jwt_identity()
    items=Bookmark.query.filter_by(user_id=user).all()
    for item in items:
        new_link={
            'visits':item.visits,
            'url':item.url,
            'id':item.id,
            'short_url':item.short_url
        }
        data.append(new_link)
    return jsonify({'data':data}),HTTPStatus.OK.value
    