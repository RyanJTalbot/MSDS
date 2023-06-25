
// Note on the PriorityQueueTest:
//
// You really only need to do two things:
//
// 1. Search/replace PriorityQueueTest with the name of your test.
//
// 2. Implement a bunch of functions that start with test and end with
// the name of the test you want. The names should match those
// provided in ../description-common.json. For example if a test is
// FooThingWorks, your test function should be testFooThingWorks.
//
// Nothing else is required as long as you attach the RetroPrinter to
// your test runner.

import org.junit.Test;
import org.junit.Before;
import static org.junit.Assert.*;
import org.junit.runner.JUnitCore;

public class PriorityQueueTest {

    public static void main(String[] args) {
	JUnitCore core= new JUnitCore();
	core.addListener(new RetroPrinter());
	core.run(PriorityQueueTest.class);
    }

    @Test 
    public void testEverything() {
	PriorityQueue queue = new PriorityQueue();
	String text = "Cat Video";
	queue.insert(text, 3);
	text = queue.peek();
	assertTrue(text.equals("Cat Video"));
	text = "RTS Game Packet";
	queue.insert(text, 10);
	text = queue.peek();
	assertTrue(text.equals("RTS Game Packet"));
	text = "PingAlive";
	queue.insert(text, 2);
	text = queue.peek();
	assertTrue(text.equals("RTS Game Packet"));
	text = "Medical Packet";
	queue.insert(text, 11.5f);
	text = queue.peek();
	assertTrue(text.equals("Medical Packet"));  
	text = "Medical Packet";
	queue.insert(text, 12.5f);
	text = queue.peek();
	assertTrue(text.equals("Medical Packet"));  
	text = "Cat Video";
	queue.insert(text, 3);
	text = queue.peek();
	assertTrue(text.equals("Medical Packet"));
	// the PQ table should look like this:
	// 2    Ping Alive
	// 3    Cat Video
	// 3    Cat Video
	// 10   RTS Game Packet
	// 11.5 Medical Packet
	// 12.5 Medical Packet
	text = queue.remove();
	assertTrue("Remove OK", text.equals("Medical Packet"));
	text = queue.peek();
	assertTrue(text.equals("Medical Packet"));
	text = queue.remove();
	assertTrue("Remove OK", text.equals("Medical Packet"));
	text = queue.peek();
	assertTrue(text.equals("RTS Game Packet"));  
	text = queue.remove();
	assertTrue("Remove OK", text.equals("RTS Game Packet"));  
	text = queue.remove();
	assertTrue("Remove OK", text.equals("Cat Video"));  
	text = queue.remove();
	assertTrue("Remove OK", text.equals("Cat Video"));  
	text = queue.remove();
	assertTrue("Remove OK", text.equals("PingAlive"));
    }


}
