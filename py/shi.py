#
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import cm
# from mpl_toolkits import mplot3d
# # Space and time domain
# M,  N,  K   = 300,  300,  4000
# Dx, Dy, Dt  = 0.03, 0.03, 1e-4
#
# # Material Properties
# tau = 3e-4
# eps_bar = 0.01
# sigma = 0.02
# J = 4.
# theta_0 = 0.2
# alpha = 0.9
# gamma = 10.
# T_eq = 1.
# kappa = 1.8
#
# #%% Evolution
# p = np.zeros((M, N))
# T = np.zeros((M, N))
# # Initial Solidification area
# for i in range(M):
#     for j in range(N):
#         if (i - M/2)**2 + (j - N/2)**2 < 5.0:
#             p[i, j] = 1.0
#
# # Define Laplacian operator
# def Lap(p):
#     p_i_j  = np.delete(np.delete(p, [0, -1], axis=0), [0, -1], axis=1)
#     p_im_j = np.delete(np.delete(p, [0, -1], axis=0), [-1,-2], axis=1)
#     p_ip_j = np.delete(np.delete(p, [0, -1], axis=0), [0,  1], axis=1)
#     p_i_jm = np.delete(np.delete(p, [0, -1], axis=1), [0,  1], axis=0)
#     p_i_jp = np.delete(np.delete(p, [0, -1], axis=1), [-1,-2], axis=0)
#     Lap_p  = (p_im_j + p_ip_j + p_i_jm + p_i_jp - 4*p_i_j)/Dx**2
#     Lap_pj = np.vstack((Lap_p[0,:], Lap_p, Lap_p[-1,:]))
#     return np.hstack((Lap_pj[:,0].reshape(N,1), Lap_pj, Lap_pj[:,-1].reshape(N,1)))
#
# # Phase field evolution
# def Phase_field(p, T):
#     theta = np.arctan2(np.gradient(p, Dy, axis=1), np.gradient(p, Dx, axis=0))
#     eps = eps_bar * (1. + sigma * np.cos(J * (theta - theta_0)))
#     g = -eps * eps_bar * sigma * J * np.sin(J * (theta - theta_0)) * np.gradient(p, Dy, axis=1)
#     h = -eps * eps_bar * sigma * J * np.sin(J * (theta - theta_0)) * np.gradient(p, Dx, axis=0)
#     m = alpha/np.pi * np.arctan(gamma * (T_eq - T))
#     term_1 = - p*(p - 1.)*(p - 0.5 + m)
#     term_2 = - np.gradient(g, Dx, axis=0)
#     term_3 = np.gradient(h, Dy, axis=1)
#     term_4 = eps**2 * Lap(p)
#     p_ev = Dt / tau * (term_1 + term_2 + term_3 + term_4)
#     return p + p_ev
#
# # Temperature evolution
# def Temp(T, p_new, p_old):
#     T_ev = Dt*Lap(T) + kappa*(p_new - p_old)
#     return T + T_ev
#
# # Evolution process
# # p_hist = []
# # T_hist = []
# p_old = p; T_old = T
# for t_step in range(K):
#     p_new = Phase_field(p_old, T_old)
#     T_new = Temp(T_old, p_new, p_old)
#     p_old = p_new
#     T_old = T_new
#     plt.clf()
#     X, Y = np.meshgrid(range(N), range(M))
#     plt.imshow(p_old, extent=[np.min(X), np.max(X), np.min(Y), np.max(Y)])
#     plt.colorbar()
#     plt.show(block=False)
#     plt.pause(0.01)
#     # if t_step % 50 == 0:
#     #     p_hist.append(p_new)
#     #     T_hist.append(T_new)
#





'''
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection='3d')
'''
'''
p_hist = []
T_hist = []
p_old = p
T_old = T
for t_step in range(K):
    p_new = Phase_field(p_old, T_old)
    T_new = Temp(T_old, p_new, p_old)
    p_old = p_new
    T_old = T_new

    if t_step % 50 == 0:
        p_hist.append(p_new)
        T_hist.append(T_new)
        print('Step finished:', t_step, '/', str(K))
        '''


'''
 # Clear the plot
ax.cla()

# Create grid coordinates for 3D plot
X, Y = np.meshgrid(range(N), range(M))

# Plot the phase field
ax.plot_surface(X, Y, p_new, cmap='gray')
ax.set_title('Phase Field (Step {})'.format(t_step))
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Phase Field')
plt.show()

'''































'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import i1

# Parameters
D = 1
lam = 10
gamma_y = 1
kappa = 1
N = 10
T = 1
dt = 0.01
dx = 0.01

# Grid
x = np.arange(0, 1 + dx, dx)
y = np.arange(0, 1 + dx, dx)
t = np.arange(0, T + dt, dt)
Nx = len(x)
Ny = len(y)
Nt = len(t)

# Initialize arrays
u = np.zeros((Nx, Nt))
v = np.zeros((Nx, Nt))
k = np.zeros((Nx, Ny))
q = np.zeros((Nx, Ny))
gamma = np.zeros((Nx, Ny))
U = np.zeros(Nt)

# Initial conditions
u[:, 0] = 0
v[:, 0] = 0
k[:, 0] = 0

# Compute k(x, y)
for i in range(Nx):
    for j in i:
        k[i, j] = k[i, j - 1] + dt * (k[i + 1, j - 1] - 2 * k[i, j - 1] + k[i - 1, j- 1]) / dx ** 2 + dt * lam * k[
            i, j- 1]
        if j==i:
          k[j,j]=-5*j*dx

       

# Compute q(x, y)
for i in range(Nx):
    for j in range(Ny):
        q[i, j] = -gamma_y * (x[i] - y[j])

# Compute gamma(x, y)
for i in range(Nx):
    for j in range(Ny):
        for n in range(1, N+1):
            gamma[i, j] += 2 * np.exp(D * (lam - n**2 * np.pi**2) * kappa) * np.sin(n * np.pi * y[j]) * \
                          np.sin(n * np.pi * x[i]) * np.trapz(np.sin(n * np.pi * y) * k[1, :], y)

# Compute U(t)
for k in range(Nt):
    U[k] = np.trapz(y * u[:, k], y) + D * np.trapz(q[1, :] * v[:, k], y)

# Compute v(x, t)
for i in range(Nx):
    for k in range(Nt):
        v[i, k] = U[k + 1]
        if i == Nx-1:
        else:
         U[k + 1 + int(D * (x[i] - 1) / dx)]

# Compute u(x, t)
for k in range(1, Nt):
    for i in range(1, Nx - 1):
        u[i, k] = u[i, k-1] + dt * (u[i+1, k-1] - 2 * u[i, k-1] + u[i-1, k-1]) / dx**2 + dt * lam * u[i, k-1]

# Plot u(x, t)
X, T = np.meshgrid(x, t)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, T, u.T, cmap='viridis')
ax.set_xlabel('x')
ax.set_ylabel('t')
ax.set_zlabel('u')
ax.set_title('u(x, t)')
plt.show()
'''



'''
import numpy as np
from scipy.special import iv
from scipy.integrate import quad

# 定义常数
D = 1
lambda_val = 1
pi_val = np.pi

# 定义k(x, y)
def k(x, y, lambda_val):
    return -lambda_val * y * iv(1, np.sqrt(lambda_val * (x**2 - y**2))) / np.sqrt(lambda_val * (x**2 - y**2))

