import os
from app import create_app
from flasgger import Swagger

app = create_app(os.getenv('ENV'))

Swagger(app, template_file="docs.yml")

if __name__ == '__main__':
    app.run()
