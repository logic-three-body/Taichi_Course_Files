import taichi as ti

ti.init(arch=ti.cpu)


def foo():
    for i in range(10000):  # Serial
        print(i)


# foo()

@ti.kernel
def foo():
    for i in range(10000):  # Parallel
        print(i)
        for b in range(10):
            if (b == 7):
                break;


foo()
print('finish')

N = 100
x = ti.Vector.field(2, dtype=ti.i32, shape=(N, N))


@ti.kernel
def foo():
    for i, j in x:
        x[i, j] = ti.Vector([i, j])
        '''
        for b,c in x
            x[i,j]=ti.Vector([a,b])
            print(x[i,j])
        '''
        '''
        RuntimeError: [simplify.cpp:taichi::lang::Simplify::visit@581] 
        Nested struct-fors are not supported for now. Please try to use range-fors for inner loops.
        '''
        print(x[i, j])


foo()
print(x)
vf = ti.Vector.field(3, dtype=ti.f32, shape=4)
a, b, c = 1, 2, 3


@ti.kernel
def foo():
    # v = ti.Vector([1., 2., 3.])
    # vf[0]=v
    vf[0] = ti.Vector([a, b, c])
    print(vf[0])


foo()
print(vf)


@ti.kernel
def my_kernel()->ti.i32:
    return 233.666
print(my_kernel())#233