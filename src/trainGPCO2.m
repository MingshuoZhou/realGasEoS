clc; clear; close all;

%%
%  p=parpool(8);
% Loading data
tic
dataNames = ["co2"];%,"nc10h22","o2","h2o","c12h26","C6H5CH3","c6h12",
% dataNames = ["n2"]
P = ["7", '10', '15', '20'];
files = ["A", "C", "D", "H", "L", "S",  "V"];

Pn=size(P,2);
M=size(files,2);

for i=1:Pn
    for k= 1:M
        %model 2
        dataFile = sprintf('../mechco2/%s_%s.csv',P(i), files(k));
        paraFile = sprintf('../mechco2/%s_%s_gppara.csv',P(i), files(k));
        % %model 3
        % dataFile = sprintf('../mech/%s/%s.csv',file(i),dataName(i));
        % paraFile = sprintf('../mech/%s/%s_para.csv',file(i),dataName(i));

        Data = load(dataFile);
        N = size(Data,1);
        dim = size(Data,2)-1;
        idx = randperm(N);
        X = Data(idx,1:dim);
        Y = Data(idx,end);
        
        yscale=(max(Y)-min(Y));
        Y=Y/yscale;
        
        % Training
        Ntrain = floor(N*0.8);
        gprMdl = fitrgp(X(1:Ntrain,:), Y(1:Ntrain), 'BasisFunction', 'none', ...
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

        para = [gprMdl.KernelInformation.KernelParameters'; gprMdl.Beta';[yscale,0]];

        writematrix(para, paraFile);
    end
end
toc

% delete(p);