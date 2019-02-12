import json

def go(model_filename):
    with open(model_filename,'r') as model_file:
        model = json.load(model_file)
    print(json.dumps(model,indent=4))

if __name__ == '__main__':
    go('model.json')
