#!/usr/bin/env python
from django.shortcuts import HttpResponse, render, redirect
from tools.sqlmanage import sql_get_all, sql_get_one, sql_run
import json


# ---------------------------------班级管理---------------------------------

# 显示班级
def show_class(request):
    class_dict = sql_get_all('select*from class')
    return render(request, 'show_class.html', {'class_dict': class_dict})


# 在新页面添加班级
def add_class(request):
    if request.method == 'POST':
        classname = request.POST.get('cname')
        sql_run("insert into class(name) values (%s)", (classname,))
        return redirect('/show_class/')  # 转到url
    else:
        return render(request, 'add_class.html')  # 渲染一个页面


# 新页面编辑班级
def edit_class(request):
    if request.method == 'POST':
        cid = request.POST.get('cid')  # 值是通过隐藏框设置name值即class的id传来
        cname = request.POST.get('cname')
        sql_run("update class set name=%s where id=%s", [cname, cid])
        return redirect('/show_class/')
    else:
        cid = request.GET.get('cid')
        class_dict = sql_get_one("select * from class where id=%s", (cid,))
        return render(request, 'edit_class.html', {'class_dict': class_dict})


# 删除班级
def del_class(request):
    cid = request.GET.get('cid')
    sql_run("delete from class where id = %s", [cid])
    return redirect('/show_class/')


