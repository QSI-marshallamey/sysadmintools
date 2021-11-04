# main.py
from appJar import gui
import Communication

# Application for retrieving email
class MyEmail():

    # Build the GUI
    def Prepare(self, app):
        # Form GUI
        app.setTitle('Login')
        app.setFont(16)
        app.setBg('teal')
        app.setFg('white')
        app.setSize(400, 150)
        app.setGuiPadding(50, 10)
        app.setStopFunction(self.BeforeExit)
        

        # Add labels & entries in correct row & column
        app.addLabel('userLab', 'Username:', 0, 0)
        app.addEntry('username', 0, 1)
        app.addLabel('passLab', 'Password:', 1, 0)
        app.addSecretEntry('password', 1, 1)
        app.addButtons(['Submit', 'Cancel'], self.Submit, colspan=2)
        app.setFocus('username')

        return app

    # Build and start the application
    def Start(self):
        # Create a UI
        app = gui()
        # Run the prebuild method to add items to the UI
        app = self.Prepare(app)
        # Make the app class-accessible
        self.app = app
        # Start appJar
        app.go()

    # Callback execute before quitting your app
    def BeforeExit(self):
        return self.app.yesNoBox('Confirm Exit', 'Are you sure you want to exit the application?')

    # Define method that is executed when the user clicks on the submit buttons of the form
    def Submit(self, btnName):
        if btnName == 'Submit':
        
            username = self.app.getEntry('username')
            password = self.app.getEntry('password')
            m = Communication.Communication()
            theMail = m.login(username, password)
            print(theMail)
            if username and password == 'Marshall':
                self.app.removeAllWidgets()
                self.app.addMessage('messageTitle', theMail)
                self.app.setSize(1000, 500)
                self.app.setMessageWidth('messageTitle', 800)
            else:
                self.app.errorBox('Error', 'Your credentials are invalid!')
        if btnName == 'Cancel':
            self.app.stop()
# Run the application
# 'python myGUI.py'
if __name__ == '__main__':
    # Create an instance of your application
    App = MyEmail()
    # Start the app
    App.Start()