from api.domain.status_response import StatusResponse

"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : server_response.py
Purpose         : -
"""


class ServerReponse(object):
  statusResponse: StatusResponse
  body: any

  def __init__(self, statusResponse, body):
    self.statusResponse = statusResponse
    self.body = body