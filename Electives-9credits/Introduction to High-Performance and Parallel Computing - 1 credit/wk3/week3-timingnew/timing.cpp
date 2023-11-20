/////////////////////////////////////////////////////////////////////////////////
//   Usage:
//           ./program -nt T
//           T:   number of iterations to run for (default = 100)
//
//   Description:
//           Computes a[0:nx-1] = -a[1:nx] T times, for array length nx (= 10256)
//           Reports time
//
/////////////////////////////////////////////////////////////////////////////////
#include <iostream>
#include <string>
#include <fstream>
#include <ctime>
#include <chrono>		// Using high-resolution timer

using namespace std;

int main(int argc, char** argv) {
    long int niter=1000;
    long int nx=10256;
    string mystr;
    double *a, *r;

    ///////////////////////////////////////
    //  Read command-line parameters -nt
    for (long int i=0; i < argc; i++) {
        mystr=argv[i];
        if (mystr == "-nt"){
            niter=atoi(argv[i+1]);
        }
    }

    cout << "Looping " << niter << " times."   << endl;


    //////////////////////////////////////////
    // Initialize
    a = new double[nx];
    r = new double[nx];
    for (long int i = 0; i < nx; i++) {
      a[i] = (double) i;
    }


    /////////////////////////////
    //  Time loop (computes a[nx] = -a[nx] {niter} times)
    auto tstart = std::chrono::high_resolution_clock::now();
    for (long int j = 0; j < niter; j++) {
      for (long int i = 0; i < nx; i++) {
            r[i] = -a[i];
      }
    }

    auto tend = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::ratio<1, 1> > elapsed = tend - tstart;
    
    delete [] a;
    delete [] r;
    
    cout << "Problem size nx is: " << nx << endl;
    cout << "Elapsed time: " << elapsed.count() << endl;
    cout << "Elapsed time per iteration: " << elapsed.count() / (double) niter << endl;
    cout << "Elapsed time per iteration per point: " <<
      elapsed.count() / (double) niter / (double) nx << endl;
}
