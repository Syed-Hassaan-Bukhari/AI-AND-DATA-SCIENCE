from fastapi import FastAPI

app = FastAPI()

data = [{'roll':123,'name':'asad','course':'python'},
        {'roll':124,'name':'farman','course':'data science'},
        {'roll':125,'name':'shan','course':'artificial intelligence'}]



@app.get("/")
def home():
    return 'Welcome to my Learniong Portal!'

@app.get('/add')
def add(a:int, b:int):
    return {'a':a,'b':b,'sum':a+b}

@app.get("/showdata")
def show_data():
    return data[1]

