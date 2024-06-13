# Django Project Name
User Discussion Management System
#first you need to create an environment
    python3 -m venv myenv
    myenv\Scripts\activate 
# install requirements.txt
    pip install -r requirements.txt

## Admin Credentials
email = admin@gmail.com
password = Abcd@1234
## Installation
Visit http://127.0.0.1:8000/

## POST_MAN Payload Collections
link - https://api.postman.com/collections/34549230-48838ec3-a3b4-4bde-a11c-6463df587195?access_key=PMAT-01J09AVQ29Q3CE7XZS7A7BHKMA

## Contributing API ENDPOINT
● POST: http:/127.0.0.1:8000/user/register/ : Create a new user.
● POST: http:/127.0.0.1:8000/user/login: login User.
● GET:  http:/127.0.0.1:8000/user/user_list: list of all users.
● PUT or GET: http:/127.0.0.1:8000/user/b2c3d5f2-d7ec-477b-afd2-3a7b1af2159a/: Update and Get specific user's details.
● DELETE user/b2c3d5f2-d7ec-477b-afd2-3a7b1af2159a/: Delete a specific user.

## User Discussion
● POST: http:/127.0.0.1:8000/discussion/add/: Create a discussion.
● GET : http:/127.0.0.1:8000/discussion/: List all discussion
● GET or PUT: http:/127.0.0.1:8000/discussion/e7e594f4-ab9c-42ca-bd71-c7be3aa8b982/  : Retrieve or Update Specific Discussion.
● GET: http:/127.0.0.1:8000/discussion/list_by_hashtag/?hashtag=%23interview  : Retrieve Discussion by the hashtag.
● GET: http:/127.0.0.1:8000/discussion/list_by_text/?text=discussion   : Retrieve Discussion by the hashtag.
● DELETE: http:/127.0.0.1:8000/discussion/f3aeb206-4599-4eee-8ddc-6facfb7d3300/   : Delete Specific Discussion by the UUID.
