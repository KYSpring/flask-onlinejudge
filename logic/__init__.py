#-*-coding:utf-8-*-
import os
from flask import Flask,g
# url_for('pro_list', pro_class='structure')

def create_app(test_config = None):
    # create and configure the app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "kyspring123"
    app.config['DATABASE'] = 'myoj.db'
    # app.add_url_rule('/index',endpoint='user/index')
    import spider_func
    app.register_blueprint(spider_func.bp4)
    import login_and_register
    app.register_blueprint(login_and_register.bp)
    import user_function
    app.register_blueprint(user_function.bp2)
    import admin
    app.register_blueprint(admin.bp3)
    return app

if __name__ == "__main__":
    app = create_app().run(debug=True)
    # if hasattr(g, 'db'):
    #     g.db.close()

    @app.teardown_appcontext  # 在每次应用销毁时执行的装饰器
    def close_db(error):
        if hasattr(g, 'db'):
            g.db.close()
