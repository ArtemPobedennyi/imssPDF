import time

from selenium.webdriver import DesiredCapabilities, Chrome, ChromeOptions
from selenium.webdriver.common import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class OTP:
    def __init__(self, email, password):
        self.server = 'http://' + email.split("@")[1]
        self.email = email
        self.password = password
        self.driver = None
        self.otp_code = ''
        self.timeout = 1

        pass

    def createDriver(self):
        print('#OTP_createDriver => start')

        try:
            port = utils.free_port()

            options = ChromeOptions()                
            options.headless = True
            options.add_argument('--no-sandbox') 
            options.add_argument('--disable-setuid-sandbox')
            options.add_argument('--remote-debugging-port={}'.format(port))
            options.add_argument('--disable-dev-shm-using') 
            options.add_argument('--disable-extensions') 
            options.add_argument('--disable-gpu') 
            options.add_argument('start-maximized') 
            options.add_argument('disable-infobars')

            desired_capabilities = DesiredCapabilities().CHROME
            desired_capabilities['pageLoadStrategy'] = 'none'
            desired_capabilities['acceptInsecureCerts'] = True
            
            # create driver
            self.driver = Chrome(
                options=options, desired_capabilities=desired_capabilities)

            print('\tsuccess')
        except Exception as ex:
            print('\terror')
            return False

        return True

    def loginServer(self):
        print('#OTP_loginServer => start')

        self.driver.get(self.server)

        try:
            WebDriverWait(self.driver, self.timeout*60).until(
                EC.presence_of_element_located(
                    (By.ID, 'rcmloginuser'))
            )

            # print('#OTP_loginServer => find out form!')
            self.driver.find_element(By.XPATH, '//input[@id="rcmloginuser"]').clear()
            time.sleep(self.timeout)

            self.driver.find_element(By.XPATH, '//input[@id="rcmloginuser"]').send_keys(self.email)
            time.sleep(self.timeout)

            self.driver.find_element(By.XPATH, '//input[@id="rcmloginpwd"]').clear()
            time.sleep(self.timeout)

            self.driver.find_element(By.XPATH, '//input[@id="rcmloginpwd"]').send_keys(self.password)
            time.sleep(self.timeout)

            self.driver.find_element(By.XPATH, '//button[@id="rcmloginsubmit"]').click()

        except Exception as ex:
            print('\terror' + ex)
            return False

        time.sleep(self.timeout)

        print('\tsuccess')

        return True

    def fetchOTPCode(self):
        print('#OTP_fetchOTPCode => start')  

        try:
            WebDriverWait(self.driver, self.timeout*60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="messagelist-content"]/table/tbody/tr/td/span/a/span[text()="Código de acceso Aplicación IMSS Digital"]'))
            )

            self.driver.find_elements(By.XPATH,
                '//div[@id="messagelist-content"]/table/tbody/tr/td/span/a/span[text()="Código de acceso Aplicación IMSS Digital"]'
            )[0].click()

        except TimeoutException:
            print('\terror => cannot findout OTP email')
            return False  

        time.sleep(self.timeout * 1)
        

        try:
            WebDriverWait(self.driver, self.timeout*60).until_not(
                EC.presence_of_element_located((By.XPATH, '//div[@id="messagestack"]//span[text()="Loading..."]'))
            )
            self.driver.switch_to.frame(self.driver.find_element_by_name("messagecontframe"))                                  
        except TimeoutException:
            print('\terror => cannot load message body!')
            return False          

        try:
            self.otp_code = self.driver.find_element_by_xpath('//div[@id="messagebody"]/div/div/center/span').text    
            print('\tsuccess => {}'.format(self.otp_code))                              
        except Exception as ex:
            print('\terror => cannot get otp code!')
            return False     

        return True

    def closeDriver(self):
        if self.driver:
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
                self.driver.close()                
            self.driver.quit()
            self.driver = None