for it = 1:N_t-1
    % 计算空间导数（内部点）
    for iz = 2:N_z-1
        for i = 1:N
            % 获取当前状态（行向量）
            w_current = squeeze(w(i,:,it,iz));     % 1×2
            s_current = squeeze(s(i,:,it,iz));     % 1×2
            
            % 计算二阶空间导数（中心差分）
            w_forward = squeeze(w(i,:,it,iz+1));   % 1×2
            w_backward = squeeze(w(i,:,it,iz-1));  % 1×2
            
            s_forward = squeeze(s(i,:,it,iz+1));   % 1×2
            s_backward = squeeze(s(i,:,it,iz-1));  % 1×2
            
            d2w = (w_forward - 2*w_current + w_backward)' / (z_sample^2);  % 2×1
            d2s = (s_forward - 2*s_current + s_backward)' / (z_sample^2);  % 2×1
            
            % 添加边界力项
            boundary_force = zeros(n,1);
            if iz == N_z-1  % 右边界附近点
                boundary_force = u(i,:,it)' / z_sample;  % 2×1
            end
            
            % 修正耦合项计算 - 确保是列向量
            w_matrix = squeeze(w(:,:,it,iz));  % N×2
            s_matrix = squeeze(s(:,:,it,iz));  % N×2
            
            % 确保耦合项是列向量
            coupling_term = (c * G(i,:) * w_matrix * Gamma')';  % 2×1
            coupling_term1 = (c * G(i,:) * s_matrix * Gamma')'; % 2×1
            
            % 确保所有项都是列向量
            f = Theta * d2w - A * w_current' + B * tanh(w_current') + coupling_term + boundary_force;  % 2×1
            f1 = Theta * d2s - A * s_current' + B * tanh(s_current') + coupling_term1;  % 2×1
                  
%             
            % 更新状态
            for dim = 1:n
                w(i,dim,it+1,iz) = w_current(dim) + t_sample * f(dim);
                s(i,dim,it+1,iz) = s_current(dim) + t_sample * f1(dim);
            end
        end
    end
    
    % 处理边界条件
    for i = 1:N
        % 左边界：零梯度
        w(i,:,it+1,1) = w(i,:,it+1,2);
        s(i,:,it+1,1) = s(i,:,it+1,2);
        
        % 右边界：控制梯度
%         w(i,:,it+1,N_z) = w(i,:,it+1,N_z-1) + u(i,:,it) * z_sample;
        w(i,:,it+1,N_z) = w(i,:,it+1,N_z-1);
        s(i,:,it+1,N_z) = s(i,:,it+1,N_z-1);
    end
    
    % 计算误差
    for i = 1:N
        for iz = 1:N_z
            e(i,:,it,iz) = w(i,:,it,iz) - s(i,:,it,iz);
        end
    end
    % 初始化
if it == 1:round(1/2*N_t)
if it > chufa(m) && it < xiuxi(m)
    % 从触发到休息开始：施加控制
    for i = 1:N
        control_sum = zeros(1,2);
        for iz = 2:N_z-1
            control_sum = control_sum - z_sample * D(i,i) * e(i,:,it,iz);
        end
        u(i,:,it+1) = control_sum;
    end
    fprintf('时间 %d: 控制中 (触发%d → 休息%d)\n', it, chufa(m), xiuxi(m));
    
elseif it >= xiuxi(m)
    % 休息期间：控制为0
    u(i,:,it+1) = zeros(1,2);
    fprintf('时间 %d: 休息中 (控制为0)\n', it);
    
    current_integral = L_vals(it);
    trigger_integral = W_vals(chufa(m));
    threshold = exp(-a_1) * trigger_integral;
    
    % 事件触发检查
    if current_integral >= threshold 
        % 新的事件触发
        chufa(m+1) = it; 
        
        if it== xiuxi(m)
         xiuxi(m+1)=it + 2*(xiuxi(m)-chufa(m));
        else 
         xiuxi(m+1)=it + 2/3*(xiuxi(m)-chufa(m)); 
        end
        W_vals(chufa(m+1)) = current_integral;
        m = m + 1;
    end
    
    
