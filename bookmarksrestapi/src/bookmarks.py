from flask import Blueprint,request,jsonify
import validators
from http import HTTPStatus
from src.database import Bookmark,db
from flask_jwt_extended import get_jwt_identity,jwt_required


bookmarks=Blueprint("bookmarks",__name__,url_prefix='/api/v1/bookmarks')

@bookmarks.route('/',methods=['POST','GET'])
@jwt_required()
def handle_bookmarks():
    import pdb
    pdb.set_trace()
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
        bookmarks=Bookmark.query.filter_by(user_id=current_user)
        data=[]
        pdb.set_trace()
        for bookmark in bookmarks:
            data.append({
            'url':bookmark.url,
            'short_url':bookmark.short_url,
            'id':bookmark.id,
            'visit':bookmark.visits,
            'body':bookmark.body,
            'created_at':bookmark.created_at,
            'updated_at':bookmark.updated_at,
        })
        return jsonify({'data':data}),HTTPStatus.OK.value