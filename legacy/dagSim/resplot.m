clear
close all

a = load('dagLog_np2.txt');
b = load('dagLog_np3.txt');
c = load('dagLog_np4.txt');
d = load('dagLog.txt');

li = {'-b','--k','-.r'};

% plot(a(:,2));
% hold on
% plot(b(:,2));
% plot(c(:,2));
% legend('2','3','4');

figure
subplot(2,1,1:2);

plot(a(:,2));
hold on
plot(b(:,2));
plot(c(:,2));
legend('2','3','4');

% t{1} = load('txLog_np1.5.txt');
% t{2} = load('txLog_np2.txt');
% t{3} = load('txLog_np2.5.txt');
% t{4} = load('txLog_np3.txt');
% t{5} = load('txLog_np3.5.txt');
% t{6} = load('txLog_np4.txt');

t{1} = load('txLog_np2.txt');
t{2} = load('txLog_np3.txt');
t{3} = load('txLog_np4.txt');

figure
for i = 1:3
    subplot(1,3,1);
    cdfplot(t{i}(:,2));
    hold on    
    subplot(1,3,2);
    cdfplot(t{i}(:,3));
    hold on
    subplot(1,3,3);
    cdfplot(t{i}(:,2) + t{i}(:,3));
    hold on
end

for i = 1:3
    subplot(1,3,i);
%     legend('1.5','2','2.5','3','3.5','4');
    legend('n=2','n=3','n=4');
    ylabel('CDF');
    title('');    
end