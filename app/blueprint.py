from .ess_status.blueprint import ess_status



def register(app):
    app.register_blueprint(ess_status)


    return
