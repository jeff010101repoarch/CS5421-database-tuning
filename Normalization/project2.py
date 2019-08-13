############################################################
## project2.py - Code template for Project 2 - Normalization 
## Both for CS5421 and CS4221 students 
############################################################


### IMPORTANT! Change this to your metric number for grading
student_no = 'A0194935N' 

## Determine the closure of set of attribute S given the schema R and functional dependency F
# remove the element of a list because the shallow copy of python
def remove_element(A, index):
    B = []
    for i in range(0, len(A)):
        if i != index:
            B.append(A[i])
    return B

def closure(R, F, S):
    Omega = F
    Sigma = set(S)
    f_p = []
    while True:
        p = 0
        for f in range(0, len(Omega)):
            if set(Omega[f][0]).issubset(Sigma):
                f_p = Omega[f]
                p = f
                break
        if len(f_p) == 0:
            break
        Omega = remove_element(Omega,p)
        Sigma.update(set(f_p[1]))
        f_p = []
        
    return sorted(Sigma)

## Determine the all the attribute closure excluding superkeys that are not candidate keys given the schema R and functional dependency F
# get all subsets
def Subset(items):
    
    if len(items) == 0:
        return [[]]
    
    subsets = []
    first_elt = items[0] #first element
    rest_list = items[1:]

    for partial_sebset in Subset(rest_list):
        subsets.append(partial_sebset)
        next_subset = partial_sebset[:] +[first_elt]
        subsets.append(sorted(next_subset))
    return sorted(subsets)

def all_closures(R, F): 
    subsets = Subset(R)
    closures_all = []
    key = []
    for i in subsets:
        if len(i)!=0:
            closure_s = closure(R,F,i)
            if len(closure_s) == len(R):
                key.append(i)
            else:
                closures_all.append([i,closure_s])
    for i in key:
        n = 0
        for j in key:
            if set(j).issubset(i):
                n = n+1
        if n==1:
            closures_all.append([i,R])
            
    return sorted(closures_all)

## Return the candidate keys of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS5421 students.
def candidate_keys(R, F): 
    subsets = Subset(R)
    closures_all = []
    key = []
    for i in subsets:
        if len(i)!=0:
            closure_s = closure(R,F,i)
            if len(closure_s) == len(R):
                key.append(i)
            else:
                closures_all.append([i,closure_s])
    candidate_key = []
    for i in key:
        n = 0
        for j in key:
            if set(j).issubset(i):
                n = n+1
        if n==1:
            candidate_key.append(i)
            
    return sorted(candidate_key)
    
## Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
# sigma_1 singliton the RHS
def get_sigma1(R,FD):
    FD_new = []
    for i in FD:
        for j in i[1]:
            FD_new.append([i[0],[j]])
    return FD_new

# as the naive FD do not help to the final, we delete them
def filter_naive(FD):
    FD_new = []
    for i in FD:
        indictor = True
        if (set(i[1]).issubset(set(i[0]))):
            indictor = False
        if indictor:
            FD_new.append(i)
    return FD_new

# sigma 2 simplify the LHS

def LHS_simply(R,FD, FDs):
    X = FD[0]
    Y = FD[1]
    X_rm_l = []
    X_rm = []
    for i in X:
        S = set(X)
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

def get_sigma2_integ(R,sigma_1,FD):
    sigma_2 = []
    for i in range(0,len(sigma_1)):
        simple_LHS = LHS_simply1(R,sigma_1[i], FD)
        #print(simple_LHS)
        sigma_2.append(simple_LHS)
    return sorted(sigma_2)

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
    B = cross_join(A)
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
    sigma_1_filtered = sigma_1
    sigma_2 = get_sigma2(R,sigma_1_filtered,FD)
    sigma_2_filtered = sigma2_filter(sigma_2)
    sigma_3 = get_sigma3(R,sigma_2_filtered)
    sigma_3_filtered = sigma3_filter(sigma_3)
    return sigma_3_filtered[0]

## Return all minimal covers reachable from the functional dependencies of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS4221 students.
def min_covers(R, FD):
    sigma_1 = get_sigma1(R,FD)
    sigma_1_filtered = sigma_1
    sigma_2 = get_sigma2(R,sigma_1_filtered,FD)
    sigma_2_filtered = sigma2_filter(sigma_2)
    sigma_3 = get_sigma3(R,sigma_2_filtered)
    sigma_3_filtered = sigma3_filter(sigma_3)
    return sigma_3_filtered

## Return all minimal covers of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS4221 students.
def all_min_covers(R, FD):
    sigma_plus = all_closures(R, FD)
    sigma_1_plus = get_sigma1(R,sigma_plus)
    sigma_1_plus_filtered = filter_naive(sigma_1_plus)
    sigma_2_plus = get_sigma2(R,sigma_1_plus_filtered,FD)
    sigma_2_plus_filtered = sigma2_filter(sigma_2_plus)
    sigma_3_plus = get_sigma3(R,sigma_2_plus_filtered)
    sigma_3_plus_filtered = sigma3_filter(sigma_3_plus)
    return sigma_3_plus_filtered

### Test case from the project
R = ['A', 'B', 'C', 'D']
FD = [[['A', 'B'], ['C']], [['C'], ['D']]]

print closure(R, FD, ['A'])
print closure(R, FD, ['A', 'B'])
print all_closures(R, FD)
print candidate_keys(R, FD)

R = ['A', 'B', 'C', 'D', 'E', 'F']
FD = [[['A'], ['B', 'C']],[['B'], ['C','D']], [['D'], ['B']],[['A','B','E'], ['F']]]
print min_cover(R, FD) 

R = ['A', 'B', 'C']
#FD = [[['A', 'B'], ['C']],[['A'], ['B']], [['B'], ['A']]] 
FD = [[['A', 'C'], ['C']],[['A'], ['B']], [['B'], ['A']], [['B'], ['C']]] 
print min_covers(R, FD) 
print all_min_covers(R, FD) 

## Tutorial questions
R = ['A', 'B', 'C', 'D', 'E']
FD = [[['A', 'B'],['C']], [['D'],['D', 'B']], [['B'],['E']], [['E'],['D']], [['A', 'B', 'D'],['A', 'B', 'C', 'D']]]

print candidate_keys(R, FD)
print min_cover(R, FD)
print min_covers(R, FD)
print all_min_covers(R, FD) 
