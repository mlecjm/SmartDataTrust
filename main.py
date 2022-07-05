import sys
from flask import Flask
from pathlib import Path
from api.bootstrap import Bootstrap

from api.controller.consent_controller import consent
from api.controller.data_subject_controller import data_subject
from api.controller.data_access_request_controller import data_access_request
from api.controller.data_access_response_controller import data_access_response

from tests.controller.responder_controller import responder
from tests.controller.requester_controller import requester

def create_app():
  path = Path().absolute()
  Bootstrap(path)

  app = Flask(__name__)

  app.register_blueprint(consent)
  app.register_blueprint(data_subject)
  app.register_blueprint(data_access_request)
  app.register_blueprint(data_access_response)

  app.register_blueprint(requester)
  app.register_blueprint(responder)

  return app


if __name__ == '__main__':
  try:
    port = int(sys.argv[1])
  except Exception:
    port = 8081

  create_app().run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
