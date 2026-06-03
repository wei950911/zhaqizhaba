 
data1 = importdata('w.mat');  
data2 = importdata('s.mat'); 

% 查看结构体字段名
field_names = fieldnames(data2)
disp('结构体字段:');
disp(field_names);

% 查看第一个字段的数据类型和内容
if ~isempty(field_names)
    first_field = data2.(field_names{1});
    whos first_field
    disp(['第一个字段的数据类型: ', class(first_field)]);
end
  

newVar1 = data1.w * 1e16;       % 对y数据进行缩放
newVar2 = data2.s * 1e16;       % 对s数据进行缩放

rng(42);


save('modified1.mat', 'newVar1','-v7.3');
save('modified2.mat', 'newVar2','-v7.3');



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5查看数据缩放因子不匹配
disp(['newVar1 最小值: ', num2str(min(newVar1(:)))]);
disp(['newVar1 最大值: ', num2str(max(newVar1(:)))]);
disp(['newVar2 最小值: ', num2str(min(newVar2(:)))]);
disp(['newVar2 最大值: ', num2str(max(newVar2(:)))]);



% 计算总元素数量
numElements1 = numel(newVar1(:,:,2500:end,:));
numElements2 = numel(newVar2(:,:,2500:end,:));
sequence1 = zeros(numElements1, 1, 'double'); % 保持双精度进行数值操作
sequence2 = zeros(numElements2, 1, 'double');
idx = 1;
%
for k = 100000:size(newVar1,3)
    for l = 1:size(newVar1,4)
        for j = 1:size(newVar1,2)
            for i = 1:size(newVar1,1)
                sequence1(idx) = newVar1(i,j,k,l);
                 sequence2(idx) = newVar2(i,j,k,l);
                idx = idx + 1;
            end
        end
    end
end

% 输入数据验证



n = 262144; % 每个序列的目标长度
half_n = n/2; 


sequence1 = uint8(mod(floor(sequence1), 256));
sequence2 = uint8(mod(floor(sequence2), 256));






total_length = size(sequence1,1);
mid_index = floor(total_length/2);
start_idx = mid_index - half_n + 1;
end_idx = mid_index + half_n;


