import requests
import json
import mpu.io

class YellowLabs:

    def __init__(self, tarUrl):
        self.tarUrl = tarUrl
        requestJson = {'url': self.tarUrl, 'waitForResponse': 'false',
                       'screenshot': 'true', 'device': "desktop"}
        self.requestJs = requestJson

    def scan(self):
        resRun = requests.post(url='https://yellowlab.tools/api/runs', json=self.requestJs)
        runId = json.loads(resRun.text)

        while True:
            r = requests.get(
                url='https://yellowlab.tools/api/runs/{}'.format(runId['runId']))
            statusJson = json.loads(r.text)
            status = statusJson['status']['statusCode']
            if str(status) == "complete":
                print('scan complete')
                return runId

    def getResult(self, scanId):
        r = requests.get(
            url='https://yellowlab.tools/api/results/{}?exclude=toolsResults'.format(scanId['runId']))
        data=json.loads(r.text)
        print(data)

        mpu.io.write('result.json', data)

    
    def Run(self):
        ScanId = self.scan()
        self.getResult(ScanId)


def main():
    # enter your url here
    Url = "http://cert.uma.ac.ir/" 
    obj = YellowLabs(Url)
    obj.Run()


if __name__ == "__main__":
    main()
