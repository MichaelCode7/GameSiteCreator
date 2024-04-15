import json


class GeneralFuncs: 
    def get_form_json(path, key=None):
        with open(path, 'r') as jsonf:
            jsond = json.loads(jsonf.read())
            if key != "" or key != None:
                return jsond[key]
            return jsond
