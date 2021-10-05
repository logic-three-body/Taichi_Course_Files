import taichi as ti

ti.init(arch=ti.cpu)

'''python scope'''
def foo():
    print('Hi,Im in py')

foo()
'''python scope'''

@ti.kernel
def foo():
    print('Hi,Im in taichi')

foo()