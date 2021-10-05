import taichi as ti

ti.init(arch=ti.cpu)

ti.init(default_fp=ti.f32)  # float = ti.f32
#ti.init(default_fp=ti.f64)  # float = ti.f64
#ti.init(default_ip=ti.i32)  # int = ti.i32
#ti.init(default_ip=ti.i64)  # int = ti.i64

'''Type Promotion
    i32+f32=f32
    i32+i64=i64
    precise low -> high
'''

'''Impicit Cast'''


def foo():
    a = 1
    a = 2.7
    print(a)


foo()  # 2.7


@ti.kernel
def foo():
    a = 1
    a = 2.7
    print(a)


foo()  # 2
'''
[W 10/04/21 12:37:39.512 6368] [type_check.cpp:taichi::lang::TypeCheck::visit@145] [$9] Local store may lose precision (target = i64, value = f32) at
[W 10/04/21 12:37:39.512 6368] [type_check.cpp:taichi::lang::TypeCheck::visit@146] 
  File "E:/college class/coding/ComputerGraph/TaiChiCourse/Lec1/TaichiData.py", line 28, in foo
    a=2.7
  File "D:\Anaconda3\lib\site-packages\taichi\lang\common_ops.py", line 284, in assign
    return ti.assign(self, other)
  File "D:\Anaconda3\lib\site-packages\taichi\lang\ops.py", line 137, in wrapped
    return imp_foo(a, b)

2

'''

'''Impicit Cast'''

'''Type Cast'''


@ti.kernel
def foo():
    a = 1.7
    b = ti.cast(a, ti.i32)
    c = ti.cast(b, ti.f32)
    print("b:", b)  # 1
    print("c:", c)  # 1.000000


foo()
'''Type Cast'''

'''compound types'''

vec3f = ti.types.vector(3, ti.f32)
mat2f = ti.types.matrix(2, 2, ti.f32)
ray = ti.types.struct(orgin=vec3f, dir=vec3f, l=ti.f32)


@ti.kernel
def foo():
    # a=vec3f(0)
    # print(a)#[0, 0, 0]
    a = vec3f(0.0)
    print(a)  # [0.000000, 0.000000, 0.000000]
    d = vec3f(0.0, 1.0, 0.0)  # [0.000000, 1.000000, 0.000000]
    print(d)
    B = mat2f([[1.5, 1.4], [1.3, 1.2]])  # [[1.500000, 1.400000], [1.300000, 1.200000]]
    B = mat2f(0)  # [[0.000000, 0.000000], [0.000000, 0.000000]]
    print(B)
    r = ray(orgin=a, dir=d, l=1)
    print("r.orgin=", r.orgin)  # [0.000000, 0.000000, 0.000000]
    print("r.dir=", r.dir)  # [0.000000, 0.000000, 0.000000]
    print("r.l=", r.l)  # 1.000000


foo()

'''predefined'''

@ti.kernel
def foo():
    a=ti.Vector([0.,0.,0.])
    print(a)
    d=ti.Vector([0.,1.,0.])
    print(d)
    B=ti.Matrix([[1.5,1.4],[1.3,1.2],[3.,4.]])
    print('B=',B)#[[1.500000, 1.400000], [1.300000, 1.200000], [3.000000, 4.000000]]
    r=ti.Struct(v1=a,v2=d,l=1)
    print('r.v1:',r.v1)#[0.000000, 0.000000, 0.000000]
    print('r.v2:',r.v2)#[0.000000, 1.000000, 0.000000]
    print('r.l:',r.l)#1

    print(d[2])#0.000000
    print(B[0,1])#1.400000

    #print(d[3])#out of range
    print(B[2,1])#4.000000

foo()


'''predefined'''

'''compound types'''

'''ti.feld
a global N-d array of elements
    |_ can be read/written from both scope of taichi and python
          |_(Scalar:N=0),(Vector:N=1),(Matrix:N=2),(N=3,4,5)
                        |_scalar,vector,matrix,struct
'''

pixels=ti.field(dtype=float,shape=(3,4))
pixels[2,3]=42
pixels[7,5]=1#??? not out of range ???
print(pixels)
'''
[[ 0.  0.  0.  0.]
 [ 0.  0.  0.  0.]
 [ 0.  0.  0. 42.]]
'''
print(pixels[2,3])#42.0
print(pixels[3,4])#0 ???not out of range???
print(pixels[7,5])#1.0

vf = ti.Vector.field(3, ti.f32, shape=4)
a,b,c =1,2,3
vf[0]=ti.Vector([a,b,c])
print(vf)
print('vf[3000]=',vf[3000])#???[1. 2. 3.]???
print('vf[10]=',vf[10])#???[0. 0. 0.]???

'''
[[1. 2. 3.]
 [0. 0. 0.]
 [0. 0. 0.]
 [0. 0. 0.]]
'''


'''
#not understand the opertion of ti.field in ti.kernel yet
@ti.kernel
def foo() :
    #a,b,c=1,2,3
    v=ti.Vector([1.,2.,3.])
   # vf[0]=v
    #vf[0]=ti.Vector([a,b,c])
    

foo()
#v=ti.Vector([0,0,0])
#v=foo()
# print(foo())
# vf[0]=foo()
# print(vf[0])
'''

'''scaler'''

zero_d_scalar = ti.field(ti.f32,shape=())
zero_d_scalar[None]=1.5
print(zero_d_scalar)#1.5
zero_d_vec = ti.Vector.field(2,ti.f32,shape=())
zero_d_vec[None]=ti.Vector([2.5,2.5])
print(zero_d_vec[None])#[2.5 2.5]
'''scaler'''

'''ti.feld'''