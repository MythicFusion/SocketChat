
pages = {
    "homepage" : {
        "size" : [24, 8],
        "position" : [38, 16],
        "title" : "Welcome to the Roads",
        "elements" : [{
            "type" : "Menu",
            "size" : [10, 3],
            "position" : [7, 3],
            "options" : ["Sign In", "Register", "Exit"],
            "commands" : ["GET Sign In", "GET Register", "EXIT"]
        }]
    },
    "Sign In" : {
        "size" : [24, 12],
        "position" : [38, 14],
        "title" : "Sign In Page",
        "elements" : [{
            "type" : "Input",
            "size" : [22, 3],
            "position" : [1,2],
            "label" : "Username"
        },{
            "type" : "Input",
            "size" : [22, 3],
            "position" : [1,5],
            "label" : "Password",
            "char" : "*"
        },{
            "type" : "Button",
            "size" : [9, 3],
            "position" : [7,8],
            "label" : "Sign In",
            "command" : "POST authenticate {self.elements[0].input_string} {self.elements[1].input_string}"
        }]
    },
    "Register" : {
        "size" : [24, 12],
        "position" : [38, 14],
        "title" : "Registration Page",
        "elements" : [{
            "type" : "Input",
            "size" : [22, 3],
            "position" : [1,2],
            "label" : "Username"
        },{
            "type" : "Input",
            "size" : [22, 3],
            "position" : [1,5],
            "label" : "Password",
            "char" : "*"
        },{
            "type" : "Button",
            "size" : [10, 3],
            "position" : [7,8],
            "label" : "Register",
            "command" : "POST register {self.elements[0].input_string} {self.elements[1].input_string}"
        }]
    },
    "Lobby" : {
        "size" : [98, 36],
        "position" : [1, 1],
        "title" : "User's Lobby",
        "elements" : []
    }
}
