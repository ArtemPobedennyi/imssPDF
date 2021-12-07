from imss import IMSS
from otp import OTP
import config

def main_proc(curp, email_address, email_password):
    print('Curp \t=> {}'.format(curp))
    print('Email \t=> {}\n'.format(email_address))

    imss = IMSS(curp, email_address)
    
    if not imss.actionLoginWhitelist():
        return False
    if not imss.actionSendOTP():
        return False

    otp = OTP(email_address, email_password)
    if not otp.createDriver():
        return False

    if not otp.loginServer():
        otp.closeDriver()
        return False

    if not otp.fetchOTPCode():
        otp.closeDriver()
        return False
    
    otp.closeDriver()

    if not imss.serviceAPIValidateOTP(otp.otp_code):
        return False

    if not imss.DataActionGeneratePDF():
        return False

    print('\t{}'.format(imss.bytesData.getvalue()))
    return imss.bytesData

if __name__ == "__main__":
    main_proc(config.curp, config.email_address, config.email_password)