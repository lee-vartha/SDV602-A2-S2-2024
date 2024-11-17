from jsn_drop_service import jsnDrop
from time import gmtime
from datetime import datetime

class UserManager(object):
    current_user = None
    this_user_manager = None
    current_pass = None
    current_screen = None
    current_status = None
    chat_list = []
    chat_thread = None
    stop_thread = False
    thread_lock = False
    jsn_tok = "d99cf319-8e7f-4b9c-9135-a6caae3fb7cd"
    latest_time = None

    def now_time_stamp(self):
        time_now = datetime.now()
        time_now.timestamp()
        return time_now.timestamp()
    

    def __init__(self) -> None:
        super().__init__()

        self.jsnDrop = jsnDrop(UserManager.jsn_tok,"https://newsimland.com/~todd/JSON")
        result = self.jsnDrop.create("tblUser",{"PersonID PK":"A_LOOONG_NAME"+('X'*50),
                                                "Password":"A_LOOONG_PASSWORD"+('X'*50),
                                                "Status":"STATUS_STRING"})
        
        result = self.jsnDrop.create("tblChat", {"PersonID PK":"A_LOOONG_NAME"+('X'*50),
                                                 "DESNumber":"A_LOOONG_DES_ID"+('X'*50),
                                                 "Chat":"A_LOONG____CHAT_ENTRY"+('X'*255),
                                                 "Time": self.now_time_stamp()})
        
        UserManager.this_user_manager = self
        self.test_api()

    def register(self, user_id, password):
        api_result = self.jsnDrop.select("tblUser",f"PersonID = '{user_id}")
        if( "DATA_ERROR" in self.jsnDrop.jsnStatus):
            result = self.jsnDrop.store("tblUser",[{'PersonID':user_id,'Password':password,'Status':'Registered'}])
            UserManager.current_user = user_id
            UserManager.current_status = 'Logged Out'
            result = "Registration Success"
        else:
            result = "this user already exists"

            return result


    def login(self, user_id, password):
        result = None
        api_result = self.jsnDrop.select("tblUser",f"PersonID = '{user_id}' AND Password = '{password}'") 
        if ("DATA_ERROR" in self.jsnDrop.jsnStatus):
            result = "Nope - Login Failed"
            UserManager.current_status = "Logged Out"
            UserManager.current_user = None
        else:
            UserManager.current_status = "Logged In"
            UserManager.current_user = user_id
            UserManager.current_pass = password
            api_result = self.jsnDrop.store("tblUser",[{"PersonID":user_id,"Password":password,"Status":"Logged In"}])
            result = "Login Success"
        return result

    def set_current_DES(self, DESScreen):
        result = None
        if UserManager.current_status == "Logged In":
            UserManager.current_screen = DESScreen
            result = "Set Screen"
        else:
            result = "You must login to set the current screen"
        return result


    def get_chat(self):
        result = None

        if UserManager.current_status == "Logged In":
            des_screen = UserManager.current_screen
            if not (des_screen is None):
                api_result = self.jsnDrop.select("tblChat",f"DESNumber = '{des_screen}'")
                if not ('DATA_ERROR' in api_result):
                    UserManager.chat_list = self.jsnDrop.jsnResult
                    result = UserManager.chat_list
        return result
    

    def chat(self,message):
        result = None
        if UserManager.current_status == "Logged Out":
            result = "You need to be logged in to chat"
        elif UserManager.current_screen == None:
            result = "You must set a current screen before sending a chat"
        else:
            user_id = UserManager.current_user
            des_screen = UserManager.current_screen
            api_result = self.jsnDrop.store("tblChat",[{'PersonID':user_id,
                                                        'DESNumber':f'{des_screen}',
                                                        'Chat':message,
                                                        'Time': self.now_time_stamp()}])
            if "ERROR" in api_result:
                result = self.jsnDrop.jsnStatus
            else:
                result = "Message has been sent"
            return result


    def logout(self):
        result = "Must be 'Logged In' to be able to 'Logout'"
        if UserManager.current_status == "Logged In":
            api_result = self.jsnDrop.store("tblUser",[{"PersonID": UserManager.current_user,
                                                        "Password": UserManager.current_pass,
                                                        "Status":"Logged Out"}])
            if not("ERROR" in api_result):
                UserManager.current_status = "Logged Out"
                result = "Logged Out"
            else:
                result = self.jsnDrop.jsnStatus
        return result


   
    


    def test_api(self):
        # Should this be in jsn_drop_service ?
        result = self.jsnDrop.create("tblTestUser",{"PersonID PK":"Emily","Score":20})
        print(f"Create Result from UserManager {result}")

        self.jsnDrop.store("tblTestUser",[{"PersonID":"Emily","Score":20},{"PersonID":"Lee","Score":92}])
        print(f"Store Result from UserManager {result}")

        result = self.jsnDrop.all("tblTestUser")
        print(f"All Result from UserManager {result}")

        result = self.jsnDrop.select("tblTestUser","Score > 200") # select from tblUser where Score > 200
        print(f"Select Result from UserManager {result}")

        result = self.jsnDrop.delete("tblTestUser","Score > 200") # delete from tblUser where Score > 200
        print(f"Delete Result from UserManager {result}")

        result = self.jsnDrop.drop("tblTestUser")
        print(f"Drop Result from UserManager {result}")



def testUserManager():
    # Just a Test

    # Start with no user table and no chat table
    a_jsnDrop = jsnDrop(UserManager.jsn_tok,"https://newsimland.com/~todd/JSON")
    a_jsnDrop.drop('tblUser')
    a_jsnDrop.drop('tblChat')
    # Now start a User manager with a clean slate

    # Get a User Maanager
    a_user_manager = UserManager()

    #register
    register_status = a_user_manager.register("Emily", "29904") 
    print(f"REGISTER STATUS: {register_status}")

    #login 
    login_status = a_user_manager.login("Emily","29904")
    print(f"LOGIN STATUS: {login_status}")

    # when logged in set current screen
    set_screen_status = a_user_manager.set_current_DES("DES1")  
    print(f"SET CURRENT SCREEN: {set_screen_status}") 

    # when logged in send a chat   
    chat_status = a_user_manager.chat("Hi There 1")
    print(f"SEND CHAT STATUS: {chat_status}")

    # when logged in get chat
    chat_status = a_user_manager.get_chat()
    print(f"GET CHAT STATUS: {chat_status}")

    # log out
    logout_status = a_user_manager.logout()
    print(f"LOGOUT STATUS: {logout_status}")

    # attempt bad login (logs out)
    login_status = a_user_manager.login("Emily","22")
    print(f"LOGIN STATUS: {login_status}")

    # attempt send chat when not logged in, after bad login 
    chat_status = a_user_manager.chat("Hi There 2")
    print(f"SEND CHAT STATUS after bad login: {chat_status}")

    # attempt get chat when not logged in, after bad login
    chat_status = a_user_manager.get_chat()
    print(f"GET CHAT STATUS after bad login: {chat_status}")
    

