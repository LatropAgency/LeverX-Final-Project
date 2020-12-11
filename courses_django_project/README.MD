#  Installation
***
Enter `docker-compose up --build` in CLI
# How to run app
***
Enter `docker-compose run web` in CLI
# Description
***
This django project is my final task  the LeverX courses. It's a simple REST API application. There are 2 types of users. First one is students and second one is teachers.
### Teacher may:
* CRUD his courses
* adding/deleting a student to their course
* adding a new teacher to their course
* CRUD lectures of their courses
* add homework to each lecture
* view completed homeworks
* for each completed homework, set/change marks
* add comments to each mark
### Student may:
* view available courses
* view available lectures within the selected available course
* view the available lecture's homework
* sending solution for review
* view your solutions
* view marks for your solutions
* view/add comments to the mark.
# Testing
***
Enter `docker-compose run web python manage.py test` in CLI