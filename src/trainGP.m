% Loading data
dataName = 'c12h26';

dataNames = ["co2","ch4","h2","o2","h2o","c12h26"];
files = ["conductivity", "Cpmass", "Density", "Hmass", "Hmole", "Smass", "Smole", "A", "Umass", "Umole", "viscosity", "Cpmole"];

Data = load(dataFile);
N = size(Data,1);
dim = size(Data,2)-1;
idx = randperm(N);
X = Data(idx,1:dim);
Y = Data(idx,end);

% Training
Ntrain = floor(N*0.9);
gprMdl = fitrgp(X(1:Ntrain,:), Y(1:Ntrain), 'BasisFunction', 'Linear', ...
               'KernelFunction','ardsquaredexponential', 'FitMethod','exact', ...
               'PredictMethod', 'exact', 'OptimizeHyperparameters', 'auto');

Xtest = X(Ntrain+1:end,:);
Ytest = Y(Ntrain+1:end);

Ypred = predict(gprMdl,Xtest);

plot(Y(1:Ntrain), Y(1:Ntrain), 'k--'); hold on;
plot(Y(1:Ntrain), resubPredict(gprMdl), 'rv'); hold on;
plot(Ytest, Ypred, 'g.'); hold on;

disp(gprMdl.Beta)
disp(gprMdl.KernelInformation.KernelParameterNames)
disp(gprMdl.KernelInformation.KernelParameters)

para = [gprMdl.KernelInformation.KernelParameters'; gprMdl.Beta'];

writematrix(para, paraFile);
