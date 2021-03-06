# Numerical solution of a equation
# -u'' + qu = f with x on (a1,b1) and y on (a2,b2)
# phi1=u(x,a2)=x; phi2=u(a1,y)=y^3+1+y
# phi3=u(x,b2)=8x^2+x+2x; phi4=(u-du/dx)(b1,y)=-1-y

# Solution is u(x)= x^2*y^3+x+xy; q(x)= 1
# So f(x)=x^2*y^3+x+xy-2y^3-6yx^2

#  q(x) >= 0 on ((a1,b1),(a2,b2))
# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

A1 = 0
B1 = 1
A2 = 0
B2 = 2

# кол-во промежутков по Ox
# n=3
n = 50
# шаг по Ox
h1 = (B1 - A1) / n

# кол-во промежутков по Oy
# m=4
m = 100
# шаг по Oy
h2 = (B2 - A2) / m

q = 1


def f(x, y):
    return x ** 2 * (y ** 3) + x + x * y - 2 * (y ** 3) - 6 * y * (x ** 2)


def phi1(x, y):
    return x


def phi2(x, y):
    return y ** 3 + 1 + y


def phi3(x, y):
    return 8 * (x ** 2) + x + 2 * x


def phi4(x, y):
    return -1 - y


def matrix_portrait(M, caption):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i,j]!=0:
                plt.plot(i+1,j+1,'b*')
    plt.title(caption)
    plt.show()

# %%
# формирование матрицы A и правой части b СЛАУ Au=b
A = np.zeros((n * (m - 1), n * (m - 1)))
B = np.zeros((n * (m - 1), 1))

a = 2 / (h1 * h1) + 2 / (h2 * h2)
b = -1 / (h1 * h1)
c = -1 / (h2 * h2)
d = 1 / h1
a1= h1 / (2 * h2 * h2)
b1= h1 / 2

for i in range(n * (m - 1)):
    x = A1 + (i % n) * h1
    y = A2 + (int(i / n) + 1) * h2
    if i % n == 0:
        # A[i, i] =1+d + b1 * q + 2*a1
        # A[i, i] =1+d - b1 * q - 2*a1
        # A[i, i + 1] = -d
        # B[i] = phi4(x, y) - b1 * f(x, y)

        A[i, i] =1+d + b1 * q + 2*a1
        A[i, i + 1] = -d
        B[i] = phi4(x, y) + b1 * f(x, y)
        if i==0:
            B[i]-= a1 * phi1(A1, B1)
        else:
            A[i, i - n] = a1
        if i==(m-2)*n:
            B[i]-= a1 * phi3(A1, B2)
        else:
            A[i, i + n] = a1
    else:
        A[i, i] = a + q
        A[i, i - 1] = b
        B[i] = f(x, y)
        if i % n == n - 1:
            B[i]-= b * phi2(B1, y)
        else:
            A[i, i + 1] = b

        if i - n > 0:
            A[i, i - n] = c
        else:
            B[i] -= c * phi1(x, A2)

        if i + n < n * (m - 1):
            A[i, i + n] = c
        else:
            B[i] -= c * phi3(x, B2)

matrix_portrait(A,"The matrix portrait")

U = np.linalg.solve(A, B)
u = np.zeros((m - 1, n))
for i in range(m - 1):
    for j in range(n):
        u[i, j] = U[i * n + j]

# print(u)
Phi2 = np.array([[phi2(B1, A2 + i * h2) for i in range(1,m)]]).T

# print(Phi2)
u = np.c_[u, Phi2]
# The resulting function
u = np.r_[np.array([[phi1(A1 + i * h1, A2) for i in range(n + 1)]]), u, np.array(
    [[phi3(A1 + i * h1, A2) for i in range(n + 1)]])]
print("The resulting function", u)


# %% Check
def u_t(x, y):
    return x ** 2 * (y ** 3) + x + x * y


u_t_d = np.zeros((m + 1, n + 1))

for i in range(m + 1):
    for j in range(n + 1):
        u_t_d[i, j] = u_t(A1 + h1 * j, A2 + h2 * i)

# print(u_t_d)

MSE = (abs(u_t_d - u) ** 2).sum() / ((n + 1) * (m + 1))
print("MSE: ", MSE)

X = np.linspace(A1, B1, n + 1)
Y = np.linspace(A2, B2, m + 1)
X, Y = np.meshgrid(X, Y)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# The resulting function
ax.plot_surface(X, Y, u, cmap='plasma')
plt.title("O(h^2)_numerical_solution")
plt.savefig("O(h^2)_numerical_solution.png")
plt.show()

# Original function
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X, Y, u_t(X, Y), cmap='plasma')
plt.title("O(h^2)_original function")
plt.savefig("O(h^2)_original_function.png")
plt.show()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X, Y, abs(u_t(X, Y) - u), cmap='plasma')
plt.title("O(h^2)_residues")
plt.savefig("O(h^2)_residues.png")
plt.show()

pd.DataFrame(u).to_csv("O(h^2)_numerical_solution.csv")