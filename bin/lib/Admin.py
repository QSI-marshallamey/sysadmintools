class Admin:
       ##### FUNCTIONS #####
    def __init__(self, usersFilePath, auth):
        #self.getUserList(usersFilePath)
        self.auth = auth


    def getUserList(self, usersFilePath): 
        if os.path.isfile(usersFilePath): self.useUserList(usersFilePath)
        else:
            path = input(f'\nNo user file found.  Enter path to user file or press ENTER to input users manually: ') 
            if path: self.useUserList(path)
            else: self.useManualInput()


    def useUserList(self, usersFilePath):
        ''' 
        Retrieves user data from excel file
        
        Args
            usersFilePath: File path to user data   
        Returns 
            Formatted list of users as dictionaries
        '''

        # Open excel file
        # Split col A into first and last name
        # col T (Personal Email)
        # col I (Hiring Manager)
        # col L (Department)
        # col M (Title)
        # col G ( ) Temp or FT-Admin *i
        print('getting users...')
        excelFile = openpyxl.load_workbook(usersFilePath)
        sheet = excelFile['Pending Start']
        print('excel sheet opened...')
        # Get today's date
        today = date.today()
        startDate = date.today()
        
        for cell in sheet['B']:
            
            row = cell.row          
            # If column B cell is not empty, get start date
            if cell.value:               
                try:
                    startDate = str(cell.value)
                    year = int(startDate[0:4])
                    month = int(startDate[5:7])
                    day = int(startDate[8:10])
                    startDate = date(year, month, day)
                except:
                    # TODO Add to log file
                    self.log.write('getNewHires ==> INCORRECT DATE FORMAT! Row ' + str(cell.row) + '\n')
                    startDate = date.today()
            
            # Add all newHires starting in San Francisco office to user list
            startLocation = sheet.cell(row=row, column=11).value
            if startDate > today and (startLocation == 'San Francisco' or startLocation == 'Obscura'):
                name = sheet.cell(row=row, column=1).value.split(' ')
                personalEmail = sheet.cell(row=row, column=20).value
                department = sheet.cell(row=row, column=12).value
                title = sheet.cell(row=row, column=13).value
                manager = sheet.cell(row=row, column=9).value
                status = sheet.cell(row=row, column=7).value
                self.users.append({
                    'firstName': name[0],
                    'lastName': name[1],
                    'personalEmail': personalEmail,
                    'workEmail': f'{name[0].lower()}.{name[1].lower()}@obscuradigital.com',
                    'department': department,
                    'title': title,
                    'manager': manager,
                    'status': status.lower(),
                    'startDate': startDate,
                })
        self.log.write('\n')
        self.log.write('getNewHires ==> Found the following users in Onboarding Tracker:\n\n')
        for user in self.users: self.log.write(str(user) + '\n\n')   


    def useManualInput(self):
        ''' 
        Retrieves user data manually from administrator
        '''
        done = False
        while not done:

            ## Enter user info
            user = {}
            print('\nEnter new user information')
            user['firstName'] = input('First name: ')
            user['lastName'] = input('Last name: ')
            user['personalEmail'] = input('Personal email: ')
            user['workEmail'] = input('Work email: ')
            user['department'] = input('Department: ')
            user['title'] = input('Job title: ')
            user['manager'] = input('Manager: ')
            user['status'] = input('Status (ft or temp): ')
            user['startDate'] = input('Start date (mm/dd/yyyy):')
            
            ## Validate entry
            print('\nYou have entered the following new user.')
            print(user)
            confirm = input('Is this correct? (Y or N): ')
            if confirm.lower() == 'n': continue

            ## Add new user to users list
            self.users.append(user)
            confirm = input('Would you like to add another user? (Y or N): ')
            if confirm.lower() == 'n': 
                done = True
