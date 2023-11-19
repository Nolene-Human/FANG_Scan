def password_check(passwd):
     
    SpecialSym =['$', '@', '#', '%','!']
    val = True
    
    if len(passwd) < 6:
        msg='Length should be at least 6 characters'
        val = False

    if not any(char.isdigit() for char in passwd):
        msg=('Password should have at least one numeral value')
        val = False
         
    if not any(char.isupper() for char in passwd):
        msg=('Password should have at least one uppercase letter')
        val = False
         
    if not any(char.islower() for char in passwd):
        msg=('Password should have at least one lowercase letter')
        val = False
         
    if not any(char in SpecialSym for char in passwd):
        msg=("Password should have at least one of the symbols '$', '@', '#', '%', '!' ")
        val = False
    if val:
        msg='Password Saved'
    
    return msg