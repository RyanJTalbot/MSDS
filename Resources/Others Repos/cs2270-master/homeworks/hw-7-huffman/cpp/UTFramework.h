//-------------------------------------------------------------------------------------
// Alec G Thilenius - Alec.Thilenius@Colorado.EDU
//
// This software is distributed under the MIT License, available at the following URL:
// http://www.opensource.org/licenses/mit-license.php
//-------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------
// V 1.2.2

// IMPORTANT: You MUST specify -pthread at the end of flags in makefile to compile
// 	      the UTFramework on Linux!

// Abstract:
// A simple unit testing framework designed to be bundled with homework assignments.
// The framework itself (UTFramework.h and UTFramework.cpp) should not be edited by
// students.

// Supported:
//	- Linux
//	- WIN32 VC++ ( Reduced functionality )
//	- Infinite loop detection and recovery
//	- std::exception catching
//	- unknown exception catching
//	- Segmentation Fault catching
//		- Note SegFault catching via POSIX handler. Must be a POSIX compatible system.

// Reduced functionality
//	- Infinite loop detection is disabled in WINDOWS
//	- SegFault handling may not work as intended in VS2012
//-------------------------------------------------------------------------------------

#ifndef UTFRAMEWORK_H
#define UTFRAMEWORK_H

#include <cstring>
#include <string>
#include <sstream>
#include <signal.h>

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32)
	// Windows
	//#include <WinBase.h>
	#include <Windows.h>
	#include <iostream>
#else
	// Linux
	#include <unistd.h>
	#include <stdio.h>
	#include <stdlib.h>
	#include <pthread.h>
	#include <iostream>
	#include <sys/time.h>
	#include <sys/select.h>
#endif

#define RUN_TIMEOUE 5000

using namespace std;

namespace Thilenius
{
	enum ConsoleColor { White, Red, Yellow, Green, Blue };
	enum RunningMode { Normal, RetroMode };
	//===========================================================================================
	//==========================    Testing Framework Class Definition   ========================
	//===========================================================================================
	class UTFramework
	{
	public:
		~UTFramework(void);

		static void StartSuite ( std::string suiteName );
		static void EndSuite ( );

		static bool StartTest ( std::string testName );
		static void EndTest ( );

		static void IsTrue ( std::string name, bool result, std::string message );
		static void Fail ( std::string name, std::string message );

		static void SegFaultRecovery ( );
		static void FaultException ( const std::exception& exeption );
		static void UnknownExHandler ( );
		static void TimeoutFault ( );
		
		static void SetMode( RunningMode mode );

		static bool IsTesting ( );
		static void SetColor ( ConsoleColor color );

	private:
		UTFramework(void);
		UTFramework(UTFramework const&);
		void operator=(UTFramework const&);

		static void Print ( std::string message, int indentLevel, ConsoleColor color );
		static void PrintLine ( std::string message, int indentLevel, ConsoleColor color );
		static void PrintIndent ( int indentLevel );
		

	private:

		static std::string m_currentSuite;
		static std::string m_currentTest;

		static bool m_testFault;
		static bool m_suiteFault;

		static int m_maxDepth;
		static int m_currentDepth;

		static RunningMode m_mode;
	};
	
	
	//===========================================================================================
	//===============================  Free Function  Definitions  ==============================
	//===========================================================================================
	extern void(*TestingFunction)( );
	extern bool isThreadFinished;
	
	void PosixSegFault(int signum);
	unsigned int get_ticks( );
	void* PosixThreadFork ( void* );
	void ForkThread ( );

	//===========================================================================================
	//===============================     Macro Debug Directives   ==============================
	//===========================================================================================
#define DEBUG_INFO(m) \
	UTFramework::SetColor ( Green ); \
	std::cout << "Info    [ " << __FUNCTION__ << " | " << __LINE__ << " ] " << m << std::endl; \
	UTFramework::SetColor ( White ); \

#define DEBUG_ERROR(m) \
	UTFramework::SetColor ( Red ); \
	std::cout << "ERROR   [ " << __FUNCTION__ << " | " << __LINE__ << " ] " << m << std::endl; \
	UTFramework::SetColor ( White ); \


#define DEBUG_WARNING(m) \
	UTFramework::SetColor ( Yellow ); \
	std::cout << "WARNING [ " << __FUNCTION__ << " | " << __LINE__ << " ] " << m << std::endl; \
	UTFramework::SetColor ( White ); \


	//===========================================================================================
	//===============================      Unit Testing Macros     ==============================
	//===========================================================================================
	
	// See UTFramework.cpp for a full expansion.
#define SUITE_BEGIN(SuiteName) \
	void(*Thilenius::TestingFunction)( );\
	void UTRunAll () \
	{ \
	Thilenius::UTFramework::StartSuite( SuiteName ); \
	if ( false ){ } \

#define SUITE_END \
		else \
	{ \
	Thilenius::UTFramework::EndSuite(); \
	} \
	} \

#define TEST_BEGIN(TestName) \
	else if ( Thilenius::UTFramework::StartTest ( TestName ) ) \
	{ \
	try \
	{ \

#define TEST_END \
	} \
	catch (const std::exception& ex) { Thilenius::UTFramework::FaultException(ex); } \
	catch (...) { Thilenius::UTFramework::UnknownExHandler(); } \
	Thilenius::UTFramework::EndTest(); \
	Thilenius::TestingFunction(); \
	} \

#define UTFrameworkInit \
	if (argc == 2 && strcmp(argv[1], "--retrograde") == 0) \
		UTFramework::SetMode(RetroMode); \
	TestingFunction = &UTRunAll; \
	ForkThread( ); \

	inline void IsTrue ( std::string testName, bool result, std::string message )
	{
		Thilenius::UTFramework::IsTrue(testName, result, message);
	}

	inline void Error ( std::string testName, std::string message )
	{
		Thilenius::UTFramework::Fail(testName, message);
	}

}

#endif
