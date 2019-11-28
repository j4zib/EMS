
# Entry Management Software
>Innovaccer Summergeeks 2020 SDE-Intern Assignment.

## Tech Stack
- HTML
- CSS
- Javascript
- Python
- SQL
- Flask
- MySQL

## General Approach
- If the Host is logged-in, then the home page will show the log of all the active visitors and the past visitors.
- If the Host is not Logged-in, then the home page will show the form to check-in the visitor.
- Visitor fills the form and choose the host that he/she is visiting.
- Once the form is filled, the data will be saved on database  along with the check-in time and then an e-mail and an SMS will be sent to the host containing visitor's details.
- When meeting is over visitor can check-out using the check-out button in the navigation bar. He has to enter the email address to check out. Check out time will be recorded and Details of the meeting will be sent to visitor. 

## Technical Approach
- Host registration form is submitted on hitting `{baseURL}/register` POST API.
- Host login form is submitted on hitting `{baseURL}/login` POST API.
- Check-in details are posted using `{baseURL}/home` POST API and `mail and sms` will be sent through `flask-mail` and `Twilio` services.
- Check-out details are posted using `{baseURL}/checkout` POST API and `mail` will be sent through `flask-mail` service.
- `{baseURL}/home` will redirect to `{baseURL}/history` when a host is logged-in.
- History details are fetched from `{baseURL}/history`.
```
Security and Caution
1. Once a visitor has checked in, he cannot use the feature again unless he checks out.
2. Prevention of duplicate information of existing host.
3. All necessary cases of error are covered, like if someone try to check out again even after checking out earlier he will be asked to check in first, etc.
4. Flash messages are added for errors and success response.
```

***
## Installation
- Clone the repository using `git clone` and then change the directory to root of the project
``` 
    git clone https://github.com/j4zib/EMS.git
    cd EMS
```
- It is recommended to create a virtual environment.
- Install all the dependencies
```
pip install -r requirements.txt
```
- Open `setup.py` and fill all the information:

```bash
DATABASE_HOST =  'localhost'
DATABASE_NAME =  'DATABASE_NAME'
DB_USER =  'USER_NAME'
DB_PASSWORD =  'USER_PASSWORD'

EMAIL_SERVER =  'smtp.gmail.com'
EMAIL_PORT =  465
EMAIL_ID =  'YOUR_EMAIL_ID'
EMAIL_PASS =  'YOUR_EMAIL_PASS'

TWILIO_ACCOUNT_SID =  'YOUR_ACCOUNT_SID'
TWILIO_AUTH_TOKEN =  'YOUR_ACCOUNT_AUTH_TOKEN'
TWILIO_NUMBER =  'YOUR_TWILIO_NUMBER'
```
- To create the necessary tables, execute:
```
pyhon createTable.py
```
- Run the server using:
```
> python main.py
```

***
## Folder Structure 
```
─── EMS
        ├── createTable.py
        ├── dbconnect.py
        ├── main.py
        ├── sendMessage.py
        ├── setup.py
        │    
        ├── templates
        │    ├── checkout.html
        │    ├── history.html
        │    ├── home.html
        │    ├── layout.html
        │    ├── login.html
        │    ├── register.html
        │    
        ├── static
             ├── main.css
             ├── main.js
             ├── home.html
        

```
***
## Screenshots
||
|-|
| Check-in page (This is the home page if no host is not logged-in) |
| ![new](https://drive.google.com/uc?export=view&id=1mrFXEj-V20-gTki9rw4pxS8HvyYRCnKc) |
| Check-out page |
| ![](https://drive.google.com/uc?export=view&id=1s5q_ARr2uAwJ88Eo8SK5EfMyvrBLXets) | 
| Host Registration Page |
| ![](https://drive.google.com/uc?export=view&id=1mAk-vUMXjWuwlO5oRNMY2EU69siEb3FL) | 
| Host Login Page |
| ![](https://drive.google.com/uc?export=view&id=1BYWzKQhA9KBqm-yxitlDwKnw3hWG66T8) | 
| History page (This is the home page if a host is logged-in) |
| ![](https://drive.google.com/uc?export=view&id=1-ByJVUeEGxuH3Y2WcZAVL_wCwrQVrFDn) | 
***

