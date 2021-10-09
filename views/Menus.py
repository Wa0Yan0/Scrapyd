import paramiko
from flask import Flask, render_template, request, redirect, url_for, Blueprint, jsonify

menu = Blueprint('menu', __name__)


@menu.route("/menus/list")
def menus_list():
    return jsonify([
        {
            'id': 101,
            "name": "系统管理",
            "path": "",
            "icon": "fa fa-cog fa-5",
            "children": [
                {
                    'id': 104,
                    "name": "用户管理",
                    "path": "/user",
                    "children": []
                },
                {
                    'id': 105,
                    "name": "菜单管理",
                    "path": "/menus",
                    "children": []
                }
            ]
        },
        {
            'id': 102,
            "name": "日志管理",
            "path": "",
            "icon": "fa fa-file-text-o",
            "children": [
                {
                    'id': 106,
                    "name": "日志列表",
                    "path": "/logs",
                    "children": []
                },
                {
                    'id': 107,
                    "name": "日志报告",
                    "path": "/report",
                    "children": []
                }
            ]
        }
    ])