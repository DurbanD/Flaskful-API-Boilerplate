import re

tester = r"^[-!#$%&'*+\/0-9=?A-Z^_a-z`{|}~](\.?[-!#$%&'*+\/0-9=?A-Z^_a-z`{|}~])*@[a-zA-Z0-9](-*\.?[a-zA-Z0-9])*\.[a-zA-Z](-?[a-zA-Z0-9])+$"
def validate(email):
    if email == None:
        return False
    emailParts = email.split('@')
    if len(emailParts) != 2: 
        return False
    account = emailParts[0]
    address = emailParts[1]
    if len(account) > 64:
        return False
    elif len(address) > 255: 
        return False
    domainParts = address.split('.')
    if len(domainParts) < 2:
        return False
    for part in domainParts:
        if len(part) > 64:
            return False
    if re.search(tester, email) == False: 
        return False
    return True