"""app initializer """
from api import create_app

"""defining the configuration to be used and defining app instance"""
app = create_app(config="testing")

if __name__ == '__main__':
    app.run()
