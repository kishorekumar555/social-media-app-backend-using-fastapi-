from fastapi import FastAPI,Response,HTTPException,status
from typing import Optional
from pydantic import BaseModel
from fastapi.params import Body
from random import randrange
app=FastAPI()
my_student=[{'id':1,'Name':"Kishore Kumar",'Class':"XII-A",'Math_marks':95,'Science_marks':92,'Social_marks':98,'English_marks':86,'Tamil_marks':83},
            {'id':2,'Name':"Karthick",'Class':"XII-A","Math_marks":89,"Science_marks":92,"Social_marks":97,"English_marks":88,"Tamil_marks":82}]
class Post(BaseModel):
    Name:str
    Class:str
    Math_Marks:float
    Science_Marks:float
    Social_Marks:float
    English_Marks:float
    Tamil_Marks:float
    Age:Optional[int]=16
#get all students
@app.get("/students")
def getstudents():
    return {'Students_data':my_student}
# post student or create a new record of students
@app.post("/students",status_code=status.HTTP_201_CREATED)
def poststudents(post:Post):
    post_dict=post.dict()
    post_dict['id']=randrange(1,20000000)
    my_student.append(post_dict)
    print(my_student)
    return{'message':"The student record was created successfully"}