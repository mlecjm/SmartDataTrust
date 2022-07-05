from api.util.singleton import Singleton

class Parameter(metaclass=Singleton):
  pseudonym: str
  consent_code: str
  consent_version: str
  responder_id: str

  request_id: str
  response_id: str
  data_transfer_url: str

  def __repr__(self):
    return "<Parameter(name={self.name!r})>".format(self=self)