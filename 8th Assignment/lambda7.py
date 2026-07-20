matrix=[[1,2,3],[2,4,5],[1,1,1]]
print(sorted(matrix,key=lambda row:sum(row)))
matrix2=[[1,2,3],[-2,4,-5],[1,-1,1]]
print(sorted(matrix2,key=lambda row:sum(row)))
