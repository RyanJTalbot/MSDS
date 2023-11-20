PROGRAM hello

 USE mpi

 INTEGER, PARAMETER:: dp=KIND(0.d0)

 INTEGER ::  ierr, comm_size, comm_rank, length
 REAL(dp) :: RESULT
 CHARACTER (len=MPI_MAX_PROCESSOR_NAME) :: proc_name

 CALL MPI_Init(ierr)
 CALL MPI_Comm_size(MPI_COMM_WORLD, comm_size, ierr)
 CALL MPI_Comm_rank(MPI_COMM_WORLD, comm_rank, ierr)
 CALL MPI_Get_processor_name(proc_name, length, ierr)

 WRITE(*,*) "Hello World from process = ", comm_rank, " on processor ", proc_name

 RESULT = EXP(REAL(comm_rank, dp))

 WRITE(*,*) "Exp(", comm_rank, ") = ", RESULT

 CALL MPI_Barrier(MPI_COMM_WORLD, ierr);
 IF (comm_rank == 0) THEN
    WRITE(*,*) "Number of mpi processes = ", comm_size
 ENDIF
 CALL MPI_Finalize(ierr);

END PROGRAM hello
