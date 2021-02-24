
import java.math.BigInteger;
import java.util.Scanner;


public class CountIntervals {
    public static class interval {
        int start;
        int end;

        interval(int thisStart, int thisEnd, int totalSets) {
            start = thisStart;
            end = thisEnd;
        }
    }

    public static interval[] mergeSortIntervals(interval[] x) {
        //if length is 0 we have fully subdevided the array, if not we move to sort the havlfs we have
        if (x.length > 1) {
            //assign values repersenting the middle front and back of the array
            int frist = 0;
            int last = x.length;
            int middle = (last) / 2;

            interval[] fronthalf = new interval[middle];
            //create a front have to pass to the recursive call
            for (int t = 0; t < middle; t++) {
                fronthalf[t] = x[t];
            }
            //create a back half to pass to the recursive call
            interval[] backhalf = new interval[last - middle];
            for (int t = 0; t < last - middle; t++) {
                backhalf[t] = x[t + middle];
            }
            //make a recersive call to create a sorted front and back of the array
            interval[] sortedFront = mergeSortIntervals(fronthalf);
            interval[] sortedBack = mergeSortIntervals(backhalf);
            //j will be the point we are in on the sorted front
            int j = 0;
            //m will be the point we are in on the sorted back
            int m = 0;
            //k will be the point we are in in the fully sorted array we are making
            int k = 0;
            while (j < sortedFront.length && m < sortedBack.length) {
                //if the value at the front of the sorted front is smaller we put it in the array and increment to the
                //next point in the array
                if (sortedFront[j].end <= sortedBack[m].end) {
                    x[k] = sortedFront[j];
                    j++;
                    k++;
                } else {
                    //if it is not we do the same thing but with the back
                    x[k] = sortedBack[m];
                    m++;
                    k++;
                }
            }
            //here we put in whatever was larger than elements in the oppsite array at the end
            while (j < sortedFront.length) {
                x[k] = sortedFront[j];
                j++;
                k++;
            }
            while (m < sortedBack.length) {
                x[k] = sortedBack[m];
                m++;
                k++;
            }

        }
        //we return the sorted array
        return x;
    }





        public static void main(String[] args) {
            Scanner kb = new Scanner(System.in);
            int n = kb.nextInt();
            int begin = 0;
            int end = 0;
            interval[] schedual = new interval[n];
            for (int m = 0; m < n; m++) {
                begin = kb.nextInt();
                end = kb.nextInt();
                schedual[m] = new interval(begin, end, n);
            }
            schedual=mergeSortIntervals(schedual);
            BigInteger[] totals=new BigInteger[n];
            totals[0]=new BigInteger("2");
            boolean overlaping=true;
            for (int m=1; m<n; m++) {
                int k = m - 1;
                overlaping=true;
                while (overlaping && k >= 0) {
                    if (schedual[k].end < schedual[m].start) {
                        overlaping = false;
                    } else {
                        k--;
                    }

                }

                if(overlaping){
                    totals[m]=totals[m-1].add(new BigInteger("1"));
                }else {
                    totals[m] = totals[m - 1].add(totals[k]);
                }
            }
        System.out.println(totals[totals.length-1]);
    }

}
