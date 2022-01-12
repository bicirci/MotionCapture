%drawing cube in real time
s = serial('COM4', 'Baudrate', 115200);
fopen(s);

size = 1000;
quats = zeros([size 4]);
accel = zeros([size 3]);
gyro = zeros([size 3]);
magno = zeros([size 3]);

xval = 1;
yaccx = 1;
yaccy = 1;
yaccz = 1;

ygyrx = 1;
ygyry = 1;
ygyrz = 1;

ymagx = 1;
ymagy = 1;
ymagz = 1;

subplot(3,3,1);
h = line(xval, yaccx);
title("Accel x");
axis([0, size, -15, 15]);

subplot(3,3,2);
h2 = line(xval, yaccy);
title("Accel y");
axis([0, size, -15, 15]);

subplot(3,3,3);
h3 = line(xval, yaccz);
title("Accel z");
axis([0, size, -15, 15]);

%gyro
subplot(3,3,4);
h4 = line(xval, ygyrx);
title("Gyro x");
axis([0, size, -0.1, 0.1]);

subplot(3,3,5);
h5 = line(xval, ygyry);
title("Gyro y");
axis([0, size, -0.1, 0.1]);

subplot(3,3,6);
h6 = line(xval, ygyrz);
title("Gyro z");
axis([0, size, -0.1, 0.1]);

%magno
subplot(3,3,7);
h7 = line(xval, ymagx);
title("Magno x");
axis([0, size, -1000, 1000]);

subplot(3,3,8);
h8 = line(xval, ymagy);
title("Magno y");
axis([0, size, -1000, 1000]);

subplot(3,3,9);
h9 = line(xval, ymagz);
title("Magno z");
axis([0, size, -1000, 1000]);


for i = 1:size
    
    temp = fscanf(s);
    splitVals = strsplit(temp);
    for j = 10:13
        quats(i,j-9) = str2double(splitVals(j));
    end
    for j = 1:3
        accel(i,j) =  9.80665 * str2double(splitVals(j));
    end
    for j = 4:6
        gyro(i,j-3) = 2*pi*str2double(splitVals(j))/360;
    end
    
    for j = 7:9
        magno(i,j-6) = str2double(splitVals(j));
    end
    
    %set(h, 'xdata', xval(i), 'yData', accel(i,1));
    xval = [xval, i];
    yaccx = [yaccx, accel(i,1)];
    yaccy = [yaccy, accel(i,2)];
    yaccz = [yaccz, accel(i,3)];
    
    ygyrx = [ygyrx, gyro(i,1)];
    ygyry = [ygyry, gyro(i,2)];
    ygyrz = [ygyrz, gyro(i,3)];
    
    ymagx = [ymagx, magno(i,1)];
    ymagy = [ymagy, magno(i,2)];
    ymagz = [ymagz, magno(i,3)];
    
    set(h, 'xdata', xval,'ydata', yaccx);
    set(h2, 'xdata', xval,'ydata', yaccy);
    set(h3, 'xdata', xval,'ydata', yaccz);
    
    set(h4, 'xdata', xval,'ydata', ygyrx);
    set(h5, 'xdata', xval,'ydata', ygyry);
    set(h6, 'xdata', xval,'ydata', ygyrz);
    
    set(h7, 'xdata', xval,'ydata', ymagx);
    set(h8, 'xdata', xval,'ydata', ymagy);
    set(h9, 'xdata', xval,'ydata', ymagz);
    
    pause(0.05);
end
fclose(s);