R2_sequence = sequence1(1:n); 
R3_sequence = sequence2(1:n);
G2_sequence = sequence1(end-n+1:end); 
G3_sequence = sequence2(end-n+1:end); 
B2_sequence = sequence1(start_idx:end_idx);
B3_sequence = sequence2(start_idx:end_idx);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%检查密钥流的熵和分布：
prob = histcounts(R2_sequence, 0:255) / numel(R2_sequence);
prob_nonzero = prob(prob > 0);
entropy = -sum(prob_nonzero .* log2(prob_nonzero));
disp(['R2_sequence 熵值: ', num2str(entropy)]); 
disp('R2_sequence 前10个值:');
disp(R2_sequence(1:10)');
% 读取原图
 image = imread('C:\\Users\\76598\\Desktop\\just for fun\\image\\mandril_color.tif');
% image = imread('C:\\Users\\76598\\Desktop\\just for fun\\pythonProject\\lena_color_512.tif');
% 提取各通道数据
[R1_sequence, G1_sequence, B1_sequence] = deal(reshape(image(:,:,1), [], 1), ...
    reshape(image(:,:,2), [], 1), reshape(image(:,:,3), [], 1));
% 加密过程
R_xor = bitxor(R1_sequence, R2_sequence);
G_xor = bitxor(G1_sequence, G2_sequence);
B_xor = bitxor(B1_sequence, B2_sequence);

K = zeros(262144, 3, 'uint8');

for j = 1:262144
    if j == 1
        K(j, :) = [R_xor(j), G_xor(j), B_xor(j)];
    else
        K(j, 1) = bitxor(K(j-1, 1), R_xor(j));
        K(j, 2) = bitxor(K(j-1, 2), G_xor(j));
        K(j, 3) = bitxor(K(j-1, 3), B_xor(j));
    end
end

% 生成加密图像
matrix_R = reshape(K(:,1), 512, 512);
matrix_G = reshape(K(:,2), 512, 512);
matrix_B = reshape(K(:,3), 512, 512);
RGB = cat(3, matrix_R, matrix_G, matrix_B);
R_xor_recovered(1) = K(1, 1);
G_xor_recovered(1) = K(1, 2);
B_xor_recovered(1) = K(1, 3);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%解密图片


[R_xor_recovered, G_xor_recovered, B_xor_recovered] = deal(zeros(262144, 1, 'uint8'));


% for j = 2:262144
%     R_xor_recovered(j) = bitxor(K(j, 1), K(j-1, 1));
%     G_xor_recovered(j) = bitxor(K(j, 2), K(j-1, 2));
%     B_xor_recovered(j) = bitxor(K(j, 3), K(j-1, 3));
% end


% 
 for j =262124:-1:2
     
     
     R_xor_recovered(j) = bitxor(K(j, 1), K(j-1, 1));
    G_xor_recovered(j) = bitxor(K(j, 2), K(j-1, 2));     
     B_xor_recovered(j) = bitxor(K(j, 3), K(j-1, 3));
 end







% 恢复原始图像
R_original = bitxor(R_xor_recovered, R3_sequence);
G_original = bitxor(G_xor_recovered, G3_sequence);
B_original = bitxor(B_xor_recovered, B3_sequence);
decrypted_image = cat(3, reshape(R_original, 512, 512), reshape(G_original, 512, 512), reshape(B_original, 512, 512));
imwrite(decrypted_image, 'C:\\Users\\76598\\Desktop\\just for fun\\image\\decrypted_image.png');




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5数据分析


N=3000;


[h_r11, v_r11, d_r11, x11, y11] = RGB_correlation(image, N);
fprintf('原图通道相关系数：\n  水平: %.4f\n  垂直: %.4f\n  对角线: %.4f\n',...
        h_r11, v_r11, d_r11);
[h_r12, v_r12, d_r12, x12, y12] = RGB_correlation(image(:,:,1), N);
fprintf('原图R通道相关系数：\n  水平: %.4f\n  垂直: %.4f\n  对角线: %.4f\n',...
        h_r12, v_r12, d_r12);    
[h_r13, v_r13, d_r13, x13, y13] = RGB_correlation(image(:,:,2), N);
fprintf('原图G通道相关系数：\n  水平: %.4f\n  垂直: %.4f\n  对角线: %.4f\n',...
        h_r13, v_r13, d_r13);
 [h_r14, v_r14, d_r14, x14, y14] = RGB_correlation(image(:,:,3), N);
fprintf('原图B通道相关系数：\n  水平: %.4f\n  垂直: %.4f\n  对角线: %.4f\n',...
        h_r14, v_r14, d_r14);   
[h_r21, v_r21, d_r21, x21, y21] = RGB_correlation(RGB, N);  
    fprintf('加密通道相关系数：\n  水平: %.4f\n  垂直: %.4f\n  对角线: %.4f\n',...
        h_r21, v_r21, d_r21);
 [h_r22, v_r22, d_r22, x22, y22] = RGB_correlation(RGB(:,:,1), N);  
    fprintf('加密R通道相关系数：\n  水平: %.4f\n  垂直: %.4f\n  对角线: %.4f\n',...
        h_r22, v_r22, d_r22);  
    [h_r23, v_r23, d_r23, x23, y23] = RGB_correlation(RGB(:,:,2), N);  
    fprintf('加密G通道相关系数：\n  水平: %.4f\n  垂直: %.4f\n  对角线: %.4f\n',...
        h_r23, v_r23, d_r23);
    [h_r24, v_r24, d_r24, x24, y24] = RGB_correlation(RGB(:,:,3), N);  
    fprintf('加密B通道相关系数：\n  水平: %.4f\n  垂直: %.4f\n  对角线: %.4f\n',...
        h_r24, v_r24, d_r24);
 data = {
    1, h_r11, v_r11,  d_r11;
    2,  h_r12, v_r12, d_r12;
    3, h_r13, v_r13, d_r13;
    4, h_r14, v_r14, d_r14;
    5, h_r21, v_r21, d_r21;
    6, h_r22, v_r22, d_r22;
    7, h_r23, v_r23, d_r23;
    8, h_r24, v_r24, d_r24;
    
};

% 创建一个图形窗口
f = figure('Name', 'MATLAB表格示例');
t = uitable(f, 'Data', data, 'Position', [20 20 500 150]);
t.ColumnName = {'列1', '列2', '列3', '列4'};   
    
    
    

% 可视化
% 将合并后的数据分割为三个方向
n = N;
h_x1 = x11(1:n);
h_y1 = y11(1:n);

v_x1 = x11(n+1:2*n);
v_y1 = y11(n+1:2*n);

d_x1 = x11(2*n+1:3*n);
d_y1 = y11(2*n+1:3*n);




h_x2 = x21(1:n);
h_y2 = y21(1:n);

v_x2 = x21(n+1:2*n);
v_y2 = y21(n+1:2*n);

d_x2 = x21(2*n+1:3*n);
d_y2 = y21(2*n+1:3*n);

% h_x2 = x12(1:n);
% h_y2 = y12(1:n);
% 
% v_x2 = x12(n+1:2*n);
% v_y2 = y12(n+1:2*n);
% 
% d_x2 = x12(2*n+1:3*n);
% d_y2 = y12(2*n+1:3*n);
% 
% 
% 
% h_x3 = x13(1:n);
% h_y3 = y13(1:n);
% 
% v_x3 = x13(n+1:2*n);
% v_y3= y13(n+1:2*n);
% 
% d_x3 = x13(2*n+1:3*n);
% d_y3 = y13(2*n+1:3*n);








%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%原图的RGB三通道的相关性分析



% 创建画布
figure('Color','white', 'Position', [100,100,1200,400]);

% ------------------------------
% 水平方向相关性图
% ------------------------------
subplot(1,3,1);
scatter(h_x1, h_y1, 5, 'r', 'filled', 'MarkerEdgeAlpha',0.1);
title(['Horizontal Correlation: R = ', num2str(h_r11, '%.4f')]);
xlabel('Current Pixel Value');
ylabel('Right Pixel Value');
axis([0 255 0 255]);
grid on;

% ------------------------------
% 垂直方向相关性图
% ------------------------------
subplot(1,3,2);
scatter(v_x1, v_y1, 5, 'g', 'filled', 'MarkerEdgeAlpha',0.1);
title(['Vertical Correlation: R = ', num2str(v_r11, '%.4f')]);
xlabel('Current Pixel Value');
ylabel('Lower Pixel Value');
axis([0 255 0 255]);
grid on;

% ------------------------------
% 对角线方向相关性图
% ------------------------------
subplot(1,3,3);
scatter(d_x1, d_y1, 5, 'b', 'filled', 'MarkerEdgeAlpha',0.1);
title(['Diagonal Correlation: R = ', num2str(d_r11, '%.4f')]);
xlabel('Current Pixel Value');
ylabel('Lower-Right Pixel Value');
axis([0 255 0 255]);
grid on;



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5加密图片的相关性分析

figure('Color','white', 'Position', [100,100,1200,400]);
subplot(1,3,1);
scatter(h_x2, h_y2, 5, 'r', 'filled', 'MarkerEdgeAlpha',0.1);
title(['Horizontal Correlation: R = ', num2str(h_r21, '%.4f')]);
xlabel('Current Pixel Value');
ylabel('Right Pixel Value');
axis([0 255 0 255]);
grid on;

% ------------------------------
% 垂直方向相关性图
% ------------------------------
subplot(1,3,2);
scatter(v_x2, v_y2, 5, 'g', 'filled', 'MarkerEdgeAlpha',0.1);
title(['Vertical Correlation: R = ', num2str(v_r21, '%.4f')]);
xlabel('Current Pixel Value');
ylabel('Lower Pixel Value');
axis([0 255 0 255]);
grid on;

% ------------------------------
% 对角线方向相关性图
% ------------------------------
subplot(1,3,3);
scatter(d_x2, d_y2, 5, 'b', 'filled', 'MarkerEdgeAlpha',0.1);
title(['Diagonal Correlation: R = ', num2str(d_r21, '%.4f')]);
xlabel('Current Pixel Value');
ylabel('Lower-Right Pixel Value');
axis([0 255 0 255]);
grid on;




%%%%%%%%%%%%%%%%%%%%%%%%%%5求商
img1 = rgb2gray(image);
img2 = rgb2gray(RGB);

% 计算直方图
counts1 = imhist(img1);
counts2 = imhist(img2);
% 计算概率并移除零概率项
prob1 = counts1 / numel(img1);
prob_nonzero1 = prob1(prob1 > 0);
prob2 = counts2 / numel(img2);
prob_nonzero2 = prob2(prob2 > 0);
% 计算熵
image_entropy1 = -sum(prob_nonzero1 .* log2(prob_nonzero1));
image_entropy2 = -sum(prob_nonzero2 .* log2(prob_nonzero2));
% 显示结果
disp(['原图图像熵为: ', num2str(image_entropy1)]);
disp(['加密图像熵为: ', num2str(image_entropy2)]);



%%%%%%%%%%%%%%%%%%%%%%%%%三个图的对比
figure;

% 显示原图
subplot(1, 3, 1);
imshow(image);
title('Original Image');

% 显示加密图
subplot(1, 3, 2);
imshow(RGB);
title('Cipher Image');

% 显示解密图
subplot(1, 3, 3);
imshow(decrypted_image);
title('Decrypted Image');

% 调整窗口大小和布局
set(gcf, 'Position', [100, 100, 1500, 500]);  % 宽度1500，高度500






%%%%%%%%%%%%%%%%%%%%%%直方图

figure;
subplot(1,3,1);
% 处理原图
histogram(image(:)); % 计算直方图
title('Original Image Histogram');

subplot(1,3,2);
% 处理加密图，假设已经是灰度或需要转换
histogram(RGB(:)); % 计算直方图
title('Cipher Image Histogram');

subplot(1,3,3);
% 处理解密图
histogram(decrypted_image); % 计算直方图
title('Decrypted Image Histogram');




img1 = imread('C:\\Users\\76598\Desktop\\just for fun\\image\\mandril_color.tif');
img2 = imread('C:\\Users\\76598\\Desktop\\just for fun\\image\\decrypted_image.png');


a=calculatePSNR(img1,img2)
b=calculatePSNR(img1(:,:,1),img2(:,:,1))
c=calculatePSNR(img1(:,:,2),img2(:,:,2))
d=calculatePSNR(img1(:,:,3),img2(:,:,3))
UACI_R=pixal_different(img1(:,:,1),img2(:,:,1));
UACI_G=pixal_different(img1(:,:,2),img2(:,:,2));
UACI_B=pixal_different(img1(:,:,3),img2(:,:,3));

fprintf('UACI_R: %d\n',UACI_R );
fprintf('UACI_G: %d\n',UACI_G );
fprintf('UACI_B: %d\n',UACI_B );


diff2=image_num(img1(:,:,1),img2(:,:,1));
diff3=image_num(img1(:,:,2),img2(:,:,2));
diff4=image_num(img1(:,:,3),img2(:,:,3));
fprintf('NPCR_R: %d\n', diff2);
fprintf('NPCR_G: %d\n', diff3);
fprintf('NPCR_B: %d\n', diff4);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%哈希值

imagePath1 = 'C:\Users\76598\Desktop\just for fun\image\mandril_color.tif';
imagePath2 = 'C:\Users\76598\Desktop\just for fun\image\decrypted_image.png';

% 定义哈希算法列表
hashAlgorithms = {@aHash, @dHash, @pHash};
algorithmNames = {'平均哈希 (aHash)', '差异哈希 (dHash)', '感知哈希 (pHash)'};

fprintf('=== 图片哈希对比报告 ===\n\n');

for i = 1:length(hashAlgorithms)
    algo = hashAlgorithms{i};
    algoName = algorithmNames{i};
    
    try
        % 计算哈希值
        hash1 = algo(imagePath1);
        hash2 = algo(imagePath2);
        
        % 计算汉明距离
        distance = hammingDistance(hash1, hash2);
        
        % 获取阈值
        threshold = thresholdCheck(algo);
        
        % 输出结果
        fprintf('算法类型: %s\n', algoName);
        fprintf('图片1哈希: %s\n', hash1);
        fprintf('图片2哈希: %s\n', hash2);
        fprintf('汉明距离: %d\n', distance);
        fprintf('相似结论: %s\n\n', ternary(distance <= threshold, '相似', '不相似'));
        
    catch ME
        fprintf('【错误】%s 算法执行失败: %s\n\n', algoName, ME.message);
    end
end
















function [h_Rxy, v_Rxy, d_Rxy, x, y] = RGB_correlation(channel, N)
% RGB_CORRELATION 计算图像通道的相邻像素相关性
% 输入参数：
%   channel : 输入的单通道图像矩阵 (h x w, uint8格式)
%   N       : 随机采样的像素数量
% 输出参数：
%   h_Rxy   : 水平相邻像素相关系数
%   v_Rxy   : 垂直相邻像素相关系数
%   d_Rxy   : 对角线相邻像素相关系数
%   x       : 合并后的横坐标数据
%   y       : 合并后的纵坐标数据

%% 参数验证
% 验证通道尺寸
[h, w] = size(channel);
if h < 2 || w < 2
    error('图像尺寸至少为2x2像素');
end

% 验证采样数量
if N < 1 || N > (h-1)*(w-1)
    error('采样数量N应介于1和(h-1)*(w-1)之间');
end

%% 转换为双精度浮点型（关键修正）
channel = double(channel); % 转换整个通道数据
rng(42);
%% 生成随机采样坐标 (MATLAB使用1-based索引)
row = randi([1, h-1], 1, N); % [1, h-1]
col = randi([1, w-1], 1, N); % [1, w-1]

%% 收集相邻像素数据
x = zeros(1, N*3);
h_y = zeros(1, N);
v_y = zeros(1, N);
d_y = zeros(1, N);

for i = 1:N
    % 当前像素
    x(i) = channel(row(i), col(i));
    
    % 水平相邻像素 (右侧)
    h_y(i) = channel(row(i), col(i)+1);
    
    % 垂直相邻像素 (下方)
    v_y(i) = channel(row(i)+1, col(i));
    
    % 对角线相邻像素 (右下方)
    d_y(i) = channel(row(i)+1, col(i)+1);
end

% 合并三个方向数据
x = [x(1:N), x(1:N), x(1:N)]; 
y = [h_y, v_y, d_y];

%% 计算统计量 (全部使用双精度)
current_pixels = channel(sub2ind([h,w], row, col));

% 当前像素统计量
% ex = mean(current_pixels);
dx = var(current_pixels, 1); % 总体方差

% 水平方向计算
h_pixels = channel(sub2ind([h,w], row, col+1));
h_cov = cov(current_pixels, h_pixels, 1); 
h_Rxy = h_cov(1,2) / (sqrt(dx) * sqrt(var(h_pixels, 1)));

% 垂直方向计算
v_pixels = channel(sub2ind([h,w], row+1, col));
v_cov = cov(current_pixels, v_pixels, 1);
v_Rxy = v_cov(1,2) / (sqrt(dx) * sqrt(var(v_pixels, 1)));

% 对角线方向计算
d_pixels = channel(sub2ind([h,w], row+1, col+1));
d_cov = cov(current_pixels, d_pixels, 1);
d_Rxy = d_cov(1,2) / (sqrt(dx) * sqrt(var(d_pixels, 1)));
% 


end



% =============== 哈希函数 ===============
function hashStr = aHash(imagePath)
% 平均哈希实现
    try
        grayImg = readGrayImage(imagePath);
        resizedImg = imresize(grayImg, [8, 8]);
        meanValue = mean(resizedImg(:));
        binaryHash = resizedImg > meanValue;
        hashStr = binaryToHex(binaryHash(:));
    catch ME
        error('aHash失败: %s', ME.message);
    end
end

function hashStr = dHash(imagePath)
% 差异哈希实现
    try
        grayImg = readGrayImage(imagePath);
        resizedImg = imresize(grayImg, [8, 9], 'bilinear');
        diffHash = false(8, 8);
        for i = 1:8
            diffHash(i, :) = resizedImg(i, 2:end) > resizedImg(i, 1:end-1);
        end
        hashStr = binaryToHex(diffHash(:));
    catch ME
        error('dHash失败: %s', ME.message);
    end
end

function hashStr = pHash(imagePath)
% 感知哈希实现
    try
        grayImg = readGrayImage(imagePath);
        resizedImg = imresize(grayImg, [32, 32], 'bilinear');
        dctImg = dct2(double(resizedImg));
        lowFreqBlock = dctImg(1:8, 1:8);
        lowFreqBlock(1,1) = 0;
        meanValue = mean(lowFreqBlock(:));
        binaryHash = lowFreqBlock > meanValue;
        hashStr = binaryToHex(binaryHash(:));
    catch ME
        error('pHash失败: %s', ME.message);
    end
end

% ============= 辅助函数 =============
function grayImg = readGrayImage(imagePath)
% 读取并转换灰度图像
    if ~exist(imagePath, 'file')
        error('文件不存在: %s', imagePath);
    end
    img = imread(imagePath);
    if size(img, 3) == 3
        grayImg = rgb2gray(img);
    else
        grayImg = img;
    end
end

function hexStr = binaryToHex(binaryArray)
% 二进制数组转十六进制
    if numel(binaryArray) ~= 64
        error('输入必须是64位数组');
    end
    hexStr = '';
    for i = 1:16
        bits = binaryArray((i-1)*4+1:i*4);
        hexStr = [hexStr dec2hex(bin2dec(num2str(double(bits)')))]; %#ok<AGROW>
    end
end

function distance = hammingDistance(hex1, hex2)
% 计算汉明距离
    bin1 = hexToBinary(hex1);
    bin2 = hexToBinary(hex2);
    distance = sum(bin1 ~= bin2);
end

function binArray = hexToBinary(hexStr)
% 十六进制转二进制数组
    binStr = '';
    for i = 1:length(hexStr)
        binStr = [binStr dec2bin(hex2dec(hexStr(i)), 4)]; %#ok<AGROW>
    end
    binArray = binStr == '1';
end

function threshold = thresholdCheck(algo)
% 获取各算法阈值
    switch func2str(algo)
        case 'aHash'
            threshold = 5;
        case 'dHash'
            threshold = 5;
        case 'pHash'
            threshold = 10;
        otherwise
            threshold = 10;
    end
end

function result = ternary(condition, trueVal, falseVal)
% 三目运算符模拟
    if condition
        result = trueVal;
    else
        result = falseVal;
    end
end

function [UACI]=pixal_different(image1,image2)
 
diff = double(image1) - double(image2);

abs_diff = abs(diff);

UACI= sum(abs_diff(:))/(512*512*255);
 
 
 
 
end




function [NPCR] = image_num(image1, image2)
    
        % For grayscale images
        [m, n] = size(image1);
        total_pixels = m * n;
        NPCR = sum(sum( image1 ~= image2) )/ total_pixels ;
        
    
end
function psnr_value = calculatePSNR(image1, image2)
% 计算两幅图像之间的PSNR值
% 输入:
%   img1, img2 - 输入图像（灰度或彩色）
% 输出:
%   psnr_value - PSNR值(dB)

    % 验证输入图像尺寸相同
    if ~isequal(size(image1), size(image2))
        error('输入图像尺寸必须相同');
    end
    
    % 转换为double类型
    img1_double = double(image1);
    img2_double = double(image2);
    
    % 计算均方误差(MSE)
    mse = mean((img1_double(:) - img2_double(:)).^2);
    
    % 计算PSNR
    if mse == 0
        psnr_value = Inf; % 图像完全相同
    else
        psnr_value = 20 * log10(255 / sqrt(mse));
    end
end