from locust import HttpLocust, Locust, TaskSet, task, between, TaskSequence
import json
import base64

class OpenHomePage(TaskSet):
  """
  This first scenarios for load testing with client/user open application page.
Then get homepage from frontend application with API.
  """
  FAKE_UUID = "a240f6b2-2d32-11ea-978f-2e728ce88125"
  FAKE_TOKEN = "cBRizRaanQg:APA91bG9NnxDekifAnyPPDmVH8XtWC52s1ljUnp8cvqwuJR3Ko2JrB1XDUCNRu9_4GWWO4GsdTdOOtU8HHUwPLjkpB4xWx5bundSG5j4LQwiwmxzaS3O6Fkn9S2IxyCG9e3gK6CV8uqI"
  FAKE_USER_ID = "5dd615b6f343d37ad7da0080"

  @task(1)
  def openApp(self):
    headerSet = {"Brand": "","OS": "","Model": "","Install": "","UUID": ""}
    with self.client.get("/openapp", headers=headerSet, catch_response=True) as response:
      jdata = json.loads(response.content)
      if response.status_code != 200 and jdata['msg']['title'] != "normal":
        response.failure("Wrong Response, it should message title is \"normal\".")

  @task(1)
  def openTranslation(self):
    headerSet = {"Content-Type": "application/json"}
    with self.client.get("/translation", headers=headerSet, catch_response=True) as response:
      jdata = json.loads(response.content)
      if response.status_code != 200 and jdata['msg']['description'] != "Success":
        response.failure("Wrong Response, it should message desc is \"Success\".")

  @task(1)
  def openNotiSub(self):
    headerSet = {"Content-Type": "application/json"}
    dataParse = {
      "uuid": self.FAKE_UUID,
      "token": self.FAKE_TOKEN,
      "user_id": self.FAKE_USER_ID
    }
    with self.client.post("/notification/subscribe", headers=headerSet, json=dataParse, catch_response=True) as response:
      jdata = json.loads(response.content)
      if response.status_code != 200 and jdata['msg']['description'] != "Success":
        response.failure("Wrong Response, it should message desc is \"Success\".")

  @task(2)
  def homepage(self):
    with self.client.get("/homepage", catch_response=True) as response:
      jdata = json.loads(response.content)
      banner_load = len(jdata['data']['banner'])
      news_load = len(jdata['data']['news'])
      feature_load = len(jdata['data']['feature'])
      isContentLoad = True if (banner_load + news_load + feature_load)/3 >= 0 else False
      if response.status_code != 200 and jdata['msg']['description'] != "Success" and not isContentLoad:
        response.failure("Wrong Response, it should message desc is \"Success\" and Content least 1 for all.")

  @task(1)
  def mobileNews(self):
    with self.client.get("/mobile/news?page=&per_page=", catch_response=True) as response:
      jdata = json.loads(response.content)
      isContentLoad = True if jdata['data']['pagination']['total'] >= 0 else False
      if response.status_code != 200 and jdata['msg']['description'] != "Success" and not isContentLoad:
        response.failure("Wrong Response, it should message desc is \"Success\" and Content least 1 for all.")

