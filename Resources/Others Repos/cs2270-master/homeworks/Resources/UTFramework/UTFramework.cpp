//-------------------------------------------------------------------------------------
// Alec G Thilenius - Alec.Thilenius@Colorado.EDU
//
// This software is distributed under the MIT License, available at the following URL:
// http://www.opensource.org/licenses/mit-license.php
//-------------------------------------------------------------------------------------
#include "UTFramework.h"

namespace Thilenius
{
	//===============================     Static Initializations   ==============================
	string UTFramework::m_currentSuite = "";
	string UTFramework::m_currentTest = "";

	bool UTFramework::m_testFault = false;
	bool UTFramework::m_suiteFault = false;

	int UTFramework::m_maxDepth = 0;
	int UTFramework::m_currentDepth = 0;
	RunningMode UTFramework::m_mode = Normal;

	UTFramework::UTFramework(void)
	{
	}

	void UTFramework::StartSuite( std::string suiteName )
	{
		if ( m_currentSuite == suiteName )
			return;

		PrintIndent(0);
		m_currentSuite = suiteName;
		m_currentTest = "";

		m_suiteFault = false;
		m_testFault = false;

		m_maxDepth = 0;
		m_currentDepth = 0;

		PrintLine("Suite: " + suiteName, 0, Blue);
	}

	void UTFramework::EndSuite()
	{
		PrintIndent(1);

		if ( m_suiteFault )
			PrintLine( "Failed!", 0, Red );
		else
			PrintLine( "Passed.", 0, Green );

		m_testFault = false;
		m_suiteFault = false;

		m_currentSuite = "";
		m_currentTest = "";

		// Reset Depth information
		m_maxDepth = 0;
		m_currentDepth = 0;
	}

	bool UTFramework::StartTest( std::string testName )
	{
		if ( m_currentDepth < m_maxDepth )
		{
			m_currentDepth++;
			return false;
		}

		PrintIndent(1);

		PrintLine( "Test: " + testName, 1, Blue );
		m_currentTest = testName;
		m_testFault = false;

		// Track new depth
		m_maxDepth ++;
		m_currentDepth = 0;

		return true;
	}

	void UTFramework::EndTest()
	{
		if ( m_currentTest == "" )
			return;

		if ( m_testFault ) 
		{
			if (m_mode == RetroMode) 
			{
				cout << "RetroGrade Result >\t" 
					<< m_currentTest << ": -" << endl;
			}
			PrintLine( "Failed!", 1, Red );

		} 
		else 
		{
			if (m_mode == RetroMode) 
			{
				cout << "RetroGrade Result >\t" 
					<< m_currentTest << ": +" << endl;
			}
			PrintLine( "Passed.", 1, Green );

		}
		m_currentTest = "";
		m_testFault = false;
	}

	void UTFramework::IsTrue( std::string name, bool result, std::string message )
	{
		if ( result )
		{
			PrintLine( "- " + name, 2, Green );
		}
		else
		{
			PrintLine( "- " + name, 2, Red );
			PrintLine( message, 3, Yellow );
			m_testFault = true;
			m_suiteFault = true;
		}
	}

	void UTFramework::Fail( std::string name, std::string message )
	{
		PrintLine( "- " + name, 2, Red );
		PrintLine( message, 3, Yellow );
		m_testFault = true;
		m_suiteFault = true;
	}


	void UTFramework::SegFaultRecovery()
	{
		PrintLine( "- SEG-FAULT!", 2, Red );
		PrintLine( "You are likely trying to de-reference a NULL pointer.", 3, Red );
		PrintLine( "Attempting to recover...", 3, Red );
		m_testFault = true;
		m_suiteFault = true;

		EndTest();

		// Let the POSIX handler call the next depth of tests
	}

	void UTFramework::FaultException( const std::exception& exeption )
	{
		PrintLine( "- Exception!", 2, Red );
		PrintLine( "Your function raised an exception during execution:", 3, Yellow );
		PrintLine( exeption.what(), 3, Yellow );
		m_testFault = true;
		m_suiteFault = true;

		EndTest();
	}

	void UTFramework::UnknownExHandler()
	{
		PrintLine( "- Exception!", 2, Red );
		PrintLine( "Your function raised an unknown exception type.", 3, Yellow );
		m_testFault = true;
		m_suiteFault = true;

		EndTest();
	}

	void UTFramework::TimeoutFault ( )
	{
		PrintLine( "- Timeout!", 2, Red );
		PrintLine( "Your function likely has an infinite loop in it.", 3, Yellow );
		m_testFault = true;
		m_suiteFault = true;

		EndTest();
	}
	
	void UTFramework::SetMode( RunningMode mode )
	{
		m_mode = mode;
	}

