% 参数设置
N = 4;          % 智能体数量
n = 2;          % 每个智能体的状态维度
L = 1;          % 空间域长度
N_z = 6;        % 空间离散点数
N_t = 100000;     % 时间步数（减少以便调试）
z_sample = L/(N_z-1);  % 空间步长
t_sample = 0.001;       % 时间步长（增大以提高计算速度）

% 系统参数
Theta = diag([1, 1]);
A = diag([1.5, 1.5]);
B = [2, 0; 0, 2];
Gamma = [0.1, 0; 0, 0.1];
c = 1;
a = 0.1;
d = [(pi^2)/2, (pi^2)/2, (pi^2)/2, (pi^2)/2];  
D = diag(d);
theta_m = 200;

% 外耦合矩阵
G = -[2, 0, -1, -1;
      0, 3, -1, -2;
      -1, -1, 2, 0;
      -1, -2, 0, 3];

% 初始化
w = zeros(N, n, N_t, N_z);
u = zeros(N, n, N_t);
s = zeros(N, n, N_t, N_z);
e = zeros(N, n, N_t, N_z);

% 初始条件（保持不变）
for i = 1:N
    for iz = 1:N_z
        z_pos = (iz-1)*z_sample;
        if i == 1
            w(i,1,1,iz) = 0.4*cos(2*pi*z_pos) + 0.1;
            w(i,2,1,iz) = 0.6*sin(3*pi*z_pos + pi/2) + 0.5;
            s(i,1,1,iz) = -0.1*sin(pi*z_pos + pi/2);
            s(i,2,1,iz) = -0.1*cos(pi*z_pos);
        elseif i == 2
            w(i,1,1,iz) = 0.3*cos(2*pi*z_pos);
            w(i,2,1,iz) = 0.5*cos(0.5*pi*z_pos + pi/2);
            s(i,1,1,iz) = -0.2*cos(pi*z_pos + pi/2);
            s(i,2,1,iz) = 0.1*cos(pi*z_pos);
        elseif i == 3
            w(i,1,1,iz) = 0.5*cos(0.25*pi*z_pos + 3*pi/4);
            w(i,2,1,iz) = 0.2*cos(2*pi*z_pos);
            s(i,1,1,iz) = -0.2*cos(pi*z_pos);
            s(i,2,1,iz) = 0.5*sin(pi*z_pos);
        else
            w(i,1,1,iz) = 0.8*sin(0.5*pi*z_pos + pi/2);
            w(i,2,1,iz) = 0.2*cos(-2*pi*z_pos);
            s(i,1,1,iz) = 0.5*cos(pi*z_pos);
            s(i,2,1,iz) = 0.1*cos(pi*z_pos) + 0.05;
        end
    end
end

% 积分权重
Delta_rho = 1/(N_z-1);
K = Delta_rho * ones(1, N_z);
K(1) = Delta_rho/2;
K(end) = Delta_rho/2;

% 初始化触发时间数组
trigger_times = [1];
m = 1;

% 初始化 L 和 W 数组
L_vals = zeros(N_t, 1);
W_vals = zeros(N_t, 1);

% 主循环
for it = 1:N_t-1
    % 计算空间导数（包括边界点）
    for iz = 1:N_z
        for i = 1:N
            if iz == 1 || iz == N_z
                % 边界条件：使用单边差分
                if iz == 1
                    w_forward = squeeze(w(i,:,it,iz+1));
                    w_current = squeeze(w(i,:,it,iz));
                    d2w = (w_forward - w_current)' / (z_sample^2);
                    
                    s_forward = squeeze(s(i,:,it,iz+1));
                    s_current = squeeze(s(i,:,it,iz));
                    d2s = (s_forward - s_current)' / (z_sample^2);
                else
                    w_backward = squeeze(w(i,:,it,iz-1));
                    w_current = squeeze(w(i,:,it,iz));
                    d2w = (w_current - w_backward)' / (z_sample^2);
                    
                    s_backward = squeeze(s(i,:,it,iz-1));
                    s_current = squeeze(s(i,:,it,iz));
                    d2s = (s_current - s_backward)' / (z_sample^2);
                end
            else
                % 内部点：使用中心差分
                w_current = squeeze(w(i,:,it,iz));
                w_forward = squeeze(w(i,:,it,iz+1));
                w_backward = squeeze(w(i,:,it,iz-1));
                d2w = (w_forward - 2*w_current + w_backward)' / (z_sample^2);
                
                s_current = squeeze(s(i,:,it,iz));
                s_forward = squeeze(s(i,:,it,iz+1));
                s_backward = squeeze(s(i,:,it,iz-1));
                d2s = (s_forward - 2*s_current + s_backward)' / (z_sample^2);
            end
            
            w_matrix = squeeze(w(:,:,it,iz));
            s_matrix = squeeze(s(:,:,it,iz));
            
            coupling_term = (c * G(i,:) * w_matrix * Gamma')';
            coupling_term1 = (c * G(i,:) * s_matrix * Gamma')';
            
            f = Theta * d2w - A * w_current' + B * tanh(w_current') + coupling_term;
            f1 = Theta * d2s - A * s_current' + B * tanh(s_current') + coupling_term1;
            
            for dim = 1:n
                w(i,dim,it+1,iz) = w_current(dim) + t_sample * f(dim);
                s(i,dim,it+1,iz) = s_current(dim) + t_sample * f1(dim);
            end
        end
    end
    
    % 计算误差
    for i = 1:N
        for iz = 1:N_z
            e(i,:,it,iz) = w(i,:,it,iz) - s(i,:,it,iz);
        end
    end
    
    % 计算积分 L(it) 和 W(t(m))
    s_sum = 0;
    s_sum1 = 0;
    for iz = 1:N_z
        current_matrix = e(:, :, it, iz);
        current_matrix1 = e(:, :, trigger_times(m), iz);
        
        frobenius_norm_squared = sum(current_matrix(:).^2);
        frobenius_norm_squared1 = sum(current_matrix1(:).^2);
        
        s_sum = s_sum + K(iz) * frobenius_norm_squared;
        s_sum1 = s_sum1 + K(iz) * frobenius_norm_squared1;
    end
    L_vals(it) = s_sum;
    W_vals(trigger_times(m)) = s_sum1;
    
    % 控制逻辑
    if it >= trigger_times(m) && it < theta_m
        for i = 1:N
            control_sum = zeros(1, n);
            for iz = 1:N_z
                control_sum = control_sum - K(iz) * D(i,i) * e(i,:,it,iz);
            end
            u(i,:,it+1) = control_sum;
        end
    else
        if L_vals(it) >= exp(-a) * W_vals(trigger_times(m))
            if m < length(trigger_times)
                m = m + 1;
            else
                trigger_times = [trigger_times, it];
                m = length(trigger_times);
            end
            
            % 更新控制输入
            for i = 1:N
                control_sum = zeros(1, n);
                for iz = 1:N_z
                    control_sum = control_sum - K(iz) * D(i,i) * e(i,:,it,iz);
                end
                u(i,:,it+1) = control_sum;
            end
            
            % 更新 theta_m
            if trigger_times(m) >= theta_m-2 && trigger_times(m) <= theta_m+2
                theta_m = 2*(theta_m - trigger_times(m-1)) + trigger_times(m);
            elseif trigger_times(m) > theta_m+2
                theta_m = (theta_m - trigger_times(m-1)) + trigger_times(m);
            end
        else
            u(:,:,it+1) = 0;
        end
    end
end
save('w.mat')
save('s.mat')