# 定义q(x, y)
def q(x, y):
    return -D * (y - x)

# 定义gamma(x, y)
def gamma(x, y, lambda_val, D):
    gamma_val = 0
    for n in range(1, 100): # 迭代100次
        gamma_val += (2 * np.exp((D * (lambda_val - n**2 * pi_val**2)) / D) * np.sin(n * pi_val * y) *
                     quad(lambda s: np.sin(n * pi_val * s) * k(1, s, lambda_val), 0, 1)[0])
    return gamma_val

# 定义v(x, y)
def v(x, y):
    return U(y + D * (x - 1))

# 定义U(y)
def U(y, lambda_val, D, gamma, u, q):
    u_int = quad(lambda x: gamma(1, x, lambda_val, D) * u(x, y), 0, 1)[0]
    v_int = D * quad(lambda x: q(1, x) * v(x, y), 0, 1)[0]
    return u_int + v_int

# 定义u(x, y)的偏微分方程
def u_pde(x, y, u):
    return u(y)

# 定义u(x, y)的边界条件
def u_bc(u):
    u[0, :] = 0
    u[-1, :] = v(0, np.linspace(0, 1, u.shape[1]))
    return u

# 定义v(x, y)的偏微分方程
def v_pde(x, y, v):
    return D * v[:, 1:] - v[:, :-1]

# 定义v(x, y)的边界条件
def v_bc(v):
    v[-1, :] = U(np.linspace(0, 1, v.shape[1]))
    return v

# 定义求解u(x, y)和v(x, y)的函数
def solve_uv(lambda_val, D):
    # 离散化区域
    x = np.linspace(0, 1, 101)
    y = np.linspace(0, 1, 101)

    # 初始化u(x, y)和v(x, y)
    u = np.zeros((len(x), len(y)))
    v = np.zeros((len(x), len(y)))

    # 使用隐式差分方法求解u(x, y)和v(x, y)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    dt = 0.001
    timesteps = 1000
    alpha = D * dt / dx**2
    beta = lambda_val * dt
    gamma_val = gamma(x, y, lambda_val, D)

    for n in range(timesteps):
        # 使用隐式差分方法更新u(x, y)
        u_new = np.zeros_like(u)
        for i in range(1, len(x) - 1):
            for j in range(1, len(y) - 1):
                u_new[i, j] = (1 - 2 * alpha - beta) * u[i, j] + alpha * (u[i+1, j] + u[i-1, j]) + beta * u[i, j+1]
        u_new = u_bc(u_new)
        u = u_new

        # 使用隐式差分方法更新v(x, y)
        v_new = np.zeros_like(v)
        for i in range(len(x)):
            for j in range(1, len(y)):
                v_new[i, j] = (1 - D * dt / dy) * v[i, j] + dt * (v[i, j-1] - v[i, j])
        v_new = v_bc(v_new)
        v = v_new

    return u, v

# 求解并输出结果
u, v = solve_uv(lambda_val, D)
print(u)
print(v)
'''














'''

