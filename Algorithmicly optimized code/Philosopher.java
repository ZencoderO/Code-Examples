//import com.sun.org.apache.xpath.internal.operations.String;

/*
 * Philosopher.java
 *
 * Version:
 *     1
 *
 * Revisions:
 * remove sleep
 * add wait
 * add notify all
 * add/remove chopstick switching
 * add/remove try catch exception handling
 * remove second wait
 * add if statement for first notify all
 * add commenting
 */



import java.util.Random;
import java.util.Vector;

/**
 * Dining philosophers without deadlock.
 * Homework 9.
 *
 *     @author Luke Batchelder
 *     @author Jessica Diehl
 */
public class Philosopher extends Thread {

    protected static Random random = new Random();        // randomize
    protected int me;             	// number for trace
    protected Integer left, right;   	// my chopsticks
    static Object o = new Object();	//lock object for wait queue

    /**
     * Create a single philosopher using an id and left and right.
     *
     * params	me		integer id number
     * params	left	left philosopher
     * params	right	right philosopher
     *
     * return			None
     *
     */
    public Philosopher (int me, Integer left, Integer right) {
        this.me = me; this.left = left; this.right = right;
    }


    /**
     * Philosophers run func, think and eat 100,000
     * times
     *
     * return			None
     *
     */
    public void run () {
        for (int n = 1; n <= 100000; ++ n) {
            System.out.println(me+" thinks");
            try {
                synchronized(o) {
                    //The last philosopher sends all other
                    //philosophers to eat, while waiting.
                    //after eating, the first philosopher
                    //releases the last philosopher.
                    //All other philosophers waits for
                    //the last philosopher to eat.
                    if(me == 4 || me == 0)
                    {
                        o.notifyAll();
                    }
                    o.wait();
                }
                //removed sleep
            } catch(Exception e) {
                e.printStackTrace();
            }
            //try to eat using the left and right chopsticks
            System.out.println(me+" is trying to eat");
            synchronized ( left )  {
                synchronized ( right )  {
                    //removed sleep
                    System.out.println("\t" + me+" eats ");
                }
            }
            System.out.println("\t" + me+" leaves");
        }
        System.out.println("Done Dining.");
    }




    /**
     * Copy a single file from the source folder to the dest folder
     *
     * params	src		Source directory
     * params	dest	Destination directory
     * params	file	file name to be copied
     *
     * return			None
     *
     */
    public static void main (String args [])
    {
        //create new integers
        Integer f[] = new Integer[5];
        for (int n = 0; n < 5; ++ n)
            f[n] = new Integer(n);

        //create new philosophers
        Philosopher p[] = new Philosopher[5];
        p[0] = new Philosopher(0, f[4], f[0]);      // backwards
        for (int n = 1; n < 5; ++ n)
            p[n] = new Philosopher(n, f[n-1], f[n]);

        //start dining
        for (int n = 0; n < 5; ++ n) p[n].start();
    }
}


//code for the homework 9 assignment
//number 1, a good example of
//resource contention