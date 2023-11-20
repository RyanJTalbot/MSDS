
!////////////////////////////////////////////////////////////////////////////////
!   Timing Program
!   usage:
!           ./program -nt T
!           T:   number of iterations to run for (default = 1000)
!
!   description:
!           Computes a[1:nx] = -a[1:nx] T times, for array length nx (= 10256)
!           Reports time
!           Reports time per interation
program main
  use iso_fortran_env, only : output_unit, real64

  implicit none

  !//////////////////////////////
  ! Timing variables
  integer :: t1, t2, count_rate, count_max, i, j
  real(real64)  :: elapsed_time

  integer, parameter :: opu=output_unit
  real(real64), allocatable :: a(:)
  real(real64), allocatable :: r(:)


  !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  !   Problem Control Parameters
  integer :: niter = 1000
  integer :: nx = 10256
  !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  call grab_args(niter)
  allocate(a(nx))
  allocate(r(nx))
  
  a(1:nx) = 1.0

  write(opu,*)'looping ', niter,' times.'

  call system_clock(t1, count_rate, count_max)
  do j = 1, niter
     do i = 1, nx
        r(i) = -a(i)
     enddo
  enddo

  call system_clock(t2, count_rate, count_max)
  elapsed_time = real(t2-t1) / real(count_rate)

  write(opu,*)'Elapsed time: ', elapsed_time
  write(opu,*)'Elapsed time per iteration: ', elapsed_time / niter

  deallocate(a)
  deallocate(r)

contains

  subroutine grab_args(numiter)
    implicit none

    integer, intent(inout)   :: numiter

    integer :: n                    ! Number of command-line arguments
    integer :: i
    character(len=1024) :: argname  ! Argument key
    character(len=1024) :: val      ! Argument value

    n = command_argument_count()
    do i=1,n,2
       call get_command_argument(i, argname)
       call get_command_argument(i+1, val)
       select case(argname)
       case('-nt')
          read(val, '(i8)') numiter
       case default
          write(output_unit,'(a)') ' '
          write(output_unit,'(a)') &
               ' Unrecognized option: '// trim(argname)
       end select
    enddo

  end subroutine grab_args


end program main
