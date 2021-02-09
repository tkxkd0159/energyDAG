clear
close all
ns = 4; % # of samples

d{1} = load('dagLog_np2.txt');
d{2} = load('dagLog_np3.txt');
d{3} = load('dagLog_np4.txt');
d{4} = load('dagLog_m2m2m.txt');

li = {'--r','-.g',':b','-k'};

% plot(a(:,2));
% hold on
% plot(b(:,2));
% plot(c(:,2));
% legend('2','3','4');

figure
for i = 1:ns
    plot(d{i}(:,2));
    hold on
end
legend('n=2','n=3','n=4','M2M2M');

t{1} = load('txLog_np2.txt');
t{3} = load('txLog_np3.txt');
t{4} = load('txLog_np4.txt');
t{2} = load('txLog_m2m2m.txt');

figure
for i = 1:ns
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
    legend('n=2','n=3','n=4','M2M2M');
end

figure

for i = 1:ns
    subplot(1,3,1);
    plot(t{i}(:,2));
    hold on    
    subplot(1,3,2);
    plot(t{i}(:,3));
    hold on
    subplot(1,3,3);
    plot(t{i}(:,2) + t{i}(:,3));
    hold on
end

for i = 1:3
    subplot(1,3,i);
%     legend('1.5','2','2.5','3','3.5','4');
    legend('n=2','n=3','n=4','M2M2M');
end

figure
for i = 1:ns
    cdfplot(t{i}(:,2) + t{i}(:,3));
    hold on
end
legend('n=2','n=3','n=4','M2M2M');