% if current_integral >= threshold 
%     chufa(m+1) = it; 
%     
%     % 自适应休息时间：触发比率越高，休息时间越长
%     trigger_ratio = current_integral / threshold;
%     base_rest = 100;  % 基础休息时间
%     
%     if trigger_ratio < 1.1
%         rest_duration = base_rest;  % 轻微超过阈值，短休息
%     elseif trigger_ratio < 1.5
%         rest_duration = 2 * base_rest;  % 中等超过，中等休息
%     else
%         rest_duration = 3 * base_rest;  % 大幅超过，长休息
%     end
%     
%     xiuxi(m+1) = it + rest_duration;
%     
%     fprintf('触发比率: %.2f, 设置休息时间: %d\n', trigger_ratio, rest_duration);
% end
% 
% end
%     if m > 1
%     if chufa(m) >= xiuxi(m)
%         error('时间顺序错误: 触发时刻 %d 应该在休息时刻 %d 之前', chufa(m), xiuxi(m));
%     end
%     if xiuxi(m) >= chufa(m+1)
%         error('时间顺序错误: 休息时刻 %d 应该在下一个触发时刻 %d 之前', xiuxi(m), chufa(m+1));
%     end
% end
%     s_sum =0;
%     % 控制逻辑
%      for iz = 1:N_z
%         current_matrix = e(:, :, it, iz);       
%         frobenius_norm_squared = sum(current_matrix(:).^2);       
%         s_sum = s_sum + K(iz) * frobenius_norm_squared;
%     end
%     L_vals(it) = s_sum;
%     W_vals(1) =L_vals(1);
%     
%     
%     
%         for i = 1:N
%             control_sum = zeros(1,2);
%             for iz = 2:N_z-1
%                 control_sum = control_sum - z_sample * D(i,i) * e(i,:,it,iz);
%             end
%             u(i,:,it+1) = control_sum;
%         end
    
%     if it > chufa(m) && it < xiuxi(m)
%     % 正常工作期间的控制律
%      for i = 1:N
%         control_sum = zeros(1,2);
%         for iz = 2:N_z-1
%             control_sum = control_sum - z_sample * D(i,i) * e(i,:,it,iz);
%         end
%         u(i,:,it+1) = control_sum;
%      end
%     
%     elseif it >= xiuxi(m)
%     % 休息期间，控制输入为零
%     u(i,:,it+1) = zeros(1,2);
%     
%     % 计算当前时刻的积分值 ∫?? ζ(ρ,t)? ζ(ρ,t) dρ
%     % 这里假设 L_vals(it) 已经包含了这个积分值
%     current_integral = L_vals(it);
%     
%     % 计算触发时刻的积分值 ∫?? ζ(ρ,t_m)? ζ(ρ,t_m) dρ
%     % 这里假设 W_vals 存储了各个触发时刻的积分值
%     trigger_integral = W_vals(chufa(m));
%    % 在事件触发部分添加调试输出
%    
%    monitor_interval = 10;  % 每10个时间步输出一次状态
% 
% if mod(it, monitor_interval) == 0
%     fprintf('监控 - 时间 %d: m=%d, 当前在[%d, %d]区间\n', ...
%             it, m, chufa(m), xiuxi(m));
%     if it >= xiuxi(m)
%         fprintf('监控 - 当前状态: 休息中\n');
%     else
%         fprintf('监控 - 当前状态: 工作中\n');
%     end
% end
%    
%    
%    
%    
% % 在循环开始前添加调试记录
% debug_info = struct();
% trigger_count = 0;
% 
% if it > chufa(m) && it < xiuxi(m)
%     % 正常工作期间
%     for i = 1:N
%         control_sum = zeros(1,2);
%         for iz = 2:N_z-1
%             control_sum = control_sum - z_sample * D(i,i) * e(i,:,it,iz);
%         end
%         u(i,:,it+1) = control_sum;
%     end
%     
%     % 记录正常工作期间的信息
%     fprintf('时间 %d: 正常工作 (在触发%d和休息%d之间)\n', it, chufa(m), xiuxi(m));
%     
% elseif it >= xiuxi(m)
%     % 休息期间
%     u(i,:,it+1) = zeros(1,2);
%     
%     current_integral = L_vals(it);
%     trigger_integral = W_vals(chufa(m));
%     threshold = exp(-a) * trigger_integral;
%     
%     fprintf('时间 %d: 休息中 | 当前积分: %.6f | 阈值: %.6f | 比率: %.4f\n', ...
%             it, current_integral, threshold, current_integral/threshold);
%     
%     % 详细的事件触发检查
%     if current_integral >= threshold 
%         trigger_count = trigger_count + 1;
%         
%         fprintf('=== 事件触发 #%d ===\n', trigger_count);
%         fprintf('触发时刻: t%d = %d\n', m+1, it);
%         fprintf('前次触发: t%d = %d\n', m, chufa(m));
%         fprintf('前次休息: θ%d = %d\n', m, xiuxi(m));
%         fprintf('当前积分: %.6f >= 阈值: %.6f\n', current_integral, threshold);
%         
%         chufa(m+1) = it; 
%         
%         % 更新休息时间
%         if it == xiuxi(m)
%             rest_duration = c1 * (xiuxi(m) - chufa(m));
%             xiuxi(m+1) = it + rest_duration;
%             fprintf('情况1: 正好休息结束时触发，新休息期: %d → %d (长度: %d)\n', ...
%                     it, xiuxi(m+1), rest_duration);
%         else
%             rest_duration = (xiuxi(m) - chufa(m));
%             xiuxi(m+1) = it + rest_duration;
%             fprintf('情况2: 休息期间触发，新休息期: %d → %d (长度: %d)\n', ...
%                     it, xiuxi(m+1), rest_duration);
%         end
%         
%         W_vals(it) = current_integral;
%         m = m + 1;
%         
%         % 记录详细的调试信息
%         debug_info(trigger_count).time = it;
%         debug_info(trigger_count).current = current_integral;
%         debug_info(trigger_count).threshold = threshold;
%         debug_info(trigger_count).ratio = current_integral / threshold;
%         debug_info(trigger_count).rest_duration = rest_duration;
%         debug_info(trigger_count).prev_trigger = chufa(m-1);
%         debug_info(trigger_count).prev_rest = xiuxi(m-1);
%         
%         fprintf('新的触发序列: t=[%s], θ=[%s]\n', ...
%                 num2str(chufa(1:m)), num2str(xiuxi(1:m)));
%         fprintf('========================\n');
%         
%     else
%         fprintf('时间 %d: 未达到触发条件 (需要: %.6f)\n', it, threshold - current_integral);
%     end  
% end

