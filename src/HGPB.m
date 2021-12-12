function [H] = HGPB(X1, X2,dim, gamma, sigma)
    cov = zeros(length(X1),length(X2));
    for i=1:length(X1)
        for j=1:length(X2)
            cov(i,j)=sigma.^2*exp(-((X1(i,1)-X2(j,1)).^2/2/gamma(1).^2)-((X1(i,2)-X2(j,2)).^2/2/gamma(2).^2));
        end
    end
    df=dfdth(X1);
    Hm=zeros(dim+1,dim+1);
    for i=1:length(X1)
        for j= 1:length(X1)
            Hm=Hm+df(i,:)'*df(j,:)*cov(i,j);
        end
    end
    H=Hm./length(X1)./length(X2);
end
function [df] = dfdth(x)
    df=[ones(length(x),1),x(:,1),x(:,2)];
end