# 模态框添加班级
def modal_add_class(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        # 表单验证，添加班级是否为空
        if cname:
            sql_run("insert into class(name) values(%s)", (cname,))
            return HttpResponse('OK')
        else:
            error = '班级名不能为空'
            return HttpResponse(error)


# 模态框编辑班级
def modal_edit_class(request):
    if request.method == 'POST':
        classId = request.POST.get('classId')
        className = request.POST.get('className')
        if className:
            sql_run('update class set name=%s where id=%s', (className, classId))
            return HttpResponse('OK')
        else:
            error = '班级名不能为空'
            return HttpResponse(error)


# 用sweetalert删除
def alert_del_class(request):
    if request.method == 'POST':
        classId = request.POST.get('classId')
        try:
            sql_run("delete from class where id = %s", (classId,))
            ret = {"status": 0, "msg": "你可以准备跑路了"}
        except Exception as e:
            ret = {"status": 1, "msg": str(e)}
        return HttpResponse(json.dumps(ret))


# ---------------------------------教师管理---------------------------------


# 显示老师列表
def show_teacher(request):
    teacher_dict = sql_get_all('select*from teacher')
    return render(request, 'show_teacher.html', {'teacher_dict': teacher_dict})


# 新页面添加教师
def add_teacher(request):
    if request.method == 'POST':
        tname = request.POST.get('tname')
        sql_run("insert into teacher(name) values (%s)", (tname,))
        return redirect('/show_teacher/')
    else:
        return render(request, 'add_teacher.html')


# 新页面编辑教师
def edit_teacher(request):
    if request.method == 'POST':
        tid = request.POST.get('tid')  # 值是通过隐藏框设置name值即class的id传来
        tname = request.POST.get('tname')
        sql_run("update teacher set name=%s where id=%s", [tname, tid])
        return redirect('/show_teacher/')
    else:
        tid = request.GET.get('tid')
        teacher_dict = sql_get_one("select * from teacher where id=%s", (tid,))
        return render(request, 'edit_teacher.html', {'teacher_dict': teacher_dict})

    # 删除教师
    cid = request.GET.get('cid')
    sql_run("delete from class where id = %s", (cid,))
    return redirect('/show_class/')


# 删除教师
def del_teacher(request):
    tid = request.GET.get('tid')
    sql_run("delete from teacher where id = %s", [tid])
    return redirect('/show_class/')


# 模态框添加教师
def modal_add_teacher(request):
    if request.method == 'POST':
        tname = request.POST.get('tname')
        # 表单验证，添加班级是否为空
        if tname:
            sql_run("insert into teacher(name) values(%s)", (tname,))
            return HttpResponse('OK')
        else:
            error = '教师名不能为空'
            return HttpResponse(error)


# 模态框编辑教师
def modal_edit_teacher(request):
    if request.method == 'POST':
        teacherId = request.POST.get('teacherId')
        teacherName = request.POST.get('teacherName')
        if teacherName:
            sql_run('update teacher set name=%s where id=%s', (teacherName, teacherId))
            return HttpResponse('OK')
        else:
            error = '教师名不能为空'
            return HttpResponse(error)


# 用sweetalert删除
def alert_del_teacher(request):
    if request.method == 'POST':
        teacherId = request.POST.get('teacherId')
        try:
            sql_run("delete from teacher where id = %s", (teacherId,))
            ret = {"status": 0, "msg": "你可以准备跑路了"}
        except Exception as e:
            ret = {"status": 1, "msg": str(e)}
        return HttpResponse(json.dumps(ret))


# ---------------------------------教师管理---------------------------------


# 查看学生
def show_student(request):
    # student.class_id也取出来用于模态框设置默认班级
    sql = 'select student.id,student.name,student.class_id, class.name as classname from student left join class on student.class_id = class.id'
    student_dict = sql_get_all(sql)
    class_dict=sql_get_all('select * from class')
    return render(request, 'show_student.html', {'student_dict': student_dict,'class_dict':class_dict})


# 添加学生信息
def add_student(request):
    if request.method == "POST":

        student_name = request.POST.get("student_name")
        class_id = request.POST.get("class_id")
        sql_run("insert into student(name, class_id) VALUES (%s, %s)", [student_name, class_id] )
        return redirect("/show_student/")

    else:

        class_dict=sql_get_all('select id, name from class')
        return render(request, "add_student.html", {"class_dict": class_dict})


# 修改学生信息
def edit_student(request):
    error = ""
    if request.method == "POST":
        student_name = request.POST.get("student_name")
        if student_name:
            class_id = request.POST.get("class_id")
            # 从URL里面获取参数的值↓
            student_id = request.GET.get("student_id")
            # 更新数据库里面的对应学生的信息
            sql_run("update student set name=%s, class_id=%s where id=%s", [student_name, class_id, student_id])
            return redirect("/show_student/")
        else:
            error = "学生姓名不能为空"

    class_dict = sql_get_all("select id, name from class")
    # 查找到当前修改的学生的信息
    # URL里面的参数，使用request.GET.get("k1")
    student_id = request.GET.get("sid")
    # 取数据库里面查
    student_record =sql_get_one("select id, name, class_id from student where id=%s", [student_id,])

    return render(request, "edit_student.html", {"class_dict": class_dict, "student": student_record,"error": error})


# 删除学生信息
def del_student(request):
    sid=request.GET.get('sid')
    sql_run('delete from student where id=%s',[sid])
    return redirect('/show_student/')


# 专门处理模态框添加学生信息
def modal_add_student(request):
    if request.method == "POST":
        student_name = request.POST.get("student_name")
        if student_name:
            class_id = request.POST.get("class_id")
            # 存到数据库
            sql_run("insert into student (name, class_id) VALUES (%s, %s)", [student_name, class_id])
            ret = {"status": 0, "msg": "添加成功"}
        else:
            ret = {"status": 1, "msg": "学生姓名不能为空"}
        return HttpResponse(json.dumps(ret))


# 专门处理模态框编辑学生信息
def modal_edit_student(request):
    if request.method == "POST":
        print(request.POST)
        student_id = request.POST.get("student_id")
        student_name = request.POST.get("student_name")
        if student_name:
            class_id = request.POST.get("class_id")
            # 更新学生信息到数据库
            sql_run("update student set name=%s, class_id=%s where id=%s", [student_name, class_id, student_id])
            ret = {"status": 0, "msg": "编辑成功"}
        else:
            ret = {"status": 1, "msg": "学生姓名不能为空"}
        return HttpResponse(json.dumps(ret))


# 删除专用函数
def modal_del_student(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        try:
            sql_run("delete from student where id=%s", [student_id])
            ret = {"status": 0, "msg": "你可以准备跑路了"}
        except Exception as e:
            ret = {"status": 1, "msg": str(e)}
        return HttpResponse(json.dumps(ret))