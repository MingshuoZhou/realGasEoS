% Loading data
tic
dataName = 'c12h26';

dataFile = ['../mech/Alpha/' dataName '.csv'];
paraFile = ['../mech/Alpha/' dataName '_para.csv'];

% dataFile = ['../mech/CP/' dataName '.csv'];
% paraFile = ['../mech/CP/' dataName '_para.csv'];

% dataFile = ['../mech/H/' dataName '.csv'];
% paraFile = ['../mech/H/' dataName '_para.csv'];

Data = load(dataFile);
N = size(Data,1);
dim = size(Data,2)-1;
idx = randperm(N);
X = Data(idx,1:dim);
Y = Data(idx,end);

% Training
Ntrain = floor(N*0.8);
gprMdl = fitrgp(X(1:Ntrain,:), Y(1:Ntrain), 'BasisFunction', 'linear', ...
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

H=HGPB(X(1:Ntrain,:),X(1:Ntrain,:),dim,gprMdl.KernelInformation.KernelParameters(1:dim),...,
gprMdl.KernelInformation.KernelParameters(end))
para = [gprMdl.KernelInformation.KernelParameters'; gprMdl.Beta';H];

writematrix(para, paraFile);
toc