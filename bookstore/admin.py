from models import Genre, Book, User, UserRole
from bookstore import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose
from flask import redirect
import utils
admin = Admin(app=app, name="Quản Trị Nhà Sách", template_mode="bootstrap4")


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class ProductView(AuthenticatedModelView):
    #tìm kiếm theo tên name, author
    column_searchable_list = ['name', 'author', 'theloai_id']
    #cho phép cột nào đc sắp xếp
    column_sortable_list = ['name', 'author', 'price']
    #bỏ cột
    column_exclude_list = ['active']


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')
    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html',
                           stats=utils.products_stats())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


admin.add_view(AuthenticatedModelView(Genre, db.session, name="Thể loại"))
admin.add_view(ProductView(Book, db.session, name="Sách"))
admin.add_view(StatsView(name='Thống kê doanh thu'))
admin.add_view(LogoutView(name='Đăng xuất'))
