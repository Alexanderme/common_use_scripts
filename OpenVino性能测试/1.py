"""
    #  @ModuleName: 1
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/9/24 16:04
"""
from functools import wraps

def log(fun):
    @wraps(fun)
    def b(*args, **kwargs):
        print(123)
        return fun(*args, **kwargs)
    return b



@log
def test(p):
    print(test.__name__ + " param: " + p)


test("I'm a param")