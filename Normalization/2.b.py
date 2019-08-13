## Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.

## sigma_1 singliton the RHS
def get_sigma1(R,FD):
    FD_new = []
    for i in FD:
        for j in i[1]:
            FD_new.append([i[0],[j]])
    return FD_new

## sigma_2 simplify LHS

# filiter naive FDs
def filter_naive(FD):
    FD_new = []
    for i in FD:
        indictor = True
        if (set(i[1]).issubset(set(i[0]))):
            indictor = False
        if indictor:
            FD_new.append(i)
    return FD_new

# simplify LHS of a single FD
def LHS_simply(R,FD, FDs):
    X = FD[0]
    Y = FD[1]
    X_rm_l = []
    X_rm = []
    for i in X:
        S = set(X.copy())
        S.remove(i)
        B = list(S)
        S1 = set(closure(R,FDs,B))
        if set(Y).issubset(S1) or set(i).issubset(S1):
            X_rm_l.append(i)
    if len(X_rm_l)==0:
        return []
    else:
        for i in X_rm_l:
            S = set(X)
            S.remove(i)
            B = list(S)
            X_rm_n = LHS_simply(R,[B,Y], FDs)
            if len(X_rm_n)==0:
                X_rm.append([i])
            else:
                for j in X_rm_n:
                    X_rm.append([i]+j)
    return X_rm

def LHS_simply1(R,FD, FDs):
    X = FD[0]
    Y = FD[1]
    simple = LHS_simply(R,FD, FDs)
    simple_1 = []
    for i in simple:
        indictor = True
        for j in simple_1:
            if len(set(j)-set(i))==0:
                indictor = False
        if indictor:
            simple_1.append(i)
    X_sim = []
    if len(simple_1)==0:
        return [FD]
    else:
        for i in simple_1:
            S = set(X)
            for j in i:
                S.remove(j)
            B = list(S)
            X_sim.append(sorted(B))
        FD_return = []
        for i in X_sim:
            FD_return.append([i, Y])
        if len(X_sim)==1:
            return sorted(FD_return)
        else:
            return sorted(FD_return)

# simplify LHS of all FDs, get all cases in integrated form
def get_sigma2_integ(R,sigma_1,FD):
    sigma_2 = []
    for i in range(0,len(sigma_1)):
        simple_LHS = LHS_simply1(R,sigma_1[i], FD)
        #print(simple_LHS)
        sigma_2.append(simple_LHS)
    return sorted(sigma_2)

# get all cases of FDs
def cross_join(A):
    C = []
    if len(A) == 1:
        for i in A[0]:
            C.append([i])
    else:
        for i in A[0]:
            B = cross_join(A[1:])
            for j in B:
                C.append(j+[i])
    return C

### remove same FDs and left one of them
def filter_same_dependence(FD):
    FD_new = []
    
    for i in FD:
        indictor = True
        #print(i)
        X_1 = set(i[0])
        Y_1 = set(i[1])
        #print(i,FD_new)
        for j in FD_new:
            X_2 = set(j[0])
            Y_2 = set(j[1])
            #print(X_1,X_2,Y_1,Y_2)
            if (len(X_1-X_2)==0 and len(X_2-X_1)==0) and (len(Y_1-Y_2)==0 and len(Y_2-Y_1)==0):
                indictor = False
        if indictor:
            FD_new.append(i)
    return sorted(FD_new)

def get_sigma2(R,sigma_1,FD):
    A = get_sigma2_integ(R,sigma_1,FD)
    C = sigma2_filter(A)
    B = cross_join(C)
    C_filter = []
    for i in B:
        C_filter.append(filter_same_dependence(i))
    return sorted(C_filter)

# remove rebandant FDs in sigma2
# compare FD1 and FD2 are same
def compare_FD(FD_1,FD_2):
    if len(FD_1)!=len(FD_2):
        return False
    else:
        A = filter_same_dependence(FD_1+FD_2)
        #print(len(A),A)
        if len(A) == len(FD_1):
            return True
        else:
            return False

# filter sigma_2 cases, remove the same case
def sigma2_filter(sigma_2):
    A = []
    i = 0
    A.append(sigma_2[0])
    while(i <= len(sigma_2)-1):
        for j in range(i+1, len(sigma_2)+1):
            if j>len(sigma_2)-1:
                i = j
                break
            else:
                indictor = compare_FD(sigma_2[i],sigma_2[j])
                #print(i,j,indictor)
                if (indictor==False):
                    A.append(sigma_2[j])
                    i = j
                    break
    return A


def get_sigma3_case(FD,labels):
    sigma = []
    for i in labels:
        sigma.append(FD[i])
    return sigma

# remove rebandunt FD and get different case
def remove(R,FD,keep_label):
    keep_label_set = set(keep_label)
    #print(keep_label_set)
    label_all = []
    indictor = True
    for i in keep_label_set:
        label_new = keep_label_set-{i}
        S = get_sigma3_case(FD,label_new-{i})
        if set(FD[i][1]).issubset(closure(R,S,FD[i][0])):
            keep_label_low = remove(R,FD,list(label_new))
            #print(keep_label_low)
            for j in keep_label_low:
                label_all.append(j)
            indictor = False
    if indictor:
        label_all = [keep_label]
        
    #print(label_all)
    return label_all

# remove same cases
def remove_same(labels):
    label_new = []
    for i in labels:
        indictor = True
        for j in label_new:
            if len(set(i)-set(j))==0 and len(set(j)-set(i))==0:
                indictor = False
            #print(indictor)
        if indictor:
            label_new.append(i)
        #print(label_new)
    return label_new

# get sigma3 of different cases for different cases
def get_sigma3(R,sigma_2):
    sigma_3 = []
    for i in range(0,len(sigma_2)):
        labels = remove_same(remove(R,sigma_2[i],range(0,len(sigma_2[i]))))
        for j in range(0,len(labels)):
            #print(sigma_2[i],labels[j])
            A = get_sigma3_case(sigma_2[i],labels[j])
            sigma_3.append(A)
    return sorted(sigma_3)

#  filter the same sigma3
def sigma3_filter(A):
    return sigma2_filter(A)



def min_cover(R, FD):
    sigma_1 = get_sigma1(R,FD)
    sigma_1_filtered = filter_naive(sigma_1)
    sigma_2 = get_sigma2(R,sigma_1_filtered,FD)
    sigma_2_filtered = sigma2_filter(sigma_2)
    sigma_3 = get_sigma3(R,sigma_2_filtered)
    sigma_3_filtered = sigma3_filter(sigma_3)
    return sigma_3_filtered[0]
