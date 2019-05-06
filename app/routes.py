from app import app
from flask import render_template, flash, redirect
from app.forms.postForm import PostForm
import requests
from func_pack import create_rec_hash, get_current_time, get_api_info
from config import Config
# CPU 泄露函数
import fault_func as ff
import logging


@app.route('/cpu-err-injection', methods=['POST'])
def post():
    form = PostForm()
    # 处理 POST 的逻辑
    if form.validate_on_submit():
        # 点击发言按钮后, 注入 500mb 的内存泄露
        #ret = ff.fault_injection()
        #flash(ret)
        flash('no fault')
        return redirect('/cpu-err-injection')


# 获取最新评论消息
@app.route('/cpu-err-injection', methods=['GET'])
def welcome():
    form = PostForm()
    queries_list = [
        {
            "Username": "Leon_Tian",
            "Post": "Click the button upside and you can inject CPU error to your host.",
            "PostTime": "2019-04-27/15:34:09"
        }
    ]
    # 处理 GET 的逻辑
    return render_template('frontPage.html', title='CPU Err Injection', comments=queries_list, form=form)
#
#
# # 获取 username 为 admin 的用户所发出的信息
# @app.route('/announcement', methods=['GET'])
# def announcement():
#     query_url = 'http://' + Config.DB_CONNECTOR_URL + '/queries/' + 'Administer'
#     # 获取最新的 comments 信息
#     result = requests.get(query_url)
#     queries_list = get_api_info(result)
#     # 逆序，将最新的留言放置最前
#     queries_list.reverse()
#     # 处理 GET 的逻辑
#     return render_template('announcement.html', title='Rules', comments=queries_list)
#     pass


