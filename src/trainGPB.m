% Loading data
tic
dataname = "CO2";
files = ["C"];

dataFile = sprintf('../mechco2/%s_%s_2.csv',dataname, files);
paraFile = sprintf('../mechco2/%s_%s_para2.csv',dataname, files);

% dataFile = ['../mech/CP/' dataName '.csv'];
% paraFile = ['../mech/CP/' dataName '_para.csv'];

% dataFile = ['../mech/H/' dataName '.csv'];
% paraFile = ['../mech/H/' dataName '_para.csv'];

Data = load(dataFile);
N = size(Data,1);
dim = size(Data,2)-1;
idx = randperm(N);
X = Data(idx,1:dim);
Y = Data(idx,end)/max(Data(idx,end));
yscale=max(Data(idx,end));
% Training
Ntrain = floor(N*0.9);
gprMdl = fitrgp(X(1:Ntrain,:), Y(1:Ntrain), 'BasisFunction', 'linear', ...
           'KernelFunction','ardexponential', 'FitMethod','exact', ...
           'PredictMethod', 'exact','Optimizer', 'lbfgs', 'OptimizeHyperparameters', 'auto', ...
           'HyperparameterOptimizationOptions',struct('UseParallel',1, 'ShowPlots',0));
toc
%%
tic
Xtest = X(Ntrain+1:end,:);
Ytest = Y(Ntrain+1:end);
Xpre(:,1) = linspace(min(X(:,1)),max(X(:,1)),2000)';
Xpre(:,2) = 2;

Ypred = predict(gprMdl,Xtest);
Ypre = predict(gprMdl,Xpre);

plot(Y(1:Ntrain), Y(1:Ntrain), 'k--'); hold on;
plot(Y(1:Ntrain), resubPredict(gprMdl), 'rv'); hold on;
plot(Ytest, Ypred, 'gv'); hold on;
xlabel('Groundtruth')
ylabel('Prediction')
legend('data','training data','test data')
grid on

figure()
plot(X(1:Ntrain,1), Y(1:Ntrain), 'k*'); hold on;
plot(X(1:Ntrain,1), resubPredict(gprMdl), 'rv'); hold on;
%plot(Xtest(:,1), Ypred, 'g.'); hold on;
plot(Xpre(:,1), Ypre, 'gv'); hold on;
xlabel('Tr')
ylabel('Cp')
legend('data','training data','predict data')
grid on

disp(gprMdl.Beta)
disp(gprMdl.KernelInformation.KernelParameterNames)
disp(gprMdl.KernelInformation.KernelParameters)

H=HGPB(X(1:Ntrain,:),X(1:Ntrain,:),dim,gprMdl.KernelInformation.KernelParameters(1:dim),...,
gprMdl.KernelInformation.KernelParameters(end))
para = [gprMdl.KernelInformation.KernelParameters'; gprMdl.Beta';H; [yscale,0,0]];

writematrix(para, paraFile);
toc