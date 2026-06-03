import sys

sys.path.insert(0, 'C:/Users/76598/Zotero/storage/5RBCJZYA/PINNs-master/Utilities')
import torch
import numpy as np
from scipy.interpolate import griddata
from pyDOE import lhs
import time
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import scipy.io
np.random.seed(1234)
# tf.random.set_seed(1234)
torch.manual_seed(1234)

class PhysicsInformedNN:
    # Initialize the class
    def __init__(self, x0, u0, v0, tb, X_f, layers, lb, ub):

        X0 = np.concatenate((x0, 0 * x0), 1)  # (x0, 0)
        X_lb = np.concatenate((0 * tb + lb[0], tb), 1)  # (lb[0], tb)
        X_ub = np.concatenate((0 * tb + ub[0], tb), 1)  # (ub[0], tb)

        self.lb = lb
        self.ub = ub

        self.x0 = X0[:, 0:1]
        self.t0 = X0[:, 1:2]

        self.x_lb = X_lb[:, 0:1]
        self.t_lb = X_lb[:, 1:2]

        self.x_ub = X_ub[:, 0:1]
        self.t_ub = X_ub[:, 1:2]

        self.x_f = X_f[:, 0:1]
        self.t_f = X_f[:, 1:2]

        self.u0 = u0
        self.v0 = v0

        # Initialize NNs
        self.layers = layers
        self.weights, self.biases = self.initialize_NN(layers)

        #
        self.x0_tf = torch.tensor(self.x0, dtype=torch.float32, requires_grad=False)
        self.t0_tf = torch.tensor(self.t0, dtype=torch.float32, requires_grad=False)

        self.u0_tf = torch.tensor(self.u0, dtype=torch.float32, requires_grad=False)
        self.v0_tf = torch.tensor(self.v0, dtype=torch.float32, requires_grad=False)

        self.x_lb_tf = torch.tensor(self.x_lb, dtype=torch.float32, requires_grad=False)
        self.t_lb_tf = torch.tensor(self.t_lb, dtype=torch.float32, requires_grad=False)

        self.x_ub_tf = torch.tensor(self.x_ub, dtype=torch.float32, requires_grad=False)
        self.t_ub_tf = torch.tensor(self.t_ub, dtype=torch.float32, requires_grad=False)

        self.x_f_tf = torch.tensor(self.x_f, dtype=torch.float32, requires_grad=False)
        self.t_f_tf = torch.tensor(self.t_f, dtype=torch.float32, requires_grad=False)

        # tf Graphs
        # self.u0_pred, self.v0_pred, _, _ = self.net_uv(self.x0_tf, self.t0_tf)
        # self.u_lb_pred, self.v_lb_pred, self.u_x_lb_pred, self.v_x_lb_pred = self.net_uv(self.x_lb_tf, self.t_lb_tf)
        # self.u_ub_pred, self.v_ub_pred, self.u_x_ub_pred, self.v_x_ub_pred = self.net_uv(self.x_ub_tf, self.t_ub_tf)
        # self.f_u_pred, self.f_v_pred = self.net_f_uv(self.x_f_tf, self.t_f_tf)

        # Loss
        self.optimizer =torch.optim.LBFGS(self.model.parameters(), max_iter=50000, max_eval=50000,
                                     history_size=50, line_search_fn='strong_wolfe')
        self.optimizer_Adam = torch.optim.Adam(self.model.parameters())

    def train1(self, nIter):
        for it in range(nIter):
            self.optimizer.zero_grad()
            self.loss = self.calculate_loss()
            self.loss.backward()
            self.optimizer.step()

    def calculate_loss(self):
        u0_pred, v0_pred, _, _ = self.net_uv(self.x0_tf, self.t0_tf)
        u_lb_pred, v_lb_pred, u_x_lb_pred, v_x_lb_pred = self.net_uv(self.x_lb_tf, self.t_lb_tf)
        u_ub_pred, v_ub_pred, u_x_ub_pred, v_x_ub_pred = self.net_uv(self.x_ub_tf, self.t_ub_tf)
        # ... (other calculations)
        loss = (torch.mean((self.u0_tf - u0_pred) ** 2) +
                torch.mean((self.v0_tf - v0_pred) ** 2) +
                torch.mean((u_lb_pred - u_ub_pred) ** 2) +
                torch.mean((v_lb_pred - v_ub_pred) ** 2) +
                torch.mean((u_x_lb_pred - u_x_ub_pred) ** 2) +
                torch.mean((v_x_lb_pred - v_x_ub_pred) ** 2) +
                torch.mean(f_u_pred ** 2) + torch.mean(f_v_pred ** 2))
        return loss

    def initialize_NN(self, layers):
        weights = []
        biases = []
        num_layers = len(layers)
        for l in range(0, num_layers - 1):
            W = self.xavier_init(size=[layers[l], layers[l + 1]])
            b = torch.nn.Parameter(torch.zeros(1, layers[l + 1], dtype=torch.float32))
            weights.append(W)
            biases.append(b)
        return weights, biases

    def xavier_init(self, size):
        tensor = torch.empty(size)
        in_dim = size[0]
        out_dim = size[1]
        xavier_stddev = np.sqrt(2 / (in_dim + out_dim))
        torch.nn.init.normal_(tensor, mean=0, std=xavier_stddev)
        return tensor

    def neural_net(self, X, weights, biases):
        num_layers = len(weights) + 1

        H = 2.0 * (X - self.lb.astype(np.float32)) / (self.ub.astype(np.float32) - self.lb.astype(np.float32)) - 1.0
        for l in range(0, num_layers - 2):
            W = weights[l]
            b = biases[l]
            H = torch.tanh(torch.matmul(H, W) + b.to(torch.float32))
        W = weights[-1]
        b = biases[-1]
        Y = torch.matmul(H, W) + b.to(torch.float32)
        return Y

    def net_uv(self, x, t):
        X = torch.cat((x, t), dim=1)

        uv = self.neural_net(X, self.weights, self.biases)
        u = uv[:, 0:1]
        v = uv[:, 1:2]

        u_x = torch.autograd.grad(u, x, torch.ones_like(u), create_graph=True)[0]
        v_x = torch.autograd.grad(v, x, torch.ones_like(v), create_graph=True)[0]

        return u, v, u_x, v_x

    def net_f_uv(self, x, t):
        u, v, u_x, v_x = self.net_uv(x, t)

        u_t = torch.autograd.grad(u, t, create_graph=True)[0]
        u_xx = torch.autograd.grad(u_x, x, create_graph=True)[0]

        v_t = torch.autograd.grad(v, t, create_graph=True)[0]
        v_xx = torch.autograd.grad(v_x, x, create_graph=True)[0]

        f_u = u_t + 0.5 * v_xx + (u ** 2 + v ** 2) * v
        f_v = v_t - 0.5 * u_xx - (u ** 2 + v ** 2) * u

        return f_u, f_v


    def callback(self, loss):
       print('Loss:', loss)



    def train(self, nIter):
        start_time = time.time()
        for it in range(nIter):
            self.optimizer_Adam.zero_grad()

            loss_value = self.loss_function(inputs)  # Update this according to your loss function
            loss_value.backward()

            self.optimizer_Adam.step()

        # Print
            if it % 10 == 0:
               elapsed = time.time() - start_time
               print('It: %d, Loss: %.3e, Time: %.2f' % (it, loss_value.item(), elapsed))
               start_time = time.time()


    def predict(self, X_star):
        with torch.no_grad():
            x0_tensor = torch.Tensor(X_star[:, 0:1])
            t0_tensor = torch.Tensor(X_star[:, 1:2])

            u_star = self.u0_pred(x0_tensor, t0_tensor).numpy()
            v_star = self.v0_pred(x0_tensor, t0_tensor).numpy()

            x_f_tensor = torch.Tensor(X_star[:, 0:1])
            t_f_tensor = torch.Tensor(X_star[:, 1:2])

            f_u_star = self.f_u_pred(x_f_tensor, t_f_tensor).numpy()
            f_v_star = self.f_v_pred(x_f_tensor, t_f_tensor).numpy()

        return u_star, v_star, f_u_star, f_v_star









