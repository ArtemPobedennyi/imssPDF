from io import BytesIO
import requests
from base64 import b64decode

import config

class IMSS:
    def __init__(self, curp, email):
        self.ssn = requests.Session()
        self.ssn.headers.update(config.header)

        self.deviceId = '00000100-89ABCDEF-01234567-89ABCDEF'
        self.email = email
        self.curp = curp

        self.token = None
        self.NSS = None
        self.timeout = 60

        self.bytesData = None

    def actionLoginWhitelist(self):
        print('#ActionLoginWhitelist => start')

        endpoint = 'https://outsystems.imss.gob.mx/IMSSDigital/screenservices/IMSSUsers_MCW/ActionLoginListablanca'
        params = {
            "inputParameters": {
                "LoginUsuario": {
                    "CURP": self.curp,
                    "Email": self.email,
                    "IdDispositivo": ""
                }
            },
            "versionInfo": {
                "apiVersion": "Ve6SIW7IJ_qDqxVGC83eZQ",
                "moduleVersion": "yYfO0ZJMnZNIFtHvmHNvdQ"
            },
            "viewName": "IMSSDigital.LoginIMSS"
        }

        try:
            response = self.ssn.post(endpoint, json=params, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("\tHttp Error:", errh)
            return False
        except requests.exceptions.ConnectionError as errc:
            print ("\tError Connecting:", errc)
            return False
        except requests.exceptions.Timeout as errt:
            print ("\tTimeout Error:", errt)
            return False
        except requests.exceptions.RequestException as err:
            print ("\tOOps: Something Else", err)
            return False

        
        self.token = response.json()['data']['Tokens']['Token']
        self.NSS = response.json()['data']['Persona']['Nss']

        # print('\tToken => ' + self.token)
        print('\tsuccess')

        return True

    def actionSendOTP(self):
        print('#ActionSendOTP => start')

        endpoint = 'https://outsystems.imss.gob.mx/IMSSDigital/screenservices/IMSSUsers_MCW/LoginFlow/Login/ActionEnviarOTP'
        params = {
            "inputParameters": {
                "LoginUsuario": {
                    "CURP": self.curp,
                    "Email": self.email,
                    "IdDispositivo": self.deviceId
                }
            },
            "versionInfo": {
                "apiVersion": "2OT7DAEETfZciW+BVL1QFA",
                "moduleVersion": "yYfO0ZJMnZNIFtHvmHNvdQ"
            },
            "viewName": "IMSSDigital.LoginIMSS"
        }

        try:
            response = self.ssn.post(endpoint, json=params, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("\tHttp Error:", errh)
            return False
        except requests.exceptions.ConnectionError as errc:
            print ("\tError Connecting:", errc)
            return False
        except requests.exceptions.Timeout as errt:
            print ("\tTimeout Error:", errt)
            return False
        except requests.exceptions.RequestException as err:
            print ("\tOOps: Something Else", err)
            return False

        print('\tsuccess')
        result = response.json()['data']['Result']['Success']

        # print('\tSend OTP => {}'.format(result))

        return True

    def serviceAPIValidateOTP(self, otp_code):
        print('#serviceAPIValidateOTP => start')
        endpoint = 'https://outsystems.imss.gob.mx/IMSSDigital/screenservices/IMSSUsers_MCW/LoginFlow/OTPForm/ServiceAPIvalidarOTP'
        params = {
            "inputParameters": {
                "LoginUsuario": {
                    "CURP": self.curp,
                    "Email": self.email,
                    "IdDispositivo": self.deviceId
                },
                "OTP": otp_code
            },
            "versionInfo": {
                "apiVersion": "wJSA19vsUwA9lrFg5MzfBw",
                "moduleVersion": "yYfO0ZJMnZNIFtHvmHNvdQ"
            },
            "viewName": "IMSSDigital.LoginIMSS"
        }

        try:
            response = self.ssn.post(endpoint, json=params, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("\tHttp Error:", errh)
            return False
        except requests.exceptions.ConnectionError as errc:
            print ("\tError Connecting:", errc)
            return False
        except requests.exceptions.Timeout as errt:
            print ("\tTimeout Error:", errt)
            return False
        except requests.exceptions.RequestException as err:
            print ("\tOOps: Something Else", err)
            return False

        print('\tsuccess')
        result = response.json()['data']['ResultadoServicio']['Exito']

        # print('\tValidation OTP => {}'.format(result))

        return True

    def DataActionGeneratePDF(self):
        print('#DataActionGeneratePDF => start')

        endpoint = 'https://outsystems.imss.gob.mx/IMSSDigital/screenservices/Semanas_Cotizadas_MCW/SemanasCotizadas_Private/Paso4/DataActionGeneratePDF'
        params = {
            "screenData": {
                "variables": {
                    "CURP": self.curp,
                    "Detalles": True,
                    "Loaded": False,
                    "NSS": self.NSS,
                    "TokenExpirado": False,
                    "_cURPInDataFetchStatus": 1,
                    "_detallesInDataFetchStatus": 1,
                    "_nSSInDataFetchStatus": 1,
                    "_tokenExpiradoInDataFetchStatus": 1
                }
            },
            "versionInfo": {
                "apiVersion": "I62fOf7E869V364_jitGAA",
                "moduleVersion": "yYfO0ZJMnZNIFtHvmHNvdQ"
            },
            "viewName": "IMSSDigital.SemanasCotizadas"
        }

        try:
            response = self.ssn.post(endpoint, json=params, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("\tHttp Error:", errh)
            return False
        except requests.exceptions.ConnectionError as errc:
            print ("\tError Connecting:", errc)
            return False
        except requests.exceptions.Timeout as errt:
            print ("\tTimeout Error:", errt)
            return False
        except requests.exceptions.RequestException as err:
            print ("\tOOps: Something Else", err)
            return False

        result = response.json()
        
        popupEnabled = result['data']['Popup']['Enabled']
        exceptionFlag = result['data']['Exception']

        if popupEnabled or exceptionFlag:            
            print('\terror => {}'.format(result['data']['Popup']['Message']))
            return False

        
        pdfBase64 = result['data']['PDFBase64']
        if not pdfBase64 or len(pdfBase64) < 4:
            print('\terror')
            return False

        try:
            bytes = b64decode(pdfBase64, validate=True)
            if bytes[0:4] != b'%PDF':
                raise ValueError('Missing the PDF file signature')
            self.bytesData = BytesIO(bytes)
            # with open('file.pdf', 'wb') as f:
            #     f.write(self.bytesData.getbuffer())

        except Exception as ex:
            print('\terror')
            return False

        print('\tsuccess')
        return True