clc; clear; close all;

%%
 p=parpool(8);
% Loading data
tic
dataNames = ["co2","ch4","h2","o2","h2o","c12h26"];
files = ["conductivity", "Cpmass", "Density", "Hmass", "Hmole", "Smass", "Smole", "A", "Umass", "Umole", "viscosity", "Cpmole"];

N=size(dataNames,2);
M=size(files,2);

for i=1:N
    for j=1:M
        dataName(floor(i-1)*M+j)=dataNames(i);
        file(floor(i-1)*M+j)=files(j);
    end
end

parfor i=1:N*M
    dataFile = sprintf('../mech2/%s/%s.csv',file(i),dataName(i));
    paraFile = sprintf('../mech2/%s/%s_para.csv',file(i),dataName(i));

    Data = load(dataFile);
    N = size(Data,1);
    dim = size(Data,2)-1;
    idx = randperm(N);
    X = Data(idx,1:dim);
    Y = Data(idx,end);
    
    yscale=max(Y)-min(Y);
    Y=Y/yscale;
    
    % Training
    Ntrain = floor(N*0.8);
    gprMdl = fitrgp(X(1:Ntrain,:), Y(1:Ntrain), 'BasisFunction', 'linear', ...
           'KernelFunction','ardsquaredexponential', 'FitMethod','exact', ...
           'PredictMethod', 'exact', 'OptimizeHyperparameters', 'auto', ...
           'HyperparameterOptimizationOptions',struct('UseParallel',0, 'ShowPlots',0));

    Xtest = X(Ntrain+1:end,:);
    Ytest = Y(Ntrain+1:end);

    Ypred = predict(gprMdl,Xtest);

    plot(Y(1:Ntrain), Y(1:Ntrain), 'k--'); hold on;
    plot(Y(1:Ntrain), resubPredict(gprMdl), 'rv'); hold on;
    plot(Ytest, Ypred, 'g.'); hold on;

    disp(gprMdl.Beta)
    disp(gprMdl.KernelInformation.KernelParameterNames)
    disp(gprMdl.KernelInformation.KernelParameters)

    H=HGPB2(X(1:Ntrain,:),X(1:Ntrain,:),dim,gprMdl.KernelInformation.KernelParameters(1:dim),...,
    gprMdl.KernelInformation.KernelParameters(end))
    para = [gprMdl.KernelInformation.KernelParameters'; gprMdl.Beta';H;[yscale,0]];

    writematrix(para, paraFile);

end
toc

delete(p);