if __name__ == "__main__":
    noise = 0.0

    # Doman bounds
    lb = np.array([-5.0, 0.0])
    ub = np.array([5.0, np.pi / 2])

    N0 = 50
    N_b = 50
    N_f = 20000
    layers = [2, 100, 100, 100, 100, 2]

    data = scipy.io.loadmat('C:/vpn/NLS.mat')

    t = data['tt'].flatten()[:, None]
    x = data['x'].flatten()[:, None]
    Exact = data['uu']
    Exact_u = np.real(Exact)
    Exact_v = np.imag(Exact)
    Exact_h = np.sqrt(Exact_u ** 2 + Exact_v ** 2)

    X, T = np.meshgrid(x, t)

    X_star = np.hstack((X.flatten()[:, None], T.flatten()[:, None]))
    u_star = Exact_u.T.flatten()[:, None]
    v_star = Exact_v.T.flatten()[:, None]
    h_star = Exact_h.T.flatten()[:, None]

    ###########################

    idx_x = np.random.choice(x.shape[0], N0, replace=False)
    x0 = x[idx_x, :]
    u0 = Exact_u[idx_x, 0:1]
    v0 = Exact_v[idx_x, 0:1]

    idx_t = np.random.choice(t.shape[0], N_b, replace=False)
    tb = t[idx_t, :]

    X_f = lb + (ub - lb) * lhs(2, N_f)

    model = PhysicsInformedNN(x0, u0, v0, tb, X_f, layers, lb, ub)