class LoginwithAccount(TaskSequence):
  """
  Second scenarios to simulate user action on login account from application.
This transaction inherit task from [OpenHomePage] first, then send POST request 
to create user's session to get any action.
  """
  USER_TOKEN = None

  def encodeToken(self,strtoken):
    msgByte = strtoken.encode('utf8')
    base64Byte = base64.b64encode(msgByte)
    return base64Byte.decode('utf8')
  
  def decodeToken(self,encodetoken):
    base64Msg = encodetoken.encode('utf8')
    msgByte = base64.b64decode(base64Msg)
    return msgByte.decode('utf8')

  def getToken(self):
    return self.decodeToken(self.USER_TOKEN)
  
  def setToken(self,token):
    self.USER_TOKEN = self.encodeToken(token)

  def sendCredentials(self):
    headerSet = {"Content-Type": "application/json"}
    postBodies = {
      "username": "0912567652",
      "password": "Pass1234",
      "type": "normal",
      "apple": "rottenApple"
    }
    with self.client.post("/login", headers=headerSet, json=postBodies, catch_response=True) as response:
      jdata = json.loads(response.content)
      if response.status_code != 200 and jdata['msg']['description'] != "Success":
        response.failure("Wrong Response, it should message desc is \"Success\".")
      else:
        self.setToken(jdata["data"]["token"])
  
  def refreshToken(self):
    headerSet = {"Authorization": "Bearer "+self.getToken() }
    with self.client.get("/refresh_token", headers=headerSet, catch_response=True) as response:
      jdata = json.loads(response.content)
      isContentLoad = True if 'expire' in jdata['data'] else False
      if response.status_code != 200 and jdata['msg']['description'] != "Success" and not isContentLoad:
        response.failure("Wrong Response, it should message desc is \"Success\" and Content least 1 for all.")

  def checkPinMobile(self):
    headerSet = {"Authorization": "Bearer "+self.getToken() }
    payload = {
      "pin": "123451",
      "pin_confirm": "123451"
    }
    with self.client.get("/mobile/check/pin", headers=headerSet, data=payload, catch_response=True) as response:
      jdata = json.loads(response.content)
      isContentLoad = True if jdata['data']['has_pin'] == 'true' else False
      if response.status_code != 200 and jdata['msg']['description'] != "Success" and not isContentLoad:
        response.failure("Wrong Response, it should message desc is \"Success\" and Content least 1 for all.")

  def getProfileMe(self):
    headerSet = {"Authorization": "Bearer "+self.getToken() }
    with self.client.get("/me", headers=headerSet, catch_response=True) as response:
      jdata = json.loads(response.content)
      isContentLoad = True if 'id' in jdata['data'] else False
      if response.status_code != 200 and jdata['msg']['description'] != "Success" and not isContentLoad:
        response.failure("Wrong Response, it should message desc is \"Success\" and Content least 1 for all.")
  

class UserFirstAction(LoginwithAccount,OpenHomePage):
  
  @seq_task(1)
  def openPage(self):
    print("Start with: " + self.getToken())
    self.openApp()
    self.openTranslation()
    self.openNotiSub()
    self.mobileNews()
  
  @seq_task(2)
  def Login(self):
    self.sendCredentials()
    print("Login: " + self.getToken())
  
  # @seq_task(3)
  # def refreshToken(self):
  #   self.refreshToken()
  
  @seq_task(4)
  def chkPinandgetMe(self):
    self.checkPinMobile()
    self.getProfileMe()
    print("Chk Profile: " + self.getToken())
  
  @seq_task(5)
  def afterLogin(self):
    self.homepage()
    self.refreshToken()
    self.getProfileMe()
    self.mobileNews()
    print("Post Login: " + self.getToken())

class UserGetNearby(LoginwithAccount,OpenHomePage):

  def getNearBy(self):
    parameters = {
      "lat": 13.6925968,
      "ing": 100.60917,
      "page": 1,
      "per_page": 200
    }
    with self.client.get("/locations", params=parameters, catch_response=True) as response:
      jdata = json.loads(response.content)
      isContentLoad = True if jdata['data']['pagination']['total'] >= 0 else False
      if response.status_code != 200 and jdata['msg']['description'] != "Success" and not isContentLoad:
        response.failure("Wrong Response, it should message desc is \"Success\" and Content least 1 for all.")

  @seq_task(1)
  def openPage(self):
    self.openApp()
    self.openTranslation()
  
  @seq_task(2)
  def Login(self):
    self.sendCredentials()
  
  @seq_task(3)
  def refreshToken(self):
    self.refreshToken()
  
  @seq_task(4)
  def chkPinandgetMe(self):
    self.checkPinMobile()
    self.getProfileMe()
  
  @seq_task(5)
  def afterLogin(self):
    self.homepage()
    self.refreshToken()
    self.getProfileMe()
    self.mobileNews()
    self.getNearBy()

class Start(HttpLocust):
  task_set = UserFirstAction
  wait_time = between(1,5)