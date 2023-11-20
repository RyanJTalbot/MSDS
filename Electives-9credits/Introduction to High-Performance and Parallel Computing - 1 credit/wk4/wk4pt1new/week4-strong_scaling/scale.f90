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
Program Main
    USE ISO_FORTRAN_ENV, ONLY : output_unit
    USE MPI 
    IMPLICIT NONE
    Character*8 :: rank_string, nproc_string
    Character(MPI_MAX_PROCESSOR_NAME) :: node_name
    Integer :: ierr, num_proc, my_rank, name_len
    Real*8 :: loop_end, loop_start, ticklen
    Real*8, Allocatable :: f(:,:), df(:,:), ftemp(:,:)
    Integer :: myleft, myright ! processor id's to "left" and "right"
    Integer :: nylocal  ! Number of y-points stored locally
    !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    !   Problem Control Parameters
    Integer :: niter = 100
    Integer :: nyglobal = 4096
    Integer :: nxglobal = 1024 
    !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    !Initialize MPI  (ierr is an error flag with nonzero value if there's a problem)
    Call MPI_INIT( ierr )
    !Find number of MPI processes executing this program (num_proc)
    Call MPI_Comm_size(MPI_COMM_WORLD, num_proc,ierr)
    !Find this process's rank (my_rank; unique numeric identifier for each MPI process)
    Call MPI_Comm_rank(MPI_COMM_WORLD, my_rank,ierr)
    ! Find the name of this node (node_name)
    Call MPI_Get_processor_name(node_name, name_len,ierr)
    !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ! Define left and right neighbors
    myright = MOD(my_rank+1,num_proc)
    myleft  = MOD(my_rank-1,num_proc)
    If (myleft .eq. -1) myleft =num_proc-1
    If (myright >= num_proc) myright = 0
    !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Call grab_args(nxglobal, nyglobal, niter)
    Call Initialization()
    loop_start = MPI_Wtime()
    Call Main_Loop()
    loop_end = MPI_Wtime()
    ! Print out some information regarding the time and problem size
    If (my_rank .eq. 0) Then
        Write(output_unit, '(i6,e12.3,i6,i6,i6)') &
        & num_proc, loop_end-loop_start, nxglobal, nyglobal, niter
    Endif
    Call Finalize()
Contains
    SUBROUTINE grab_args(numx, numy, numiter)
            IMPLICIT NONE
            INTEGER, INTENT(INOUT)   :: numx
            INTEGER, INTENT(INOUT)   :: numy
            INTEGER, INTENT(INOUT)   :: numiter
            INTEGER :: n                    ! Number of command-line arguments
            INTEGER :: i                    
            CHARACTER(len=1024) :: argname  ! Argument key
            CHARACTER(len=1024) :: val      ! Argument value
            n = command_argument_count()
            DO i=1,n,2
                    CALL get_command_argument(i, argname)
                    CALL get_command_argument(i+1, val)
                    SELECT CASE(argname)
                            CASE('-nx')
                                    read(val, '(I8)') numx
                            CASE('-ny')
                                    read(val, '(I8)') numy
                            CASE('-nt')
                                    read(val, '(I8)') numiter
                            CASE DEFAULT
                                    WRITE(output_unit,'(a)') ' '
                                    WRITE(output_unit,'(a)') &
                                    ' Unrecognized option: '// trim(argname)
                    END SELECT
            ENDDO
    END SUBROUTINE grab_args
    Subroutine Initialization()
        Implicit None
        Integer :: modcheck
        nylocal = nyglobal/num_proc


        modcheck = Mod(nxglobal, num_proc)
        If (my_rank .lt. modcheck) nylocal = nylocal+1
        Allocate(    f( 1:nxglobal , 1:nylocal+2 ))
        Allocate(   df( 1:nxglobal , 1:nylocal+2 ))
        Allocate(ftemp( 1:nxglobal , 1:nylocal+2 ))
        f = 0
        df = 0
        ftemp =0
    End Subroutine Initialization
    Subroutine Main_Loop()
        Implicit None
        Integer :: i
        Do i = 1, niter
            Call Do_Work()
            If (num_proc .gt. 1) Call Send_Messages()
        Enddo
    End Subroutine Main_Loop
    Subroutine Do_Work()
        Integer :: i, j, k
        ! Simple Smoothing operation
        Do j = 2, nylocal-1
            Do i = 2, nxglobal -1
                df(i,j) = 0.25 * ( f(i+1,j) + f(i-1,j) + f(i,j+1) + f(i,j-1) )
            Enddo
        Enddo
        Do j = 2, nylocal-1
            Do i = 2, nxglobal-1
                f(i,j) = df(i,j)
            Enddo
        Enddo
    End Subroutine Do_Work
    Subroutine IWaitAll(n,irq)
        Integer :: irq(:)
        Integer, Intent(In) :: n
        Integer :: mpi_err
        Integer, Allocatable :: istat(:,:)
        Allocate(istat(MPI_STATUS_SIZE,1:n))
        Call MPI_WAITALL(n,irq,istat,mpi_err)
        DeAllocate(istat)
    End Subroutine IWaitAll
    Subroutine Finalize()
        Implicit None
        Integer :: ierr
        If (Allocated(    f)) DeAllocate(    f) 
        If (Allocated(   df)) DeAllocate(   df) 
        If (Allocated(ftemp)) DeAllocate(ftemp) 
        Call MPI_Finalize(ierr)
    End Subroutine Finalize


    Subroutine Send_Messages()
        Implicit None
        Integer :: irqs(1:4), ierr1, ierr2, ierr3, ierr4
        Call MPI_ISEND(f(1,2), nxglobal, MPI_DOUBLE_PRECISION, myleft, 1, MPI_COMM_WORLD, irqs(1), ierr1)
        Call MPI_ISEND(f(1,nylocal+1), nxglobal, MPI_DOUBLE_PRECISION, myright, 2, MPI_COMM_WORLD, irqs(2), ierr2)
        Call MPI_IRECV(f(1,1), nxglobal, MPI_DOUBLE_PRECISION,myleft, 2, MPI_COMM_WORLD, irqs(3), ierr3)
        Call MPI_IRECV(f(1,2), nxglobal, MPI_DOUBLE_PRECISION, myright,1,MPI_COMM_WORLD, irqs(4), ierr4)
        
        Call IWaitAll(4,irqs)
    End Subroutine Send_Messages
End Program Main
