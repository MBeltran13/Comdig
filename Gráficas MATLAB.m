datos = readmatrix('SaveDataLaunch.csv');

% Extrae las columnas de datos
t = datos(:, 1);
AX = datos(:, 2);
AY = datos(:, 3);
AZ = datos(:, 4);
GX = datos(:, 5);
GY = datos(:, 6);
GZ = datos(:, 7);
ALTURA = datos(:, 8);

% Grafica 1
figure;
plot(t, AX,'r',t,AY,'g',t,AZ,'b');
title('Gráfico de Aceleración vs Tiempo');
xlabel('Tiempo');
ylabel('Aceleración');
zlabel('Variables AX, AY y AZ');
legend('AX', 'AY', 'AZ');

%Grafica 2
figure;
plot(t, GX,t,GY,t,GZ)
title('Gráfico de Giroscopio vs Tiempo');
xlabel('Tiempo');
ylabel('Giroscopio');
legend('GX', 'GY', 'GZ');

% Grafica 3
figure;
plot(t, ALTURA);
title('Grafica Altura vs Tiempo');
xlabel('Tiempo');
ylabel('Altura');
legend('ALTURA');
