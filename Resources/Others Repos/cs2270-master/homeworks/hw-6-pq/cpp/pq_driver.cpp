//
// pq_driver.cpp
//
// This is an empty unit test file that you can implement (or not) to
// create unit tests for your code.
//
// You'll likely want one for insert, remove, and peek. Try to think
// about how your queue could break, and write tests that help you
// test your deepest priority-queue-related fears.
//
// The test code will appear on RetroGrade late in the game.

#include <string>
#include <iostream>
#include "UTFramework.h"
#include "pq.h"

using namespace Thilenius;

SUITE_BEGIN("Priority Queue")

TEST_BEGIN("Everything")
{
  pq* queue = init_priority_queue();
  string text = "Cat Video";
  insert(queue, text, 3);
  text = peek(queue);
  IsTrue("Peek OK", text == "Cat Video", "Why am I not watching a cat video right now?");
  text = "RTS Game Packet";
  insert(queue, text, 10);
  text = peek(queue);
  IsTrue("Peek OK", text == "RTS Game Packet", "Game Packet Not Found");
  text = "PingAlive";
  insert(queue, text, 2);
  text = peek(queue);
  IsTrue("Peek OK", text == "RTS Game Packet", "Game Packet Not Found");
  text = "Medical Packet";
  insert(queue, text, 11.5);
  text = peek(queue);
  IsTrue("Peek OK", text == "Medical Packet", "Robot surgeon asleep at the wheel?");  
  text = "Medical Packet";
  insert(queue, text, 12.5);
  text = peek(queue);
  IsTrue("Peek OK", text == "Medical Packet", "Robot surgeon asleep at the wheel?");  
  text = "Cat Video";
  insert(queue, text, 3);
  text = peek(queue);
  IsTrue("Peek OK", text == "Medical Packet", "Robot surgeon asleep at the wheel?");
  // the PQ table should look like this:
  // 2    Ping Alive
  // 3    Cat Video
  // 3    Cat Video
  // 10   RTS Game Packet
  // 11.5 Medical Packet
  // 12.5 Medical Packet
  text = remove(queue);
  IsTrue("Remove OK", text == "Medical Packet", "Remove not working");
  text = peek(queue);
  IsTrue("Peek OK", text == "Medical Packet", "Robot surgeon asleep at the wheel?");
  text = remove(queue);
  IsTrue("Remove OK", text == "Medical Packet", "Remove not working");
  text = peek(queue);
  IsTrue("Peek OK", text == "RTS Game Packet", "Game Packet Not Found");  
  text = remove(queue);
  IsTrue("Remove OK", text == "RTS Game Packet", "Remove not working");  
  text = remove(queue);
  IsTrue("Remove OK", text == "Cat Video", "Remove not working");  
  text = remove(queue);
  IsTrue("Remove OK", text == "Cat Video", "Remove not working");  
  text = remove(queue);
  IsTrue("Remove OK", text == "PingAlive", "Remove not working");
}TEST_END


SUITE_END

int main (int argc, char* argv[])
{	
  UTFrameworkInit;
}
