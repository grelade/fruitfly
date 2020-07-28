function [HierarchyDegree] = hierarchy(A)

% Step 0: transform weighted adj to unweighted
% A0 = A
% A = disp(A~=0)

% Step 1: Transform the node adjacency matrix to link adjacency matrix

n=size(A,1);
A_edge=zeros(n,n);
k=0;
for i=1:n    % create the matrix in which cells are numberd in sequence.
    for j=1:n
        if A(i,j)>0
            k=k+1;
            A_edge(i,j)=k;
        end
    end
end

n_edge=sum(sum(A));
B=zeros(n_edge,n_edge);
t=0;
for i=1:n
    for j=1:n
        if A_edge(i,j)>0
            for k=1:n
                if A_edge(j,k)>0
                    B(A_edge(i,j),A_edge(j,k))=1;
                end
            end
        end
        t=t+1;
    end
%   disp(sprintf('%.2f EdgeMatrix Created', t/n/n));
end
clear t;

% Step 2: Derive the link distance matrix

L=size(B,1);
all=zeros(L,L);
sumallold=0;
dist=B;
sumuBk=B;
Bk=B;
for k=2:L
    %disp(k)
%   disp(sprintf('Power %.0f / %.0f',k,L));
    Bk=Bk*B;
    uBk=unitize(Bk);
    DBk=(uBk-sumuBk)>0;
    %disp(DBk)
    sumuBk=sumuBk+uBk;
    dist=dist+k*DBk;
    all=unitize(all+DBk);
    sumall=sum(sum(all));
    if sumall==sumallold
        break
    else sumallold=sumall;
    end
end

% Step 3: Calculate hierarchy degree, by counting links not on any cycle

Hierarhical_Link=0;
for i=1:L
	if dist(i,i)== 0
        Hierarhical_Link = Hierarhical_Link + 1;
    end
end
HierarchyDegree = Hierarhical_Link/L;

return

function [unitize]=unitize(A)
% Unitizes a matrix, makes all non zero entries = 1
unitize=A>0;
unitize=unitize+0;
return
