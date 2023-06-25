//-------------------------------------------------------------------------------------
// Alec G Thilenius - Alec.Thilenius@Colorado.EDU
//
// This software is distributed under the MIT License, available at the following URL:
// http://www.opensource.org/licenses/mit-license.php
//-------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------

// Abstract:
// A simple unit testing framework designed to be bundled with homework assignments.
// The framework itself (UTFramework.h and UTFramework.cpp) should not be edited by
// students.

// Supported:
//	- Window ( X86 / AMD64 )
//	- Linux
//	- std::exception catching
//	- unknown exception catching
//	- Segmentation Fault catching
//		- Not SegFault catching via POSIX handler. Must be a POSIX compatible system.

// Planned:
//	- Threaded timeout assertions

// Example usage:
/*

	#include "UTFramework.h"
	using namespace Thilenius;

	SUITE_BEGIN("Hello Suite!")

	TEST_BEGIN("Hello Test One!")
	{
		UTFramework::IsTrue("One Equals One.", 1 == 1, "This shows if 1 != 1");
		UTFramework::IsTrue("SegFaulting for fun...", true, "");
		*((int*)0) = 4;
	}TEST_END

	TEST_BEGIN("Hello Test Two!")
	{
		UTFramework::IsTrue("Throwing STD::Exception...", true, "");
	}TEST_END

	SUITE_END


	int main ()
	{
		UTFrameworkInit;
	}
*/
//-------------------------------------------------------------------------------------
#ifndef UTFRAMEWORK_H
#define UTFRAMEWORK_H

#include <string>
#include <sstream>
#include <signal.h>
#include <iostream>

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32)
	// Windows
	#include <Windows.h>
	#include <iostream>

#else
	// Linux
	#include <stdlib.h>
#endif

using namespace std;

namespace Thilenius
{
	enum ConsoleColor { White, Red, Yellow, Green, Blue };

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
		static void FaultException ( std::exception exeption );
		static void UnknownExHandler ( );

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
		static int m_retroMode;

	};

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
#define SUITE_BEGIN(SuiteName)			\
	void UTRunAll () \
	{ \
	  UTFramework::StartSuite( SuiteName );	\
	if ( false ){ } \

#define SUITE_END \
		else \
	{ \
	UTFramework::EndSuite(); \
	} \
	} \
	void PosixSegFault(int signum) \
	{ \
	if ( UTFramework::IsTesting ( ) ) \
	{ \
	signal(SIGSEGV, PosixSegFault); \
	UTFramework::SegFaultRecovery(); \
	UTRunAll(); \
	} \
	signal(signum, SIG_DFL); \
	exit(3); \
	} \

#define TEST_BEGIN(TestName) \
	else if ( UTFramework::StartTest ( TestName ) ) \
	{ \
	try \
	{ \

#define TEST_END \
	} \
	catch (const std::exception& ex) { UTFramework::FaultException(ex); } \
	catch (...) { UTFramework::UnknownExHandler(); } \
	UTFramework::EndTest(); \
	UTRunAll (); \
	} \

#define UTFrameworkInit	\
	signal(SIGSEGV, PosixSegFault); \
	UTRunAll(); \

	inline void IsTrue ( std::string testName, bool result, std::string message )
	{
		UTFramework::IsTrue(testName, result, message);
	}

	inline void Error ( std::string testName, std::string message )
	{
		UTFramework::Fail(testName, message);
	}

}

#endif
