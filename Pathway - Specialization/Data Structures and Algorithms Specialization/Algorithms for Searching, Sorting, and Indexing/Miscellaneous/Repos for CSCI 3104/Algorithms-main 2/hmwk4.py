def verifySorted(A):
    for i in range(len(A)-1):
        if A[i] > A[i+1]:
            print(f"A[{i}]=={A[i]} is greater than A[{i+1}]=={A[i+1]}")
            return
    print("Array is sorted!")


# Input:
#  array A from which to find a pivot
# Return:
#  value of the pivot
def pickPivot(A):
    return(A[-1]) # always use the last value of the array A


# Input:
#   A is the array to be partitioned
#   pivotvalue is the value around which to pivot (assumes at least one element
#     has value not less than pivotvalue)
# Return:
#   returns an index in A
#   A has been reordered such that every element below the index is less than
#      the pivotvalue, every element above the index is not less than the
#      pivotvalue, and there are no elements in A that are less than the element
#      at the index that are not less than the pivotvalue
def partitionInPlace(A,pivotvalue):
    lowindex = 0
    highindex = len(A)-1
    i = lowindex - 1
    
    for j in range(lowindex, highindex):
        if A[j] <= pivotvalue: # if element at i is less than or equal to pivot
            i = i + 1 #increment the lowindex
            A[i], A[j] = A[j], A[i] 
    
    A[i + 1], A[highindex] = A[highindex], A[i + 1]
    return(i + 1)
    
    # loop invariant:
    #   every element located lower than lowindex is less than pivotvalue
    #   every element located higher than highindex is not less than pivotvalue
    #   closestindex element is a smallest element not less than pivotvalue
#     while(True):   
        #
        # TO DO
        #

# Input:
#   an array A to be sorted
# Returns:
#   A has been sorted
def quicksort(A):
    # manual sort for small arrays
    if len(A) < 3:
        if len(A) <= 1:
            return
        elif(A[0] > A[1]):
            A[0], A[1] = A[1], A[0]
            return
        else:
            return
              
    # set up recursions
    pivotvalue = pickPivot(A) # find pivot w/ helper
    partitionindex = partitionInPlace(A,pivotvalue) # find index where pivot is located
    
    if partitionindex > 0: 
        quicksort(A[0:partitionindex]) # first half of A
    quicksort(A[partitionindex + 1:len(A)]) # second half of A


### Driver
def main():
    # create
    import numpy.random
    numpy.random.seed(0)
    A = numpy.random.randint(0,100,100)
#     A = [100,1]

    # sort
    quicksort(A)

    # verify
    print(A)
    verifySorted(A)
    

if __name__ == "__main__":
    main()