	bool UTFramework::IsTesting()
	{
		if ( m_currentSuite != "" )
			return true;

		return false;
	}

	void UTFramework::Print( std::string message, int indentLevel, ConsoleColor color )
	{
		if (m_mode == Normal) 
		{
			SetColor(Blue);
			for ( int i = 0; i < indentLevel; i++ )
			{
				cout << "|   ";
			}

			SetColor(color);
			cout << message;

			SetColor(White);
		}
	}

	void UTFramework::PrintLine( std::string message, int indentLevel, ConsoleColor color )
	{
		if (m_mode == Normal) 
		{
			Print(message, indentLevel, color);
			cout << endl;
		}
	}

	void UTFramework::PrintIndent( int indentLevel )
	{
		if (m_mode == Normal) 
		{
			SetColor(Blue);
			for ( int i = 0; i < indentLevel; i++ )
			{
				cout << "|   ";
			}
			cout << endl;
			SetColor(White);
		}
	}

	// Not that there is a Windows/Linux switch here. Windows gets a handle to
	// the console, and Linux sends string encoded commands.
	void UTFramework::SetColor( ConsoleColor color )
	{

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32)
		//Windows

		switch ( color )
		{
		case White:
			//HANDLE hStdout = GetStdHandle(STD_OUTPUT_HANDLE); 
			SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 
				FOREGROUND_RED|FOREGROUND_GREEN|FOREGROUND_BLUE);
			break;

		case Red:
			//HANDLE hStdout = GetStdHandle(STD_OUTPUT_HANDLE); 
			SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 
				FOREGROUND_RED|FOREGROUND_INTENSITY);
			break;

		case Yellow:
			//HANDLE hStdout = GetStdHandle(STD_OUTPUT_HANDLE); 
			SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 
				FOREGROUND_GREEN|FOREGROUND_RED|FOREGROUND_INTENSITY);
			break;

		case Green:
			//HANDLE hStdout = GetStdHandle(STD_OUTPUT_HANDLE); 
			SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 
				FOREGROUND_GREEN|FOREGROUND_INTENSITY);
			break;

		case Blue:
			//HANDLE hStdout = GetStdHandle(STD_OUTPUT_HANDLE); 
			SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_BLUE
				|FOREGROUND_GREEN|FOREGROUND_INTENSITY);
			break;
		}

#else
		// Linux

		switch ( color )
		{
		case White:
			std::cout << "\033[0m";
			break;

		case Red:
			std::cout << "\033[31m";
			break;

		case Yellow:
			std::cout << "\033[33m";
			break;

		case Green:
			std::cout << "\033[32m";
			break;

		case Blue:
			std::cout << "\033[36m";
			break;
		}
#endif
	}
	
	//===========================================================================================
	//=============================== Free Function  Declarations  ==============================
	//===========================================================================================
	void PosixSegFault(int signum)
	{
		if ( UTFramework::IsTesting ( ) )
		{
			signal(SIGSEGV, PosixSegFault);
			UTFramework::SegFaultRecovery();
			Thilenius::TestingFunction( );
		}
		else
			signal(signum, SIG_DFL);
	}

	bool isThreadFinished = false;

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32)
	// WINDOWS. Reduced functionality.

	void ForkThread ( )
	{
		// Single threaded
		signal(SIGSEGV, PosixSegFault);
		TestingFunction( );
	}

#else
	// LINUX POSIX Threading ( Not supported on VC++ )
	// Yes I can use WINThreads. The POSIX SIGSEGV handler will
	// not catch a SIGSEG on a non-UI thread though.

	unsigned int get_ticks()
	{
	  struct timeval tv;

	  gettimeofday(&tv, NULL);
	  return (tv.tv_usec/1000 + tv.tv_sec * 1000);
	}

	void* PosixThreadFork ( void* )
	{
		signal(SIGSEGV, PosixSegFault);
		
		TestingFunction( );
		
		isThreadFinished = true;
		return (void*) 0;
	}

	void ForkThread ( )
	{
		pthread_t threadHandle;
		unsigned int startTime = get_ticks();
		
		pthread_create( &threadHandle, NULL, PosixThreadFork, NULL );
		
		while ( (get_ticks() - startTime ) < RUN_TIMEOUE )
		{
			if (isThreadFinished == true)
				break;
			
			usleep(10 * 1000);
		}
		
		if (isThreadFinished == false)
		{
			//DEBUG_INFO ( "Threads timed out." );
			
			// Kill the threads
			pthread_cancel(threadHandle);
			
			UTFramework::TimeoutFault();
			ForkThread ( );
		}
		else
		{
			//DEBUG_INFO ( "Threads Done." );
		}

		pthread_join(threadHandle, NULL);
	}

#endif
	


}
