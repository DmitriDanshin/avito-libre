from app import App

app = App()

if __name__ == '__main__':
    import json

    with open('settings.json') as config_file:
        data = json.load(config_file)

    width = data['city']
    height = data['search']
    print(width)
    print(height)

    app.run()
