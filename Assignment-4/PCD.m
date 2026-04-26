clear; clc; close all;

img_rgb = imread('grayscale.jpg');
if size(img_rgb, 3) == 3
    img_gray = rgb2gray(img_rgb);
else
    img_gray = img_rgb;
end
img_double = im2double(img_gray);

% noise Salt & Pepper
img_sp = imnoise(img_double, 'salt & pepper', 0.05);
% noise Gaussian
img_gauss = imnoise(img_double, 'gaussian', 0, 0.01);

%% FILTERING DOMAIN SPASIAL
% a. Mean Filter
h_mean3 = fspecial('average', [3 3]);
sp_mean3 = imfilter(img_sp, h_mean3, 'replicate');

h_mean5 = fspecial('average', [5 5]);
sp_mean5 = imfilter(img_sp, h_mean5, 'replicate');

% b. Gaussian Smoothing
h_gauss_spasial = fspecial('gaussian', [5 5], 1.5);
sp_gauss = imfilter(img_gauss, h_gauss_spasial, 'replicate');

% c. Laplacian Filter
h_laplacian = fspecial('laplacian', 0);
sp_laplacian = imfilter(img_double, h_laplacian, 'replicate');

% d. Sharpening
h_sharp = [0 -1 0; -1 5 -1; 0 -1 0]; 
sp_sharp = imfilter(img_double, h_sharp, 'replicate');

%% FILTERING DOMAIN FREKUENSI

[M, N] = size(img_double);
F = fftshift(fft2(img_gauss)); 

u = 0:(M-1); v = 0:(N-1);
idx = find(u > M/2); u(idx) = u(idx) - M;
idy = find(v > N/2); v(idy) = v(idy) - N;
[V, U] = meshgrid(v, u);
D = sqrt(U.^2 + V.^2);

D0 = 50; 
n = 2;   

H_ILPF = double(D <= D0);
H_BLPF = 1 ./ (1 + (D ./ D0).^(2*n));
H_GLPF = exp(-(D.^2) ./ (2*(D0^2)));


H_IHPF = double(D > D0);
D_safe = D; D_safe(D_safe == 0) = eps; 
H_BHPF = 1 ./ (1 + (D0 ./ D_safe).^(2*n));
H_GHPF = 1 - exp(-(D.^2) ./ (2*(D0^2)));

apply_freq_filter = @(H, F_img) real(ifft2(ifftshift(H .* F_img)));

freq_ilpf = apply_freq_filter(H_ILPF, F);
freq_blpf = apply_freq_filter(H_BLPF, F);
freq_glpf = apply_freq_filter(H_GLPF, F);

F_ori = fftshift(fft2(img_double));
freq_ihpf = apply_freq_filter(H_IHPF, F_ori);
freq_bhpf = apply_freq_filter(H_BHPF, F_ori);
freq_ghpf = apply_freq_filter(H_GHPF, F_ori);

% Plot Citra Asli & Noise
figure('Name', 'Input Citra Asli dan Noise');
subplot(1,3,1), imshow(img_double), title('Citra Asli');
subplot(1,3,2), imshow(img_sp), title('Noise Salt & Pepper');
subplot(1,3,3), imshow(img_gauss), title('Noise Gaussian');

% Plot Hasil Spasial
figure('Name', 'Filtering Domain Spasial');
subplot(2,3,1), imshow(img_sp), title('Input S&P');
subplot(2,3,2), imshow(sp_mean3), title('Mean 3x3');
subplot(2,3,3), imshow(sp_mean5), title('Mean 5x5');
subplot(2,3,4), imshow(img_gauss), title('Input Gaussian');
subplot(2,3,5), imshow(sp_gauss), title('Gaussian Smooth');
subplot(2,3,6), imshow(sp_sharp), title('Sharpening');

% Plot Hasil Frekuensi Lowpass
figure('Name', 'Filtering Domain Frekuensi (Lowpass)');
subplot(1,4,1), imshow(img_gauss), title('Input Noise Gaussian');
subplot(1,4,2), imshow(freq_ilpf, []), title('ILPF (Ideal)');
subplot(1,4,3), imshow(freq_blpf, []), title('BLPF (Butterworth)');
subplot(1,4,4), imshow(freq_glpf, []), title('GLPF (Gaussian)');

% Plot Hasil Frekuensi Highpass
figure('Name', 'Filtering Domain Frekuensi (Highpass)');
subplot(1,4,1), imshow(img_double), title('Input Citra Asli');
subplot(1,4,2), imshow(freq_ihpf, []), title('IHPF (Ideal)');
subplot(1,4,3), imshow(freq_bhpf, []), title('BHPF (Butterworth)');
subplot(1,4,4), imshow(freq_ghpf, []), title('GHPF (Gaussian)');