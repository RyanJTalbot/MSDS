import org.junit.Test;
import org.junit.Before;
import static org.junit.Assert.*;
import org.junit.runner.JUnitCore;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class SortingTest {

    public static void main(String[] args) {
	JUnitCore core= new JUnitCore();
	core.addListener(new RetroPrinter());
	core.run(SortingTest.class);
    }

    Random rand;
    Sorting sorting;

    List<Integer> get_random_data(int how_many, int upper_bound) {
	List<Integer> numbers = new ArrayList<Integer>();
	for (int i=0; i < how_many; i++) {
	    int r = rand.nextInt(upper_bound);
	    numbers.add(r);
	}
	return numbers;
    }

    boolean is_nondecreasing(List<Integer> data) {
	boolean ret = true;
	if (data.size() > 1) {
	    int prev = data.get(0);
	    for (int i=1; i < data.size(); i++) {
		int here = data.get(i);
		if (prev > here) {
		    ret = false;
		    break;
		}
		prev = here;
	    }
	}
	return ret;
    }

    @Before
    public void init() {
	rand = new Random(System.currentTimeMillis());
	sorting = new Sorting();
    }

    @Test 
    public void testQuickSort() {
	List<Integer> input_data = get_random_data(1000, 500);
	List<Integer> input_data_orig = new ArrayList<Integer>(input_data);
	int size_before = input_data.size();
	sorting.quicksort(input_data, 0, size_before - 1);

	// check if it is still the right size
	assertEquals(input_data.size(), size_before);

	// check if it contains the same original elements
	assertTrue(input_data.containsAll(input_data_orig));

	// check if it is in nondecreasing order
	assertTrue(is_nondecreasing(input_data));
    }

    @Test 
    public void testBubbleSort() {
	List<Integer> input_data = get_random_data(1000, 500);
	List<Integer> input_data_orig = new ArrayList<Integer>(input_data);
	int size_before = input_data.size();
	sorting.bubblesort(input_data);

	// check if it is still the right size
	assertEquals(input_data.size(), size_before);

	// check if it contains the same original elements
	assertTrue(input_data.containsAll(input_data_orig));

	// check if it is in nondecreasing order
	assertTrue(is_nondecreasing(input_data));
    }

    @Test 
    public void testMergeSort() {
	List<Integer> input_data = get_random_data(1000, 500);
	List<Integer> input_data_orig = new ArrayList<Integer>(input_data);
	int size_before = input_data.size();
	sorting.mergesort(input_data);

	// check if it is still the right size
	assertEquals(input_data.size(), size_before);

	// check if it contains the same original elements
	assertTrue(input_data.containsAll(input_data_orig));

	// check if it is in nondecreasing order
	assertTrue(is_nondecreasing(input_data));

    }

    @Test 
    public void testMysterySort() {
	List<Integer> input_data = get_random_data(1000, 500);
	List<Integer> input_data_orig = new ArrayList<Integer>(input_data);
	int size_before = input_data.size();
	sorting.mystery_sort(input_data);

	// check if it is still the right size
	assertEquals(input_data.size(), size_before);

	// check if it contains the same original elements
	assertTrue(input_data.containsAll(input_data_orig));

	// check if it is in nondecreasing order
	assertTrue(is_nondecreasing(input_data));
    }


}
