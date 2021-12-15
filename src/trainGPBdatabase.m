% p=parpool(8);
% Loading data
tic
dataNames = ["CO2","CH4","H2","O2","H2O"];
files = ["conductivity", "Cpmass", "Density", "Hmass", "Smass", "A", "Umass", "viscosity"];

N=size(dataNames,2);
M=size(files,2);
for i=1:N
  
    dataName=dataNames(i);
    for j=1:M
        file=files(j);
        dataFile = sprintf('../mech/%s/%s.csv',file,dataName);
        paraFile = sprintf('../mech/%s/%s_para.csv',file,dataName);

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
           'PredictMethod', 'exact', 'OptimizeHyperparameters', 'auto', ...
           'HyperparameterOptimizationOptions',struct('UseParallel',1, 'ShowPlots',0));

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

    end
end
toc
% delete(p);