%    if current_integral >= exp(-a) * trigger_integral 
%     chufa(m+1) = it; 
%     
%     % 保存调试信息
%     debug_info(m).time = it;
%     debug_info(m).current = current_integral;
%     debug_info(m).threshold = exp(-a) * trigger_integral;
%     debug_info(m).ratio = current_integral / (exp(-a) * trigger_integral);
%     
%     % 更新休息时间 - 修正后的逻辑
%      if it == xiuxi(m)
%         % 触发时刻正好是休息结束时刻，给予更长的休息
%         rest_duration = c1 * (xiuxi(m) - chufa(m));
%         xiuxi(m+1) = it + rest_duration;
%         fprintf('情况1: 休息期延长至 %d\n', rest_duration);
%      else
%         % 在休息期间触发，保持相同的休息长度
%         rest_duration = (xiuxi(m) - chufa(m));
%         xiuxi(m+1) = it + rest_duration;
%         fprintf('情况2: 休息期保持 %d\n', rest_duration);
%      end
%     
%     W_vals(it) = current_integral;
%     m = m + 1;
%     
%     % 添加最小休息时间约束
%     min_rest_time = 500;  % 最小休息时间
%      if (xiuxi(m) - chufa(m)) < min_rest_time
%         xiuxi(m) = chufa(m) + min_rest_time;
%         fprintf('调整: 最小休息时间设置为 %d\n', min_rest_time);
%      end
%     end
 end
else
  if it > chufa(m) && it < xiuxi(m)
    % 从触发到休息开始：施加控制
    for i = 1:N
        control_sum = zeros(1,2);
        for iz = 2:N_z-1
            control_sum = control_sum - z_sample * D(i,i) * e(i,:,it,iz);
        end
        u(i,:,it+1) = control_sum;
    end
    fprintf('时间 %d: 控制中 (触发%d → 休息%d)\n', it, chufa(m), xiuxi(m));
    
elseif it >= xiuxi(m)
    % 休息期间：控制为0
    u(i,:,it+1) = zeros(1,2);
    fprintf('时间 %d: 休息中 (控制为0)\n', it);
    
    current_integral = L_vals(it);
    trigger_integral = W_vals(chufa(m));
    threshold = exp(-a_2) * trigger_integral;
    
    % 事件触发检查
    if current_integral >= threshold 
        % 新的事件触发
        chufa(m+1) = it; 
        
        if it== xiuxi(m)
         xiuxi(m+1)=it + 2*(xiuxi(m)-chufa(m));
        else 
         xiuxi(m+1)=it + 2/3*(xiuxi(m)-chufa(m)); 
        end
        W_vals(chufa(m+1)) = current_integral;
        m = m + 1;
    end
  end  
    
end



end 
