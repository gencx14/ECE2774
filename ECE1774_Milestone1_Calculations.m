clear
clc

        % This program is made to calculate values for PowerWorld for the
        % transmission lines

        %	Initialize variables
eo=8.854e-12;
muo=pi*4e-7;
j = sqrt(-1);


        %   Input Values
Line_Name = 'Partridge';
Dab = (18/12) + 18;     % Dab in feet - these distances are for 3 points in a line (. . .)
Dbc = (18/12) + 18;     % Dbc in feet
Dca = Dab + Dbc;        % Dca in feet
GMR = 0.0217;           % From data sheet, in feet
length = 10;            % Length of wire in miles
n = 2;                  % Number of conductors per bundle
diam = 0.642;           % Diameter of conductor in inches
r = diam/2/12;          % Radius of conductor in feet
d = 1.5;                % Distance between conductors in a bundle in feet, set to 0 if one conductor
Rac = 0.385;            % Ohms/mile - datasheet
f = 60;                 % Frequency in Hertz
w = 2 * pi * f;         % Frequency in rad/s



        %	Perform calculations
Deq = sqrt(Dab*Dbc*Dca);
switch n
    case 1
        Dsl = GMR;
        Dsc = r;
    case 2
        Dsl = sqrt(d*GMR);
        Dsc = sqrt(d*r);
    case 3
        Dsl = nthroot(d^2 * GMR, 3);
        Dsc = nthroot(d^2 * r, 3);
    case 4
        Dsl = 1.091 * nthroot(d^3 * GMR, 4);
        Dsc = 1.091 * nthroot(d^3 * r, 4);
end
R_prime = Rac / n;  % Resistance in Ohms/mile
L_prime = 2*10^-7 * log(Deq/Dsl);   % Inductance in H/m
C_prime = 2*pi*eo/log(Deq/Dsc);     % Capacitance in F/m 

X_prime = w * L_prime;              % Reactance in Ohms/m
Y_prime = j * w * C_prime;    % Shunt admittance in S/m

R = R_prime * 1609.34 * length;       % Series resistance in Ohms
X = X_prime * 1609.34 * length;       % Series reactance in Ohms
Y_shunt = Y_prime * 1609.34 * length; % Shunt admittance in S

        % Display Results
disp(['For the ', num2str(length), ' mile long, transposed, ', num2str(n),'-conductor ', Line_Name, ' line:'])
disp(['The series resistance R = ', num2str(R), ' Ohms'])
disp(['The series reactance X = ', num2str(X), ' Ohms'])
disp(['The shunt admittance Y = ', num2str(Y_shunt), ' S'])
