from website import create_app,create_api
#!!!!!!!!!!! Before Deploying change to .website !!!!!!!!!!! 
app = create_app()
api = create_api(app)

if __name__ == '__main__':
    app.run(debug=1)