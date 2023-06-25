import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.junit.runner.notification.Failure;
import org.junit.runner.Description;
import org.junit.runner.notification.RunListener;

public class RetroPrinter extends RunListener {

     String currentTestName = "Unknown";
     String status = "?";

     static Pattern pattern = Pattern.compile("^test(\\w+)\\((\\w+)\\)");

     public String extractTestName(String input) {
	 String ret = "Unknown";
	 Matcher m = pattern.matcher(input);
	 if (m.matches()) {
	     ret = m.group(1);
	 }
	 return ret;
     }

     public void reset() { 
	 this.currentTestName = "Unknown";
	 this.status = "?";
     }
     
     public void testStarted(Description desc) {
	 String test = extractTestName(desc.getDisplayName());
	 this.currentTestName = test;
	 this.status = "+";
     }
     public void testFinished(Description desc) {
	 String test = extractTestName(desc.getDisplayName());
	 if (!test.equals(currentTestName)) {
	     System.out.println("Severe error: JUnit listener is out of sync " +
				"with JUnitCore life cycle.");
	 }
	 System.out.println("RetroGrade Result > " + this.currentTestName + ": " + status);
	 reset();
     }
     public void testFailure(Failure failure) {
	 System.out.println("" + failure);
	 this.status = "-";
     }
 }
