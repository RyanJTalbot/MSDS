//-------------------------------------------------------------------------------------
// Alec G Thilenius - Alec.Thilenius@Colorado.EDU
//
// This software is distributed under the MIT License, available at the following URL:
// http://www.opensource.org/licenses/mit-license.php
//-------------------------------------------------------------------------------------
#include "UTFramework.h"

int RETROGRADE_MODE = 0;

namespace Thilenius
{



	//===============================     Static Initializations   ==============================
	string UTFramework::m_currentSuite = "";
	string UTFramework::m_currentTest = "";

	bool UTFramework::m_testFault = false;
	bool UTFramework::m_suiteFault = false;

	int UTFramework::m_maxDepth = 0;
	int UTFramework::m_currentDepth = 0;
        int UTFramework::m_retroMode = 0; // set to nonzero for retrograde output

	UTFramework::UTFramework(void)
	{
	}

  void UTFramework::StartSuite( std::string suiteName )
	{
		if ( m_currentSuite == suiteName )
			return;

		PrintIndent(0);
		m_currentSuite = suiteName;
		m_retroMode = 0;
#ifdef RETRO_MODE
		m_retroMode = 1;
#endif
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
		
		if ( m_testFault ) {
		  if (RETROGRADE_MODE) {
			cout << "RetroGrade Result >\t" 
			     << m_currentTest << ": -" << endl;
		  }
		  PrintLine( "Failed!", 1, Red );

		} else {
		  if (RETROGRADE_MODE) {
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

	void UTFramework::FaultException( std::exception exeption )
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

	bool UTFramework::IsTesting()
	{
		if ( m_currentSuite != "" )
			return true;

		return false;
	}

	//Deprecated. No need for a singleton instance.
	//UTFramework& UTFramework::GetInstance()
	//{
	//	// C++ Singleton pattern.
	//	static UTFramework instance;
	//	return instance;
	//}

	void UTFramework::Print( std::string message, int indentLevel, ConsoleColor color )
	{
	  if (RETROGRADE_MODE == 0) {
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
	  if (RETROGRADE_MODE == 0) {
		Print(message, indentLevel, color);
		cout << endl;
	  }
	}

	void UTFramework::PrintIndent( int indentLevel )
	{
	  if (RETROGRADE_MODE == 0) {
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

}