'''

























































import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import matplotlib.animation as animation

# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import cm
# import matplotlib as mpl
# import matplotlib.animation as animation
#
#
# fig = plt.figure()
# frames_list = []
#
#
#
# def f(X,Y): # u(x,y,0) = f(x,y,0)
#     return X**2-np.arctan(X*Y)
#
# def g(X,Y): # u_t(x,y,0) = g(x,y,0)
#     return X/10000
#
# def laplacian(arr, row,col, dx ): # Laplacian in terms of FDM
#     return (arr[row + 1, col]
#                             + arr[row - 1, col] + arr[row, col + 1]
#                             + arr[row, col - 1]- 4*arr[row,col])/(dx**2)
#
# def simulation_pdes(rect,hs,BC, c, frames, eq):
#
#     """ Simulation of the heat and wave equation on a
#     2D rectangular grid using the Finite Difference Method """
#
#     X, Y = np.meshgrid(np.linspace(rect[0],rect[1],hs[0]),
#                        np.linspace(rect[2],rect[3],hs[1])) # 2D meshgrid
#
#     # Initial Conditions
#     Z_init = f(X,Y) # u(x,y,0) = f(x,y,0)
#     Z_0 = f(X,Y)
#     Z_dot_init = g(X,Y) # u_t(x,y,0) = g(x,y,0)
#     zs = []
#
#     # Max/min for colorbar
#     zmax = max(Z_init.max(), BC[0], BC[1], BC[2], BC[3])
#     zmin = min(Z_init.min(), BC[0], BC[1], BC[2], BC[3])
#
#     # Boundary Conditions
#     if eq == "Heat":
#         Z_init[0] = np.ones(len(Z_init[0])) * BC[0]
#         Z_init[-1] = np.ones(len(Z_init[-1]))* BC[1]
#         Z_init[:,0] =  np.ones(len(Z_init[:,0]))* BC[2]
#         Z_init[:, -1] = np.ones(len(Z_init[:, -1])) * BC[3]
#
#     # Figure settings
#     fig = plt.figure()
#     ax = plt.axes(projection='3d')
#     ax.axes.set_xlim3d(rect[0], rect[1])
#     ax.axes.set_ylim3d(rect[2], rect[3])
#     ax.axes.set_zlim3d(zmin, zmax)
#     plt.rcParams['mathtext.fontset'] = 'stix'
#     plt.rcParams['font.family'] = 'STIXGeneral'
#
#     # Lines constituting the rectangle
#     ax.plot([rect[0], rect[1]], [rect[2], rect[2]], [BC[0], BC[0]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[2], rect[3]], [BC[3], BC[3]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[0]], [rect[2], rect[3]], [BC[2], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[1]], [rect[3], rect[3]], [BC[1], BC[1]], color='black', linewidth=2)
#
#     ax.plot([rect[0], rect[0]], [rect[2], rect[2]], [BC[0], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[2], rect[2]], [BC[0], BC[3]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[0]], [rect[3], rect[3]], [BC[1], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[3], rect[3]], [BC[1], BC[3]], color='black', linewidth=2)
#
#     # Infitesimals
#     dx = (rect[1] - rect[0]) / ((hs[0] - 1))
#     if eq == 'Heat':
#         dt = dx**2/(10*c**2)
#     else:
#         dt = dx/(10*c)
#
#     # Case separation for titles and labels
#     if eq == "Heat":
#         ax.set_title('Temperature development in a \n'
#                      'rectangular room', fontsize=18, fontname='STIXGeneral')
#         surf = ax.plot_surface(X, Y, Z_init, alpha=0.7, cmap=plt.cm.jet, vmin=zmin, vmax=zmax)
#         cbar = fig.colorbar(surf)
#         cbar.ax.set_ylabel('Temperature in ' + r'$^\circ\mathrm{C}$', rotation=270,fontsize = 14, labelpad=20)
#         ax.set_axis_off()
#
#     # if eq == "Wave":
#     #     ax.set_title('Simulation of water waves in a \n'
#     #                  'rectangular room', fontsize=18, fontname='STIXGeneral')
#     #     surf = ax.plot_surface(X, Y, Z_init, alpha=0.7, cmap="magma", vmin=zmin, vmax=zmax)
#     #     cbar = fig.colorbar(surf)
#     #     cbar.ax.set_ylabel('Water height in meters', rotation=270, fontsize=14, labelpad=20)
#     #     ax.set_axis_off()
#
#     # Finite Difference Method
#     # if eq == 'Wave':
#     #
#     #     # Creating first initial condition
#     #     for row in range(1, hs[0] - 1):
#     #         for col in range(1, hs[1] - 1):
#     #             Z_0[row,col] = Z_0[row,col] - 2 * laplacian(Z_dot_init,row,col, dx) + \
#     #                                 1/2 * c ** 2 * dt ** 2 * laplacian(Z_0, row, col, dx)
#     #
#     #     zs.append(Z_0)
#     #     zs.append(Z_init)
#
#         # for iteration in range(2,frames):
#         #     surf.remove()
#         #
#         #     # Creating temporary matrix
#         #     Z_temp = a = np.zeros((hs[0], hs[1]))
#         #     Z_temp[0] = np.ones(len(Z_temp[0])) * BC[0]
#         #     Z_temp[-1] = np.ones(len(Z_temp[-1])) * BC[1]
#         #     Z_temp[:, 0] = np.ones(len(Z_temp[:, 0])) * BC[2]
#         #     Z_temp[:, -1] = np.ones(len(Z_temp[:, -1])) * BC[3]
#         #
#         #     for row in range(1, hs[0]-1):
#         #         for col in range(1,hs[1]-1):
#         #             Z_temp[row,col] += 2 * zs[iteration - 1][row, col] - zs[iteration - 2][row, col] + \
#         #                                c ** 2 * dt ** 2 * laplacian(zs[iteration-1], row, col, dx)
#         #
#         #     zs.append(Z_temp)
#         #     # Plotting surface with slight pause
#         #     surf = ax.plot_surface(X, Y, zs[iteration-2], alpha = 1, cmap ="magma", vmin = zmin, vmax = zmax)
#         #     plt.pause(dt)
#
#     if eq == 'Heat':
#
#         for iteration in range(frames):
#             surf.remove()
#             for row in range(1, hs[0]-1):
#                 for col in range(1,hs[1]-1):
#                     Z_init[row,col] = Z_init[row,col] + c**2 * dt * laplacian(Z_init, row, col, dx)
#             # Plotting surface with slight pause
#             #surf =
#             # ax.plot_surface(X, Y, Z_init, alpha = 1, cmap =plt.cm.jet, vmin = zmin, vmax = zmax)
#             # #plt.pause(dt)
#             # plt.show()
#             # Modify this line:
#             surf = ax.plot_surface(X, Y, Z_init, alpha=1, cmap=plt.cm.jet, vmin=zmin, vmax=zmax)
#
#             # To this line:
#             frames_list.append([ax.plot_surface(X, Y, Z_init, alpha=1, cmap=plt.cm.jet, vmin=zmin, vmax=zmax)])
#         return frames_list
#
# def update(frame,ax):
#     ax.clear()
#     ax.axes.set_xlim3d(rect[0], rect[1])
#     ax.axes.set_ylim3d(rect[2], rect[3])
#     ax.axes.set_zlim3d(zmin, zmax)
#     ax.plot([rect[0], rect[1]], [rect[2], rect[2]], [BC[0], BC[0]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[2], rect[3]], [BC[3], BC[3]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[0]], [rect[2], rect[3]], [BC[2], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[1]], [rect[3], rect[3]], [BC[1], BC[1]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[0]], [rect[2], rect[2]], [BC[0], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[2], rect[2]], [BC[0], BC[3]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[0]], [rect[3], rect[3]], [BC[1], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[3], rect[3]], [BC[1], BC[3]], color='black', linewidth=2)
#     ax.set_title('Temperature development in a \n rectangular room', fontsize=18, fontname='STIXGeneral')
#     ax.set_axis_off()
#     #
#     #  the new surface plot
#
#     ax.collections[0].remove()  # Remove the previous surface plot
#     surf = ax.plot_surface(X, Y, frames_list[frame][0].get_array().data,
#                            alpha=1, cmap=plt.cm.jet, vmin=zmin, vmax=zmax)
#
# frames_list = simulation_pdes(rect=[-1, 1, -1, 1], hs=[50, 50], BC=[0, 0, 0, 0], c=2, frames=100, eq='Heat')
#
#
# # Create the animation
# ani = animation.ArtistAnimation(fig, frames_list, interval=100, repeat=True, blit=False)
#
#
# ani.save('heat_equation_animation.gif', writer='pillow')
# plt.rcParams['animation.convert_path'] = r'C:1'
#
# plt.show()

#simulation_pdes(rect = [-1,1,-1,1], hs = [50,50], BC = [0,0,0,0], c = 2, frames = 1000, eq = 'Heat')


# def f(X,Y): # u(x,y,0) = f(x,y,0)
#     return X**2-np.arctan(X*Y)
#
# def g(X,Y): # u_t(x,y,0) = g(x,y,0)
#     return X/10000
#
# def laplacian(arr, row,col, dx ): # Laplacian in terms of FDM
#     return (arr[row + 1, col]
#                             + arr[row - 1, col] + arr[row, col + 1]
#                             + arr[row, col - 1]- 4*arr[row,col])/(dx**2)
#
# def simulation_pdes(rect,hs,BC, c, frames, eq):
#
#     """ Simulation of the heat and wave equation on a
#     2D rectangular grid using the Finite Difference Method """
#
#     X, Y = np.meshgrid(np.linspace(rect[0],rect[1],hs[0]),
#                        np.linspace(rect[2],rect[3],hs[1])) # 2D meshgrid
#
#     # Initial Conditions
#     Z_init = f(X,Y) # u(x,y,0) = f(x,y,0)
#     Z_0 = f(X,Y)
#     Z_dot_init = g(X,Y) # u_t(x,y,0) = g(x,y,0)
#     zs = []
#
#     # Max/min for colorbar
#     zmax = max(Z_init.max(), BC[0], BC[1], BC[2], BC[3])
#     zmin = min(Z_init.min(), BC[0], BC[1], BC[2], BC[3])
#
#     # Boundary Conditions
#     if eq == "Heat":
#         Z_init[0] = np.ones(len(Z_init[0])) * BC[0]
#         Z_init[-1] = np.ones(len(Z_init[-1]))* BC[1]
#         Z_init[:,0] =  np.ones(len(Z_init[:,0]))* BC[2]
#         Z_init[:, -1] = np.ones(len(Z_init[:, -1])) * BC[3]
#
#     # Figure settings
#     fig = plt.figure()
#     ax = plt.axes(projection='3d')
#     ax.axes.set_xlim3d(rect[0], rect[1])
#     ax.axes.set_ylim3d(rect[2], rect[3])
#     ax.axes.set_zlim3d(zmin, zmax)
#     plt.rcParams['mathtext.fontset'] = 'stix'
#     plt.rcParams['font.family'] = 'STIXGeneral'
#
#     # Lines constituting the rectangle
#     ax.plot([rect[0], rect[1]], [rect[2], rect[2]], [BC[0], BC[0]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[2], rect[3]], [BC[3], BC[3]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[0]], [rect[2], rect[3]], [BC[2], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[1]], [rect[3], rect[3]], [BC[1], BC[1]], color='black', linewidth=2)
#
#     ax.plot([rect[0], rect[0]], [rect[2], rect[2]], [BC[0], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[2], rect[2]], [BC[0], BC[3]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[0]], [rect[3], rect[3]], [BC[1], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[3], rect[3]], [BC[1], BC[3]], color='black', linewidth=2)
#
#     # Infitesimals
#     dx = (rect[1] - rect[0]) / ((hs[0] - 1))
#     if eq == 'Heat':
#         dt = dx**2/(10*c**2)
#     else:
#         dt = dx/(10*c)
#
#     # Case separation for titles and labels
#     if eq == "Heat":
#         ax.set_title('Temperature development in a \n'
#                      'rectangular room', fontsize=18, fontname='STIXGeneral')
#         surf = ax.plot_surface(X, Y, Z_init, alpha=0.7, cmap=plt.cm.jet, vmin=zmin, vmax=zmax)
#         cbar = fig.colorbar(surf)
#         cbar.ax.set_ylabel('Temperature in ' + r'$^\circ\mathrm{C}$', rotation=270,fontsize = 14, labelpad=20)
#         ax.set_axis_off()
#
#     # if eq == "Wave":
#     #     ax.set_title('Simulation of water waves in a \n'
#     #                  'rectangular room', fontsize=18, fontname='STIXGeneral')
#     #     surf = ax.plot_surface(X, Y, Z_init, alpha=0.7, cmap="magma", vmin=zmin, vmax=zmax)
#     #     cbar = fig.colorbar(surf)
#     #     cbar.ax.set_ylabel('Water height in meters', rotation=270, fontsize=14, labelpad=20)
#     #     ax.set_axis_off()
#
#     # Finite Difference Method
#     # if eq == 'Wave':
#     #
#     #     # Creating first initial condition
#     #     for row in range(1, hs[0] - 1):
#     #         for col in range(1, hs[1] - 1):
#     #             Z_0[row,col] = Z_0[row,col] - 2 * laplacian(Z_dot_init,row,col, dx) + \
#     #                                 1/2 * c ** 2 * dt ** 2 * laplacian(Z_0, row, col, dx)
#     #
#     #     zs.append(Z_0)
#     #     zs.append(Z_init)
#
#         # for iteration in range(2,frames):
#         #     surf.remove()
#         #
#         #     # Creating temporary matrix
#         #     Z_temp = a = np.zeros((hs[0], hs[1]))
#         #     Z_temp[0] = np.ones(len(Z_temp[0])) * BC[0]
#         #     Z_temp[-1] = np.ones(len(Z_temp[-1])) * BC[1]
#         #     Z_temp[:, 0] = np.ones(len(Z_temp[:, 0])) * BC[2]
#         #     Z_temp[:, -1] = np.ones(len(Z_temp[:, -1])) * BC[3]
#         #
#         #     for row in range(1, hs[0]-1):
#         #         for col in range(1,hs[1]-1):
#         #             Z_temp[row,col] += 2 * zs[iteration - 1][row, col] - zs[iteration - 2][row, col] + \
#         #                                c ** 2 * dt ** 2 * laplacian(zs[iteration-1], row, col, dx)
#         #
#         #     zs.append(Z_temp)
#         #     # Plotting surface with slight pause
#         #     surf = ax.plot_surface(X, Y, zs[iteration-2], alpha = 1, cmap ="magma", vmin = zmin, vmax = zmax)
#         #     plt.pause(dt)
#     frames_list = []
#     if eq == 'Heat':
#
#         for iteration in range(frames):
#             surf.remove()
#             for row in range(1, hs[0]-1):
#                 for col in range(1,hs[1]-1):
#                     Z_init[row,col] = Z_init[row,col] + c**2 * dt * laplacian(Z_init, row, col, dx)
#             # Plotting surface with slight pause
#             #surf =
#             # ax.plot_surface(X, Y, Z_init, alpha = 1, cmap =plt.cm.jet, vmin = zmin, vmax = zmax)
#             # #plt.pause(dt)
#             # plt.show()
#             # Modify this line:
#             ax.plot_surface(X, Y, Z_init, alpha=1, cmap=plt.cm.jet, vmin=zmin, vmax=zmax)
#
#             # To this line:
#             frames_list.append([ax.plot_surface(X, Y, Z_init, alpha=1, cmap=plt.cm.jet, vmin=zmin, vmax=zmax)])
#         return frames_list
#
# def update(frame,ax):
#     ax.clear()
#     ax.axes.set_xlim3d(rect[0], rect[1])
#     ax.axes.set_ylim3d(rect[2], rect[3])
#     ax.axes.set_zlim3d(zmin, zmax)
#     ax.plot([rect[0], rect[1]], [rect[2], rect[2]], [BC[0], BC[0]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[2], rect[3]], [BC[3], BC[3]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[0]], [rect[2], rect[3]], [BC[2], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[1]], [rect[3], rect[3]], [BC[1], BC[1]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[0]], [rect[2], rect[2]], [BC[0], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[2], rect[2]], [BC[0], BC[3]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[0]], [rect[3], rect[3]], [BC[1], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[3], rect[3]], [BC[1], BC[3]], color='black', linewidth=2)
#     ax.set_title('Temperature development in a \n rectangular room', fontsize=18, fontname='STIXGeneral')
#     ax.set_axis_off()
#     ax.collections.clear()  # Remove the previous surface plot
#     ax.add_collection3d(frame[0])  # Add the new surface plot
#
# # import numpy as np
# # import matplotlib.pyplot as plt
# # from matplotlib import cm
# # import matplotlib as mpl
# # import matplotlib.animation as animation
# #
# # def f(X,Y): # u(x,y,0) = f(x,y,0)
# #     return X**2-np.arctan(X*Y)
# #
# # def g(X,Y): # u_t(x,y,0) = g(x,y,0)
# #     return X/10000
# #
# # def laplacian(arr, row,col, dx ): # Laplacian in terms of FDM
# #     return (arr[row + 1, col]
# #                             + arr[row - 1, col] + arr[row, col + 1]
# #                             + arr[row, col - 1]- 4*arr[row,col])/(dx**2)
# #
# # def simulation_pdes(rect,hs,BC, c, frames, eq):
# #
# #     """ Simulation of the heat and wave equation on a
# #     2D rectangular grid using the Finite Difference Method """
# #
# #     X, Y = np.meshgrid(np.linspace(rect[0],rect[1],hs[0]),
# #                        np.linspace(rect[2],rect[3],hs[1])) # 2D meshgrid
# #
# #     # Initial Conditions
# #     Z_init = f(X,Y) # u(x,y,0) = f(x,y,0)
# #     Z_0 = f(X,Y)
# #     Z_dot_init = g(X,Y) # u_t(x,y,0) = g(x,y,0)
# #     zs = []
# #
# #     # Max/min for colorbar
# #     zmax = max(Z_init.max(), BC[0], BC[1], BC[2], BC[3])
# #     zmin = min(Z_init.min(), BC[0], BC[1], BC[2], BC[3])
# #
# #     # Boundary Conditions
# #     if eq == "Heat":
# #         Z_init[0] = np.ones(len(Z_init[0])) * BC[0]
# #         Z_init[-1] = np.ones(len(Z_init[-1]))* BC[1]
# #         Z_init[:,0] =  np.ones(len(Z_init[:,0]))* BC[2]
# #         Z_init[:, -1] = np.ones(len(Z_init[:, -1])) * BC[3]
# #
# #     # Figure settings
# #     fig = plt.figure()
# #     ax = plt.axes(projection='3d')
# #     ax.axes.set_xlim3d(rect[0], rect[1])
# #     ax.axes.set_ylim3d(rect[2], rect[3])
# #     ax.axes.set_zlim3d(zmin, zmax)
# #     plt.rcParams['mathtext.fontset'] = 'stix'
# #     plt.rcParams['font.family'] = 'STIXGeneral'
# #
# #     # Lines constituting the rectangle
# #     ax.plot([rect[0], rect[1]], [rect[2], rect[2]], [BC[0], BC[0]], color='black', linewidth=2)
# #     ax.plot([rect[1], rect[1]], [rect[2], rect[3]], [BC[3], BC[3]], color='black', linewidth=2)
# #     ax.plot([rect[0], rect[0]], [rect[2], rect[3]], [BC[2], BC[2]], color='black', linewidth=2)
# #     ax.plot([rect[0], rect[1]], [rect[3], rect[3]], [BC[1], BC[1]], color='black', linewidth=2)
# #
# #     ax.plot([rect[0], rect[0]], [rect[2], rect[2]], [BC[0], BC[2]], color='black', linewidth=2)
# #     ax.plot([rect[1], rect[1]], [rect[2], rect[2]], [BC[0], BC[3]], color='black', linewidth=2)
# #     ax.plot([rect[0], rect[0]], [rect[3], rect[3]], [BC[1], BC[2]], color='black', linewidth=2)
# #     ax.plot([rect[1], rect[1]], [rect[3], rect[3]], [BC[1], BC[3]], color='black', linewidth=2)
# #
# #     # Infitesimals
# #     dx = (rect[1] - rect[0]) / ((hs[0] - 1))
# #     if eq == 'Heat':
# #         dt = dx**2/(10*c**2)
# #     else:
# #         dt = dx/(10*c)
# #
# #     # Case separation for titles and labels
# #     if eq == "Heat":
# #         ax.set_title('Temperature development in a \n'
# #                      'rectangular room', fontsize=18, fontname='STIXGeneral')
# #         surf = ax.plot_surface(X, Y, Z_init, alpha=0.7, cmap=plt.cm.jet, vmin=zmin, vmax=zmax)
# #         cbar = fig.colorbar(surf)
# #         cbar.ax.set_ylabel('Temperature in ' + r'$^\circ\mathrm{C}$', rotation=270,fontsize = 14, labelpad=20)
# #         ax.set_axis_off()
# #
# #     # if eq == "Wave":
# #     #     ax.set_title('Simulation of water waves in a \n'
# #     #                  'rectangular room', fontsize=18, fontname='STIXGeneral')
# #     #     surf = ax.plot_surface(X, Y, Z_init, alpha=0.7, cmap="magma", vmin=zmin, vmax=zmax)
# #     #     cbar = fig.colorbar(surf)
# #     #     cbar.ax.set_ylabel('Water height in meters', rotation=270, fontsize=14, labelpad=20)
# #     #     ax.set_axis_off()
# #
# #     # Finite Difference Method
# #     # if eq == 'Wave':
# #     #
# #     #     # Creating first initial condition
# #     #     for row in range(1, hs[0] - 1):
# #     #         for col in range(1, hs[1] - 1):
# #     #             Z_0[row,col] = Z_0[row,col] - 2 * laplacian(Z_dot_init,row,col, dx) + \
# #     #                                 1/2 * c ** 2 * dt ** 2 * laplacian(Z_0, row, col, dx)
# #     #
# #     #     zs.append(Z_0)
# #     #     zs.append(Z_init)
# #
# #         # for iteration in range(2,frames):
# #         #     surf.remove()
# #         #
# #         #     # Creating temporary matrix
# #         #     Z_temp = a = np.zeros((hs[0], hs[1]))
# #         #     Z_temp[0] = np.ones(len(Z_temp[0])) * BC[0]
# #         #     Z_temp[-1] = np.ones(len(Z_temp[-1])) * BC[1]
# #         #     Z_temp[:, 0] = np.ones(len(Z_temp[:, 0])) * BC[2]
# #         #     Z_temp[:, -1] = np.ones(len(Z_temp[:, -1])) * BC[3]
# #         #
# #         #     for row in range(1, hs[0]-1):
# #         #         for col in range(1,hs[1]-1):
# #         #             Z_temp[row,col] += 2 * zs[iteration - 1][row, col] - zs[iteration - 2][row, col] + \
# #         #                                c ** 2 * dt ** 2 * laplacian(zs[iteration-1], row, col, dx)
# #         #
# #         #     zs.append(Z_temp)
# #         #     # Plotting surface with slight pause
# #         #     surf = ax.plot_surface(X, Y, zs[iteration-2], alpha = 1, cmap ="magma", vmin = zmin, vmax = zmax)
# #         #     plt.pause(dt)
# #     frames_list = []
# #     if eq == 'Heat':
# #
# #         for iteration in range(frames):
# #             surf.remove()
# #             for row in range(1, hs[0]-1):
# #                 for col in range(1,hs[1]-1):
# #                     Z_init[row,col] = Z_init[row,col] + c**2 * dt * laplacian(Z_init, row, col, dx)
# #             # Plotting surface with slight pause
# #             #surf =
# #             # ax.plot_surface(X, Y, Z_init, alpha = 1, cmap =plt.cm.jet, vmin = zmin, vmax = zmax)
# #             # #plt.pause(dt)
# #             # plt.show()
# #             # Modify this line:
# #             ax.plot_surface(X, Y, Z_init, alpha=1, cmap=plt.cm.jet, vmin=zmin, vmax=zmax)
# #
# #             # To this line:
# #             frames_list.append([ax.plot_surface(X, Y, Z_init, alpha=1, cmap=plt.cm.jet, vmin=zmin, vmax=zmax)])
# #         return frames_list
# #
# # def update(frame,ax):
# #     ax.clear()
# #     ax.axes.set_xlim3d(rect[0], rect[1])
# #     ax.axes.set_ylim3d(rect[2], rect[3])
# #     ax.axes.set_zlim3d(zmin, zmax)
# #     ax.plot([rect[0], rect[1]], [rect[2], rect[2]], [BC[0], BC[0]], color='black', linewidth=2)
# #     ax.plot([rect[1], rect[1]], [rect[2], rect[3]], [BC[3], BC[3]], color='black', linewidth=2)
# #     ax.plot([rect[0], rect[0]], [rect[2], rect[3]], [BC[2], BC[2]], color='black', linewidth=2)
# #     ax.plot([rect[0], rect[1]], [rect[3], rect[3]], [BC[1], BC[1]], color='black', linewidth=2)
# #     ax.plot([rect[0], rect[0]], [rect[2], rect[2]], [BC[0], BC[2]], color='black', linewidth=2)
# #     ax.plot([rect[1], rect[1]], [rect[2], rect[2]], [BC[0], BC[3]], color='black', linewidth=2)
# #     ax.plot([rect[0], rect[0]], [rect[3], rect[3]], [BC[1], BC[2]], color='black', linewidth=2)
# #     ax.plot([rect[1], rect[1]], [rect[3], rect[3]], [BC[1], BC[3]], color='black', linewidth=2)
# #     ax.set_title('Temperature development in a \n rectangular room', fontsize=18, fontname='STIXGeneral')
# #     ax.set_axis_off()
# #     ax.collections.clear()  # Remove the previous surface plot
# #     ax.add_collection3d(frame[0])  # Add the new surface plot


#
#
# frames_list =simulation_pdes(rect = [-1,1,-1,1], hs = [50,50], BC = [0,0,0,0], c = 2, frames = 1000, eq = 'Heat')
#
# # Create the animation
# ani = animation.ArtistAnimation(fig, frames_list, interval=100, repeat=True)
#
#
# ani.save('heat_equation_animation.gif', writer='imagemagick')
# plt.show()
#
# #simulation_pdes(rect = [-1,1,-1,1], hs = [50,50], BC = [0,0,0,0], c = 2, frames = 1000, eq = 'Heat')



































# import matplotlib.pyplot as plt
# import numpy as np
# import math
# from matplotlib import cm
# from scipy import interpolate
#
#
# # 函数变量Coordx,Coordy，Strain为绘制云图的初始数据，分别为X,Y坐标以及坐标处对应的值。
# # minX,maxX,minY,maxY为二维云图绘制的坐标范围，figName为图名。
# def plot_contour(Coordx, Coordy, Strain, minX, maxX, minY, maxY, figName):
#     X = np.linspace(minX, maxX, 1000)
#     Y = np.linspace(minY, maxY, 1000)
#     # 生成二维数据坐标点，可以想象成围棋棋盘上的一个个落子点
#     X1, Y1 = np.meshgrid(X, Y)
#     # 通过griddata函数插值得到所有的(X1, Y1)处对应的值，原始数据为Coordx, Coordy, Strain
#     Z = interpolate.griddata((Coordx, Coordy), Strain, (X1, Y1), method='cubic')
#
#     fig, ax = plt.subplots(figName, figsize=(12, 8))
#
#     # level设置云图颜色范围以及颜色梯度划分，只能显示0-601范围数值，每间隔20颜色变化
#     levels = range(0, 601, 20)
#     cset1 = ax.contourf(X1, Y1, Z, levels, cmap=cm.jet)
#     # 设置cmap为jet，最小值为蓝色，最大为红色，和有限元软件云图配色类似
#
#     # 设置图片在屏幕中出现的位置
#     mngr = plt.get_current_fig_manager()
#     mngr.window.wm_geometry("+350+50")
#
#     ax.set_title(figName, size=20)  # 设置图名
#     # 设置云图坐标范围以及坐标轴标签
#     ax.set_xlim(minX, maxX)
#     ax.set_ylim(minY, maxY)
#     ax.set_xlabel("X(mm)", size=15)
#     ax.set_ylabel("Y(mm)", size=15)
#
#     # 设置colorbar的刻度，标签
#     cbar = fig.colorbar(cset1)
#     cbar.set_label('strain(με)', size=18)
#     cbar.set_ticks([0, 100, 200, 300, 400, 500, 600])
#
#     # 保存图片，bbox_inches设置图片周边空白的大小
#     fig.savefig(figName + ".png", bbox_inches='tight', dpi=150, pad_inches=0.1)
#     plt.show()  # 是否显示图片
#
#     return ()


#The following code sample describes the solving a
#partial differential equation numerically.  The equation evaluated in
#this case is the 2D heat equation.  Look at a square copper plate with
#dimensions of 10 cm on a side.








# #STEP 1.  Import the libraries needed to perform the calculations.
#
# #Import the numeric Python and plotting libraries needed to solve the equation.
# import numpy as np
# import matplotlib.pyplot as plt
#
#
#
#
#
#
#
#
# #STEP 2.  Set up the position and time grids (or axes).
#
# #Set up the position information.
# axis_size = 100     #Size of the 1D grid.
# side_length = 10    #Length of one side of the square plate (cm)
# dx = side_length/axis_size   #Space step
# axis_points = np.linspace(0,10,axis_size)   #Spatial grid points for the plate.
#
# #Set up the time grid to calcuate the equation.
# T = 1.0                                       #Total time (s)
# k = 1.011                                     #Thermal diffusivity of the plate in units of cm^2/s.
# dt = ((1/axis_size)**2)/(2*k)                 #Time step size to ensure a stable discretization scheme.
# n = int(T/dt)                                 #Total number of time steps.
#
# #Set maximum initial temperature (in degrees Celsius)
# max_temp = 100
#
#
#
#
#
#
#
#
# #STEP 3.  Initialization conditions for the 2D heat equation.
# #Set up initial temperature in the plate.  The initial temperature will be a Gaussian,
# #With the hottest temperature at the middle of the plate and it will be cooler at the edges.
#
# #Function to calculate the initial temperature of the plate.  It will be hottest at the plate center,
# #at the maximum initial temperature.
# def temp_init(x,y,c,m_temp):
#     return m_temp*np.exp(-((x-side_length/2)**2 + (y-side_length/2)**2)/c**2)
#
# #Create a meshgrid for the 3D function of initial temperature.
# X, Y = np.meshgrid(axis_points, axis_points)
#
# #denominator in the Gaussian (proportional to standard deviation).
# c = 2
#
# #Calculate the initial plate temperature using the temperature initialization function.  This is the initial
# #condition of the plate.
# U = temp_init(X, Y, c, max_temp)
#
# #Set up some boundary conditions at the edges of the plate for the initial plate condition at t = 0.
# #Set plate edge temperatures in degrees Celsius.  The bottom edge is set to be quite hot in this case.
# U[:,0] = 20
# U[:,-1] = 5
# U[0,:] = 10
# U[-1,:] = 70
#
# #Assign initial boundary conditions to their own variables.
# B1 = U[:,0]
# B2 = U[:,-1]
# B3 = U[0,:]
# B4 = U[-1,:]
#
# #Plot the results of the equation.  Use the hot colormap to show
# #the initial heat distribution.
# plt.imshow(U, cmap ='hot', vmin = 0, vmax = max_temp, extent= [0,10,0,10])
# plt.tick_params(axis='both', which='major', labelsize=16)
# plt.xlabel('Horizontal plate edge (cm)', fontsize = 16)
# plt.ylabel('Vertical plate edge (cm)', fontsize = 16)
# plt.title('Initial temperature map')
# plt.show()
#
#
#
#
#
#
#
#
#
# #STEP 4.  Laplacian numerical approximation using 5-point stencil finite difference methods.
# def laplacian(Z,d_ex):
#     Ztop = Z[0:-2,1:-1]
#     Zleft = Z[1:-1,0:-2]
#     Zbottom = Z[2:,1:-1]
#     Zright = Z[1:-1,2:]
#     Zcenter = Z[1:-1,1:-1]
#     return (Ztop + Zleft + Zbottom + Zright - 4 * Zcenter) / d_ex**2
#
#
#
#
#
#
#
#
# #STEP 5.   Now solve the PDE for a result of all spatial positions
# #after time T has elapsed.  Iterate over the specified time.
#
# for i in range(n):
#
#     #Perform the 3rd order differentiation on the function.
#     deltaU = laplacian(U,dx)
#
#     #Take the values of the function inside, but not including
#     #the first and last elements.
#     Uc = U[1:-1,1:-1]
#
#     #Update the variables after rearranging the differential equation.
#     U[1:-1,1:-1] = Uc + dt * (k*deltaU)
#
#     #Direchlet boundary conditions.  The edges of the plate
#     #have steady state, constant temperatures over all time.
#     U[:,0] = B1
#     U[:,-1] = B2
#     U[0,:] = B3
#     U[-1,:] = B4
#
#
#
#
#
#
#
#
#
# #STEP 6.   Show the new temperature distribution on the plate after the
# #time has elapsed.  Use the hot colormap to show the heat distribution.
# plt.imshow(U,cmap = 'hot', vmin = 0, vmax = max_temp, extent= [0,10,0,10])
# plt.tick_params(axis='both', which='major', labelsize=16)
# plt.xlabel('Horizontal plate edge (cm)', fontsize = 16)
# plt.ylabel('Vertical plate edge (cm)', fontsize = 16)
# plt.title('Final temperature map')
# plt.show()









#








#
#
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import cm
# import matplotlib as mpl
#
# def f(X,Y): # u(x,y,0) = f(x,y,0)
#     return X**2-np.arctan(X*Y)
#
# def g(X,Y): # u_t(x,y,0) = g(x,y,0)
#     return X/10000
#
# def laplacian(arr, row,col, dx ): # Laplacian in terms of FDM
#     return (arr[row + 1, col]
#                             + arr[row - 1, col] + arr[row, col + 1]
#                             + arr[row, col - 1]- 4*arr[row,col])/(dx**2)
#
# def simulation_pdes(rect,hs,BC, c, frames, eq):
#
#     """ Simulation of the heat and wave equation on a
#     2D rectangular grid using the Finite Difference Method """
#
#     X, Y = np.meshgrid(np.linspace(rect[0],rect[1],hs[0]),
#                        np.linspace(rect[2],rect[3],hs[1])) # 2D meshgrid
#
#     # Initial Conditions
#     Z_init = f(X,Y) # u(x,y,0) = f(x,y,0)
#     Z_0 = f(X,Y)
#     Z_dot_init = g(X,Y) # u_t(x,y,0) = g(x,y,0)
#     zs = []
#
#     # Max/min for colorbar
#     zmax = max(Z_init.max(), BC[0], BC[1], BC[2], BC[3])
#     zmin = min(Z_init.min(), BC[0], BC[1], BC[2], BC[3])
#
#     # Boundary Conditions
#     if eq == "Heat":
#         Z_init[0] = np.ones(len(Z_init[0])) * BC[0]
#         Z_init[-1] = np.ones(len(Z_init[-1]))* BC[1]
#         Z_init[:,0] =  np.ones(len(Z_init[:,0]))* BC[2]
#         Z_init[:, -1] = np.ones(len(Z_init[:, -1])) * BC[3]
#
#     # Figure settings
#     fig = plt.figure()
#     ax = plt.axes(projection='3d')
#     ax.axes.set_xlim3d(rect[0], rect[1])
#     ax.axes.set_ylim3d(rect[2], rect[3])
#     ax.axes.set_zlim3d(zmin, zmax)
#     plt.rcParams['mathtext.fontset'] = 'stix'
#     plt.rcParams['font.family'] = 'STIXGeneral'
#
#     # Lines constituting the rectangle
#     ax.plot([rect[0], rect[1]], [rect[2], rect[2]], [BC[0], BC[0]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[2], rect[3]], [BC[3], BC[3]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[0]], [rect[2], rect[3]], [BC[2], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[1]], [rect[3], rect[3]], [BC[1], BC[1]], color='black', linewidth=2)
#
#     ax.plot([rect[0], rect[0]], [rect[2], rect[2]], [BC[0], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[2], rect[2]], [BC[0], BC[3]], color='black', linewidth=2)
#     ax.plot([rect[0], rect[0]], [rect[3], rect[3]], [BC[1], BC[2]], color='black', linewidth=2)
#     ax.plot([rect[1], rect[1]], [rect[3], rect[3]], [BC[1], BC[3]], color='black', linewidth=2)
#
#     # Infitesimals
#     dx = (rect[1] - rect[0]) / ((hs[0] - 1))
#     if eq == 'Heat':
#         dt = dx**2/(10*c**2)
#     else:
#         dt = dx/(10*c)
#
#     # Case separation for titles and labels
#     if eq == "Heat":
#         ax.set_title('Temperature development in a \n'
#                      'rectangular room', fontsize=18, fontname='STIXGeneral')
#         surf = ax.plot_surface(X, Y, Z_init, alpha=0.7, cmap=plt.cm.jet, vmin=zmin, vmax=zmax)
#         cbar = fig.colorbar(surf)
#         cbar.ax.set_ylabel('Temperature in ' + r'$^\circ\mathrm{C}$', rotation=270,fontsize = 14, labelpad=20)
#         ax.set_axis_off()
#
#     if eq == "Wave":
#         ax.set_title('Simulation of water waves in a \n'
#                      'rectangular room', fontsize=18, fontname='STIXGeneral')
#         surf = ax.plot_surface(X, Y, Z_init, alpha=0.7, cmap="magma", vmin=zmin, vmax=zmax)
#         cbar = fig.colorbar(surf)
#         cbar.ax.set_ylabel('Water height in meters', rotation=270, fontsize=14, labelpad=20)
#         ax.set_axis_off()
#
#     # Finite Difference Method
#     if eq == 'Wave':
#
#         # Creating first initial condition
#         for row in range(1, hs[0] - 1):
#             for col in range(1, hs[1] - 1):
#                 Z_0[row,col] = Z_0[row,col] - 2 * laplacian(Z_dot_init,row,col, dx) + \
#                                     1/2 * c ** 2 * dt ** 2 * laplacian(Z_0, row, col, dx)
#
#         zs.append(Z_0)
#         zs.append(Z_init)
#
#         for iteration in range(2,frames):
#             surf.remove()
#
#             # Creating temporary matrix
#             Z_temp = a = np.zeros((hs[0], hs[1]))
#             Z_temp[0] = np.ones(len(Z_temp[0])) * BC[0]
#             Z_temp[-1] = np.ones(len(Z_temp[-1])) * BC[1]
#             Z_temp[:, 0] = np.ones(len(Z_temp[:, 0])) * BC[2]
#             Z_temp[:, -1] = np.ones(len(Z_temp[:, -1])) * BC[3]
#
#             for row in range(1, hs[0]-1):
#                 for col in range(1,hs[1]-1):
#                     Z_temp[row,col] += 2 * zs[iteration - 1][row, col] - zs[iteration - 2][row, col] + \
#                                        c ** 2 * dt ** 2 * laplacian(zs[iteration-1], row, col, dx)
#
#             zs.append(Z_temp)
#             # Plotting surface with slight pause
#             surf = ax.plot_surface(X, Y, zs[iteration-2], alpha = 1, cmap ="magma", vmin = zmin, vmax = zmax)
#             plt.pause(dt)
#
#     if eq == 'Heat':
#
#         for iteration in range(frames):
#             surf.remove()
#             for row in range(1, hs[0]-1):
#                 for col in range(1,hs[1]-1):
#                     Z_init[row,col] = Z_init[row,col] + c**2 * dt * laplacian(Z_init, row, col, dx)
#             # Plotting surface with slight pause
#             surf = ax.plot_surface(X, Y, Z_init, alpha = 1, cmap =plt.cm.jet, vmin = zmin, vmax = zmax)
#             plt.pause(dt)
#
# simulation_pdes(rect = [-1,1,-1,1], hs = [50,50], BC = [0,0,0,0], c = 2, frames = 1000, eq = 'Heat')










#################################################################################























# import matplotlib.pyplot as plt
# import numpy as np
# import cv2
#
#
# inputimage = cv2.imread(r"C:\Users\76598\Desktop\just for fun\12.jpg")
# dimensions = list(inputimage.shape)
# # fetching image dimensions
# imwidth = dimensions[0]
# imheight = dimensions[1]
#
# num = 10000000  # no_of_samples
#
#
# def image_to_matrix(image, width, height):
#     'converting color image to BnW image, then creating matrix T from position of each pixel'
#     'T is then returned as a normalized probability distribution over width x height'
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     T = cv2.bitwise_not(gray_image)
#     return np.array(T) / (255 * width * height)
#
#
# prop_distribution = image_to_matrix(inputimage, imwidth, imheight)  # proposed distribution
#
#
# def im_posterior_func(x):
#     return prop_distribution.item((int(np.floor(x[0])), int(np.floor(x[1]))))
#
#
#
#
# def sampler(posterior_func, Np, width, height, no_of_samples=4, start_position=None):
#     'Metropolis-hastings-algorithm'
#     # starting parameter position
#     if start_position == None:
#         current_position = [0, 0]
#     else:
#         assert len(start_position) == Np, "start_position is not correct length"
#         current_position = [0, 0]
#
#     samples = [list(current_position)]
#     print(current_position)
#     # fixed covariance matrix
#
#     # Sampling loop
#     for i in range(no_of_samples):
#         # suggest new position
#         x = np.random.uniform(low=0, high=height)
#         y = np.random.uniform(low=0, high=width)
#         # x = max(0, min(x, height - 1))
#         # y = max(0, min(y, width - 1))
#         X_n = [x, y]
#
#         # Compute log posteriors of current and proposed position
#         cur_posterior = posterior_func(current_position)
#         prop_posterior = posterior_func(X_n)
#
#         # Acceptance probability
#         A = 1
#         if cur_posterior == 0:
#             current_position = X_n
#             samples.append(list(current_position))
#             continue
#         if prop_posterior / cur_posterior < 1:
#             A = prop_posterior / cur_posterior
#
#         # Possibly update position
#         if A >= 1:
#            current_position = X_n
#         else:
#         u = np.random.uniform(0, 1)
#          if A >= u:
#          current_position = X_n
#
#         # Extend the samples array vertically for each iteration
#         samples.append(list(current_position))
#     return np.array(samples)
#
#
#
#
#
# samples = sampler(im_posterior_func, 2, imwidth, imheight, no_of_samples=num, start_position=None)  # position samples
# xs, ys = samples.T
#
#
# # def sampler(posterior_func, Np, width, height, no_of_samples=4, start_position=None):
# #     # ...
# #
# #     for i in range(no_of_samples):
# #         x = np.random.uniform(low=0, high=height)
# #         y = np.random.uniform(low=0, high=width)
# #
# #         # Clamp the proposed coordinates to the valid range
# #         x = max(0, min(x, height - 1))
# #         y = max(0, min(y, width - 1))
# #         X_n = [x, y]
# #
# #         # ...
# #
# #     # ...
#
#
#
#
#
#
#
# plt.hist2d(ys, -xs, bins=[np.arange(0, imheight, 1), np.arange(-imwidth, 0, 1)], cmap=plt.cm.binary)
# plt.show()



# #################################################################
# #没看出有什么高深的东西
# import matplotlib.pyplot as plt
# import numpy as np
# import cv2
#
# inputimage = cv2.imread(r"C:\Users\76598\Desktop\just for fun\12.jpg")
# dimensions = list(inputimage.shape)
# # fetching image dimensions
# imwidth = dimensions[0]
# imheight = dimensions[1]
#
# num = 10000000  # no_of_samples
#
#
# def image_to_matrix(image, width, height):
#     'converting color image to BnW image, then creating matrix T from position of each pixel'
#     'T is then returned as a normalized probability distribution over width x height'
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     T = cv2.bitwise_not(gray_image)
#     return np.array(T) / (255 * width * height)
#
#
#
# prop_distribution = image_to_matrix(inputimage, imwidth, imheight)  # proposed distribution
#
#
# def im_posterior_func(x):
#     return prop_distribution.item((int(np.floor(x[0])), int(np.floor(x[1]))))
#
#
# def sampler(posterior_func, Np, width, height, no_of_samples, start_position=None):
#     'Metropolis-hastings-algorithm'
#     # starting parameter position
#     if start_position == None:
#         current_position = [0, 0]
#     else:
#         assert len(start_position) == Np, "start_position is not correct length"
#         current_position = [0, 0]
#
#     samples = [list(current_position)]
#     print(current_position)
#     # fixed covariance matrix
#
#     # Sampling loop
#     for i in range(no_of_samples):
#         # suggest new position
#         x = np.random.uniform(low=0, high=height)
#         y = np.random.uniform(low=0, high=width)
#         X_n = [x, y]
#
#         # Compute log posteriors of current and proposed position
#         cur_posterior = posterior_func(current_position)
#         prop_posterior = posterior_func(X_n)
#
#         # Acceptance probability
#         A = 1
#         if cur_posterior == 0:
#             current_position = X_n
#             samples.append(list(current_position))
#             continue
#         if prop_posterior / cur_posterior < 1:
#             A = prop_posterior / cur_posterior
#
#         # Possibly update position
#         if A >= 1:
#             current_position = X_n
#         else:
#             u = np.random.uniform(0, 1)
#             if A >= u:
#                 current_position = X_n
#
#         # Extend the samples array vertically for each iteration
#         samples.append(list(current_position))
#     return np.array(samples)
#
# samples = sampler(im_posterior_func, 2, imwidth, imheight, no_of_samples=num, start_position=None)  # position samples
# xs, ys = samples.T
#
#
# plt.hist2d(ys, -xs, bins=[np.arange(0, imheight, 1), np.arange(-imwidth, 0, 1)], cmap=plt.cm.binary)
# plt.show()
#
#














###############################################################################3
#
#
#
#
#






#matplotlib inline



        # plt.show()



# levels = np.linspace(0, 100, 100)
# fig, ax = plt.subplots()
# contour_plot = ax.contourf(xx, yy, U, 100, cmap='gray_r', origin='lower', levels=levels)
# plt.colorbar(contour_plot)
# plt.xlabel('Xupt')
# plt.ylabel('Youcans')
# plt.title('Temperature distribution of the plate')
#
# # Function to update the animation at each frame
# def update(frame):
#     t = frame * dt  # Current time
#     xt, yt = x0 + vx * t, y0 + vy * t  # Updated position of the heat source
#     Qv = qv * np.exp(-((xx - xt) ** 2 + (yy - yt) ** 2))  # Updated heat source equation
#     U_new = U + rx * np.dot(U, A) + ry * np.dot(B, U) + Qv * dt  # Update temperature distribution
#     contour_plot.set_array(U_new[:-1, :-1].ravel())  # Update the data for the contour plot
#     return contour_plot,
#
# # Create the animation
# ani = FuncAnimation(fig, update, frames=tNodes+1, interval=50, blit=True)
#
# plt.show()