#     start_time = time.time()
#     model.train(50000)
#     elapsed = time.time() - start_time
#     print('Training time: %.4f' % (elapsed))
#
# # 其他部分保持不变
#     u_pred, v_pred, f_u_pred, f_v_pred = model.predict(X_star)
#     h_pred = np.sqrt(u_pred ** 2 + v_pred ** 2)
#
#     error_u = np.linalg.norm(u_star - u_pred, 2) / np.linalg.norm(u_star, 2)
#     error_v = np.linalg.norm(v_star - v_pred, 2) / np.linalg.norm(v_star, 2)
#     error_h = np.linalg.norm(h_star - h_pred, 2) / np.linalg.norm(h_star, 2)
#     print('Error u: %e' % (error_u))
#     print('Error v: %e' % (error_v))
#     print('Error h: %e' % (error_h))
#
#     U_pred = griddata(X_star, u_pred.flatten(), (X, T), method='cubic')
#     V_pred = griddata(X_star, v_pred.flatten(), (X, T), method='cubic')
#     H_pred = griddata(X_star, h_pred.flatten(), (X, T), method='cubic')
#
#     FU_pred = griddata(X_star, f_u_pred.flatten(), (X, T), method='cubic')
#     FV_pred = griddata(X_star, f_v_pred.flatten(), (X, T), method='cubic')
#
#     ######################################################################
#     ############################# Plotting ###############################
#     ######################################################################
#
#     X0 = np.concatenate((x0, 0 * x0), 1)  # (x0, 0)
#     X_lb = np.concatenate((0 * tb + lb[0], tb), 1)  # (lb[0], tb)
#     X_ub = np.concatenate((0 * tb + ub[0], tb), 1)  # (ub[0], tb)
#     X_u_train = np.vstack([X0, X_lb, X_ub])
#
#     fig, ax = newfig(1.0, 0.9)
#     ax.axis('off')
#
#     ####### Row 0: h(t,x) ##################
#     gs0 = gridspec.GridSpec(1, 2)
#     gs0.update(top=1 - 0.06, bottom=1 - 1 / 3, left=0.15, right=0.85, wspace=0)
#     ax = plt.subplot(gs0[:, :])
#
#     h = ax.imshow(H_pred.T, interpolation='nearest', cmap='YlGnBu',
#                   extent=[lb[1], ub[1], lb[0], ub[0]],
#                   origin='lower', aspect='auto')
#     divider = make_axes_locatable(ax)
#     cax = divider.append_axes("right", size="5%", pad=0.05)
#     fig.colorbar(h, cax=cax)
#
#     ax.plot(X_u_train[:, 1], X_u_train[:, 0], 'kx', label='Data (%d points)' % (X_u_train.shape[0]), markersize=4,
#             clip_on=False)
#
#     line = np.linspace(x.min(), x.max(), 2)[:, None]
#     ax.plot(t[75] * np.ones((2, 1)), line, 'k--', linewidth=1)
#     ax.plot(t[100] * np.ones((2, 1)), line, 'k--', linewidth=1)
#     ax.plot(t[125] * np.ones((2, 1)), line, 'k--', linewidth=1)
#
#     ax.set_xlabel('$t$')
#     ax.set_ylabel('$x$')
#     leg = ax.legend(frameon=False, loc='best')
#     #    plt.setp(leg.get_texts(), color='w')
#     ax.set_title('$|h(t,x)|$', fontsize=10)
#
#     ####### Row 1: h(t,x) slices ##################
#     gs1 = gridspec.GridSpec(1, 3)
#     gs1.update(top=1 - 1 / 3, bottom=0, left=0.1, right=0.9, wspace=0.5)
#
#     ax = plt.subplot(gs1[0, 0])
#     ax.plot(x, Exact_h[:, 75], 'b-', linewidth=2, label='Exact')
#     ax.plot(x, H_pred[75, :], 'r--', linewidth=2, label='Prediction')
#     ax.set_xlabel('$x$')
#     ax.set_ylabel('$|h(t,x)|$')
#     ax.set_title('$t = %.2f$' % (t[75]), fontsize=10)
#     ax.axis('square')
#     ax.set_xlim([-5.1, 5.1])
#     ax.set_ylim([-0.1, 5.1])
#
#     ax = plt.subplot(gs1[0, 1])
#     ax.plot(x, Exact_h[:, 100], 'b-', linewidth=2, label='Exact')
#     ax.plot(x, H_pred[100, :], 'r--', linewidth=2, label='Prediction')
#     ax.set_xlabel('$x$')
#     ax.set_ylabel('$|h(t,x)|$')
#     ax.axis('square')
#     ax.set_xlim([-5.1, 5.1])
#     ax.set_ylim([-0.1, 5.1])
#     ax.set_title('$t = %.2f$' % (t[100]), fontsize=10)
#     ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.8), ncol=5, frameon=False)
#
#     ax = plt.subplot(gs1[0, 2])
#     ax.plot(x, Exact_h[:, 125], 'b-', linewidth=2, label='Exact')
#     ax.plot(x, H_pred[125, :], 'r--', linewidth=2, label='Prediction')
#     ax.set_xlabel('$x$')
#     ax.set_ylabel('$|h(t,x)|$')
#     ax.axis('square')
#     ax.set_xlim([-5.1, 5.1])
#     ax.set_ylim([-0.1, 5.1])
#     ax.set_title('$t = %.2f$' % (t[125]), fontsize=10)