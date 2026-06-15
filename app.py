from fastapi import FastAPI,Path,HTTPException,Query
import json
# import pandas as pd
# import openpyxl

app = FastAPI()

def load_data():
    with open('students.json') as f:
        data = json.load(f)
        return data


# def load_data2():
#     df = pd.read_excel("employee.xlsx")
#     return df
    
    
@app.get("/")
def home():
    return {"msg":'Home'}

@app.get("/students")
def show_all_students():
    data = load_data()
    return data

@app.get("/students/{roll}")
def get_student(roll:str =Path(...,description='Student Roll Number',example="1234")):
    data = load_data()
    if roll in data:
        return data[roll]
    raise HTTPException(status_code=404, detail='Student Not Found')
        

@app.get('/sort')
def sort_students(sort_by: str = Query(...,   description='Sort on the basis of Python, Pandas or Numpy'), 
                  order: str =   Query('asc', description='sort in asc or desc order')
                  ):

    valid_fields = ['Python', 'Pandas', 'Numpy']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data
@app.get("/dataframe")
def show_employees():
    employees = load_data2()
    return employees