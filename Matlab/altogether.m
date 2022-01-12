%drawing cube in real time
s = serial('COM4', 'Baudrate', 115200);
fopen(s);

size = 10000;
quats = zeros([size 4]);
accel = zeros([size 3]);
gyro = zeros([size 3]);
magno = zeros([size 3]);


%subplot(2,2,1);
viewer = fusiondemo.OrientationViewer;
title("AHRS filter Matlab");
%subplot(2,2,2);
viewer1 = fusiondemo.OrientationViewer;
title("IME filter Matlab");
%subplot(2,2,3);
viewer2 = fusiondemo.OrientationViewer;
title("Accel and Magno");
%subplot(2,2,4);
viewer3 = fusiondemo.OrientationViewer;
title("Open Source");

gyronoise = 3.0462e-06;
accelnoise = 0.0061;
FUSE = ahrsfilter('SampleRate', 2, 'GyroscopeNoise', gyronoise, ...
    'AccelerometerNoise', accelnoise);
ifilt = imufilter('SampleRate', 2);
qe = ecompass(accel,magno);


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
    
    
    qahrs = FUSE(accel(i,:), gyro(i,:), magno(i,:));
    viewer(qahrs);

    qimu = ifilt(accel(i,:),gyro(i,:));
    viewer1(qimu);

    qe = ecompass(accel(i,:)*100,magno(i,:));
    viewer2(qe);

    q = quaternion(quats(i,1), quats(i,2), quats(i,3), quats(i,4));
    viewer3(q);

    pause(0.05);
end
fclose(s);
