import os

from flask import render_template, request, redirect, Blueprint, jsonify
from scrapyd_api import ScrapydAPI

pro = Blueprint('pro', __name__)

scrapyd = ScrapydAPI("http://47.102.139.195:6800/")


@pro.route('/')
def index():  # put prolication's code here
    return render_template('index.html')


@pro.route('/projects/')
def show_projects():  # put prolication's code here
    projects_info = []
    projects = scrapyd.list_projects()
    for i in range(len(projects)):
        spiders = scrapyd.list_spiders(projects[i])
        dic = {
            'id': i + 1,
            'project_name': projects[i],
            'spiders_name': spiders,
            'count': len(spiders)
        }
        projects_info.append(dic)
    return render_template('projects.html', projects_info=projects_info)


@pro.route('/del_project/<project_name>/', methods=['get', 'post'])
def del_project(project_name):
    scrapyd.delete_project(project_name)
    return redirect('/projects/')


@pro.route('/deploy/', methods=['get', 'post'])
def deploy_project():
    res = {'status': True, 'message': None}
    try:
        project_path = request.form.get('project_path')
        project_name = request.form.get('project_name')
        spider_name = request.form.get('spider_name')
        print(project_path, project_name, spider_name)
    except Exception as e:
        res['status'] = False
        res['message'] = '%s' % e
    return jsonify(res)


@pro.route('/test/', methods=['get', 'post'])
def test():
    p = jsonify(os.popen('curl http://47.102.139.195:6800/listprojects.json').read())
    return p