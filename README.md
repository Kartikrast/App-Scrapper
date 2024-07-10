The project has been created with the help of:
-	Appium Server
-	Appium Inspector
-	Selenium
-	Python
-	Pandas
-	Numpy
-	ADB
-	JRE/NPM
-	REGEX

I have implemented OOPs concept to create the backend of this program, the class Instagram_data contains several methods. The Appium session will first connect with my connected android device(virtual/real), for which we have to set the desired capabilities, the user needs to input only these details to use the program: -
-	ADB device_name = Device name from the command (adb devices)
-	Android Version
-	Target Number = The number of leads they want to scrape
-	Search tag = The hashtag they want to search
The program will itself search the given search tag, then it will start opening the accounts one by one from the posts section, and will start scrapping and storing the data from the account profiles, finally it will create a pandas data frame and will store the output(leads) in an Excel file.
