!///////////////////////////////////////////////////////////////////////////////////////////
!   This program is intended for use illustrating the concepts of strong
!   and weak scaling.  There is no useful work done by the program at the moment
!   
!   The user can switch between modes of operation involving nearest-neighbor and global communication
!   Usage:
!           mpiexec -np N ./program -nx X -ny Y -nt T
!           N:   number of MPI ranks
!           X:   number of gridpoints in x-direction (default = 1024)
!           Y:   number of gridpoints in y-direction (default = 4096)
!           T:   number of iterations to run for (default = 100)

!
!   Description:
!           The program will run for T timesteps and execute a smoothing operation on an array of size
!           X x Y at each timestep.   The Y gridpoints are distributed across the N MPI ranks.
!           The X-direction remains in processor always (1-D domain decomposition)
!
PROGRAM Main
  USE ISO_FORTRAN_ENV, ONLY : output_unit, real64
  USE MPI
  
  IMPLICIT NONE

  CHARACTER*8 :: rank_string, nproc_string
  CHARACTER(MPI_MAX_PROCESSOR_NAME) :: node_name
  INTEGER :: ierr, num_proc, my_rank, name_len
  REAL(real64) :: loop_end, loop_start, ticklen
  REAL(real64), ALLOCATABLE :: f(:,:), df(:,:), ftemp(:,:)
  INTEGER :: myleft, myright ! processor id's to "left" and "right"
  INTEGER :: nylocal  ! Number of y-points stored locally
  !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !   Problem Control Parameters
  INTEGER :: niter = 100
  INTEGER :: nyglobal = 4096
  INTEGER :: nxglobal = 1024 
  !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !Initialize MPI  (ierr is an error flag with nonzero value if there's a problem)
  CALL MPI_INIT( ierr )
  !Find number of MPI processes executing this program (num_proc)
  CALL MPI_Comm_size(MPI_COMM_WORLD, num_proc,ierr)
  !Find this process's rank (my_rank; unique numeric identifier for each MPI process)
  CALL MPI_Comm_rank(MPI_COMM_WORLD, my_rank,ierr)
  ! Find the name of this node (node_name)
  CALL MPI_Get_processor_name(node_name, name_len,ierr)
  !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ! Define left and right neighbors
  myright = MOD(my_rank+1,num_proc)
  myleft  = MOD(my_rank-1,num_proc)
  IF (myleft .EQ. -1) myleft = num_proc-1
  IF (myright >= num_proc) myright = 0
  !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  CALL grab_args(nxglobal, nyglobal, niter)
  CALL initialization()
  loop_start = MPI_Wtime()
  CALL main_Loop()
  loop_end = MPI_Wtime()
  ! Print out some information regarding the time and problem size
  IF (my_rank .EQ. 0) THEN
     WRITE(output_unit, '(i6,e12.3,i6,i6,i6)') &
          & num_proc, loop_end-loop_start, nxglobal, nyglobal, niter
  ENDIF
  CALL finalize()
CONTAINS
  ! This subroutine allocates the memory
  SUBROUTINE initialization()
    IMPLICIT NONE
    INTEGER :: modcheck
    nylocal = nyglobal/num_proc


    modcheck = MOD(nxglobal, num_proc)
    IF (my_rank .LT. modcheck) nylocal = nylocal+1
    ALLOCATE(    f( 1:nxglobal , 1:nylocal+2 ))
    ALLOCATE(   df( 1:nxglobal , 1:nylocal+2 ))
    ALLOCATE(ftemp( 1:nxglobal , 1:nylocal+2 ))
    f(:,:) = 0.0
    df(:,:) = 0.0
    ftemp(:,:) = 0.0
  END SUBROUTINE initialization

  ! Run the algorithm
  SUBROUTINE main_Loop()
    IMPLICIT NONE
    INTEGER :: i
    DO i = 1, niter
       CALL do_work()
       IF (num_proc .GT. 1) CALL send_messages()
    ENDDO
  END SUBROUTINE Main_Loop

  ! Execute the smoothing algorithm
  SUBROUTINE do_work()
    IMPLICIT NONE
    INTEGER :: i, j, k
    ! Simple Smoothing operation
    DO j = 2, nylocal-1
       DO i = 2, nxglobal-1
          df(i,j) = 0.25 * ( f(i+1,j) + f(i-1,j) + f(i,j+1) + f(i,j-1) )
       ENDDO
    ENDDO
    DO j = 2, nylocal-1
       DO i = 2, nxglobal-1
          f(i,j) = df(i,j)
       ENDDO
    ENDDO
  END SUBROUTINE Do_Work

  ! Waitall 
  SUBROUTINE IWaitAll(n,irq)
    INTEGER :: irq(:)
    INTEGER, INTENT(In) :: n
    INTEGER :: mpi_err
    INTEGER, ALLOCATABLE :: istat(:,:)
    ALLOCATE(istat(MPI_STATUS_SIZE,1:n))
    CALL MPI_WAITALL(n,irq,istat,mpi_err)
    DEALLOCATE(istat)
  END SUBROUTINE IWaitAll

  ! Finalize the program and end MPI
  SUBROUTINE Finalize()
    IMPLICIT NONE
    INTEGER :: ierr
    IF (ALLOCATED(    f)) DEALLOCATE(    f) 
    IF (ALLOCATED(   df)) DEALLOCATE(   df) 
    IF (ALLOCATED(ftemp)) DEALLOCATE(ftemp) 
    CALL MPI_Finalize(ierr)
  END SUBROUTINE Finalize

  ! send data to your neighbours
  SUBROUTINE Send_Messages()
    IMPLICIT NONE
    INTEGER :: irqs(1:4), ierr1, ierr2, ierr3, ierr4
    CALL MPI_ISEND(f(1,2), nxglobal, MPI_DOUBLE_PRECISION, myleft, 1, MPI_COMM_WORLD, irqs(1), ierr1)
    CALL MPI_ISEND(f(1,nylocal+1), nxglobal, MPI_DOUBLE_PRECISION, myright, 2, MPI_COMM_WORLD, irqs(2), ierr2)
    CALL MPI_IRECV(f(1,1), nxglobal, MPI_DOUBLE_PRECISION,myleft, 2, MPI_COMM_WORLD, irqs(3), ierr3)
    CALL MPI_IRECV(f(1,2), nxglobal, MPI_DOUBLE_PRECISION, myright,1,MPI_COMM_WORLD, irqs(4), ierr4)

    CALL IWaitAll(4,irqs)
  END SUBROUTINE Send_Messages

  ! get the command line arguments
  SUBROUTINE grab_args(numx, numy, numiter)
    IMPLICIT NONE
    INTEGER, INTENT(INOUT)   :: numx
    INTEGER, INTENT(INOUT)   :: numy
    INTEGER, INTENT(INOUT)   :: numiter
    INTEGER :: n                    ! Number of command-line arguments
    INTEGER :: i                    
    CHARACTER(len=1024) :: argname  ! Argument key
    CHARACTER(len=1024) :: val      ! Argument value
    n = command_argument_COUNT()
    DO i=1,n,2
       CALL get_command_ARGUMENT(i, argname)
       CALL get_command_ARGUMENT(i+1, val)
       SELECT CASE(argname)
       CASE('-nx')
          READ(val, '(I8)') numx
       CASE('-ny')
          READ(val, '(I8)') numy
       CASE('-nt')
          READ(val, '(I8)') numiter
       CASE DEFAULT
          WRITE(output_unit,'(a)') ' '
          WRITE(output_unit,'(a)') &
               ' Unrecognized option: '// TRIM(argname)
       END SELECT
    ENDDO
  END SUBROUTINE grab_args

END PROGRAM Main
