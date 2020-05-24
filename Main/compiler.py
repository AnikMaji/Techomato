import requests

RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
COMPILE_URL = u'https://api.hackerearth.com/v3/code/compile/'
CLIENT_SECRET = '5df0bbbede9ccf1a5dede39e160e5078a3e43ad6'


class MyCompiler:
    def compile(self, source, lan):
        data = {
            'client_secret': CLIENT_SECRET,
            'async': 0,
            'source': source,
            'lang': lan,
            'time_limit': 5,
            'memory_limit': 262144,
        }

        r = requests.post(COMPILE_URL, data=data)
        rJson=r.json()
        print(r.json())
        if('compile_status' in rJson):
            return rJson['compile_status']
        else:
            return "You have not written anything in the code section."

    def runCode(self, source, lan, input=""):
        data = {
            'client_secret': CLIENT_SECRET,
            'input':input,
            'async': 0,
            'source': source,
            'lang': lan,
            'time_limit': 5,
            'memory_limit': 262144,
        }

        r = requests.post(RUN_URL, data=data)
        rJson = r.json()
        error=False
        print(r.json())
        if ('compile_status' in rJson):
            if(rJson['compile_status']=="OK"):
                if('run_status' in rJson):
                    if('stderr' in rJson['run_status']):
                        if(rJson['run_status']['stderr']==""):
                            return [rJson['run_status']['output'],error]
                        else:
                            error = True
                            return [rJson['run_status']['stderr'],error]
                    else:
                        error = True
                        return [rJson['compile_status'],error]
                else:
                    error = True
                    return [rJson['compile_status'],error]
            else:
                error = True
                return [rJson['compile_status'],error]
        else:
            return ["You have not written anything in the code section.",error]
