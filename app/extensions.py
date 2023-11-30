from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
# migrate = Migrate(include_schemas=True)
migrate = Migrate()

