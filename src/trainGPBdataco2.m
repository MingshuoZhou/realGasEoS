clc; clear; close all;

%%
%  p=parpool(8);
% Loading data
tic
dataNames = ["co2"];%,"nc10h22","o2","h2o","c12h26","C6H5CH3","c6h12",
% dataNames = ["n2"]
P = ["7"];%, '10', '15', '20'
files = ["A", "C", "D", "H","L" , "S",  "V"];%"A", "C", "D", "H", , "S",  "V"

Pn=size(P,2);
M=size(files,2);
%%
for i=1:Pn
    for k= 1:M
        %model 2
        dataFile = sprintf('../mechco2/%s_%s.csv',P(i), files(k));
        paraFile = sprintf('../mechco2/%s_%s_para.csv',P(i), files(k));
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
        sigma0 = 0.5*std(Y(:));
        sigmaF0 = sigma0;
        d = size(X(:),2);
        sigmaM0 = 80*ones(d,1);%'KernelParameters',[sigmaM0;sigmaF0],'Sigma',sigma0,
        gprMdl = fitrgp(X(:,:), Y(:), 'BasisFunction', 'linear', ...
            'KernelFunction','ardsquaredexponential',  ...
            'FitMethod','exact','PredictMethod', 'exact', 'Optimizer', 'lbfgs', 'OptimizeHyperparameters', 'all', ...
            'HyperparameterOptimizationOptions',struct('UseParallel',1, 'ShowPlots',0));%,'AcquisitionFunctionName','expected-improvement-plus'

        Xtest = X(Ntrain+1:end,:);
        Ytest = Y(Ntrain+1:end);
        Xpre = linspace(min(X),max(X),2000)';
        L = loss(gprMdl,Xtest,Ytest)

        Ypred = predict(gprMdl,Xtest);
        Ypre = predict(gprMdl,Xpre);

        plot(Y(:), Y(:), 'k--'); hold on;
        plot(Y(:), resubPredict(gprMdl), 'rv'); hold on;
        plot(Ytest, Ypred, 'b.'); hold on;

        figure()
        plot(X(1:Ntrain), Y(1:Ntrain), 'k*'); hold on;
        plot(X(:), resubPredict(gprMdl), 'rv'); hold on;
        plot(Xtest, Ypred, 'g.'); hold on;
        plot(Xpre, Ypre, 'k'); hold on;

        disp(gprMdl.Beta)
        disp(gprMdl.KernelInformation.KernelParameterNames)
        disp(gprMdl.KernelInformation.KernelParameters)
        
        % Model 2
        H = HGPB2(X(1:Ntrain,:),X(1:Ntrain,:),dim,gprMdl.KernelInformation.KernelParameters(1:dim),...,
        gprMdl.KernelInformation.KernelParameters(end));
        %para = [gprMdl.KernelInformation.KernelParameters'; gprMdl.Beta';H;[yscale,0]];
        % % model 3
        % H=HGPB(X(1:Ntrain,:),X(1:Ntrain,:),dim,gprMdl.KernelInformation.KernelParameters(1:dim),...,
        % gprMdl.KernelInformation.KernelParameters(end))
        % para = [gprMdl.KernelInformation.KernelParameters'; gprMdl.Beta';H;[yscale,0,0]];

        %writematrix(para, paraFile);
    end
end
toc

% delete(p);