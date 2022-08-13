from flask_restful import Resource, reqparse
from flask_login import login_required
import yaml


class Yaml(Resource):

    def get(self):
        with open('/Users/zsy/svc.yaml', encoding='utf-8') as Yaml:
            content = yaml.safe_load(Yaml)
            # print(content)
            content['metadata']['name'] = 'Test'
            content['metadata']['namespace'] = 'TestEnv'
            content['spec']['selector']['k8s-app'] = 'k8s'
            content['spec']['ports'][0]['port'] = 8080
            new_yaml = yaml.dump(content)
            print(new_yaml)
        # return {'data': "hello world", 'message': 'test'}
