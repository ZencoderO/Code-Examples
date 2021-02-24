import java.util.Scanner;
public class Planters {


   public static class allPots {
       //places to hold the data we are given by the user
        int[] fullPots;
        int[] sparePots;
        //int to track what pots we can use
        int fullPotsAccessable;
        int sparePotsAccessable;
        //constructor for allPots
        allPots(int[] full, int[] spare) {
            fullPots = full;
            sparePots = spare;
            fullPotsAccessable=fullPots.length-1;
            sparePotsAccessable=sparePots.length-1;
        }
        //function that finds if we can transfer the flowers successfully
        boolean canTranspher() {
            //checks to see if we have a spare pot larger than our largest occupied pot, if we don't it returns false
            if (sparePotsAccessable>-1 && sparePots[sparePotsAccessable] >= (fullPots[fullPotsAccessable] + 1) ) {
                sparePotsAccessable--;
            }else{
                return false;
            }
            //runing time should be O(n) for this part
            for (int i = fullPotsAccessable-1; i > 0; i--) {
                //checks to see if there are any spare pots left to use
                if (sparePotsAccessable > -1) {
                    //want to use smallest ones we can frist
                    if (sparePots[sparePotsAccessable] >= fullPots[fullPotsAccessable]) {
                        //checks spares to see if we have somthing of the correct size
                        if (sparePots[sparePotsAccessable] >= (fullPots[i] + 1)) {
                            sparePotsAccessable--;
                        } else {
                            //same with fulls
                            if (fullPots[fullPotsAccessable] >= fullPots[i] + 1) {
                                fullPotsAccessable--;
                            } else {
                                //if both do not work returns false
                                return false;
                            }
                        }
                    } else {
                        //does the same thing but checks in reverse
                        if (fullPots[fullPotsAccessable] >= (fullPots[i] + 1)) {
                            fullPotsAccessable--;
                        } else {
                            if (sparePots[sparePotsAccessable] >= fullPots[i] + 1) {
                                sparePotsAccessable--;
                            } else {
                                return false;
                            }
                        }
                    }
                }else{
                    //does the same thing but only checks the array of Pots that were full
                    if (fullPots[fullPotsAccessable] >= (fullPots[i] + 1)) {
                        fullPotsAccessable--;
                    } else {return false;}
                }

                }
                return true;
            }

    }
    //reuse of mergesort used in HW0
    public static int[] mergeSort(int[] x) {
       //if length is 0 we have fully subdevided the array, if not we move to sort the havlfs we have
        if(x.length>1) {
            //assign values repersenting the middle front and back of the array
            int frist = 0;
            int last = x.length;
            int middle = (last) / 2;

            int[] fronthalf=new int[middle];
            //create a front have to pass to the recursive call
            for(int t=0; t<middle; t++){
                fronthalf[t]=x[t];
            }
            //create a back half to pass to the recursive call
            int[] backhalf=new int[last-middle];
            for(int t=0; t<last-middle; t++){
                backhalf[t]=x[t+middle];
            }
            //make a recersive call to create a sorted front and back of the array
            int[] sortedFront=mergeSort(fronthalf);
            int[] sortedBack=mergeSort(backhalf);
            //j will be the point we are in on the sorted front
            int j=0;
            //m will be the point we are in on the sorted back
            int m=0;
            //k will be the point we are in in the fully sorted array we are making
            int k=0;
            while(j<sortedFront.length && m<sortedBack.length) {
                //if the value at the front of the sorted front is smaller we put it in the array and increment to the
                //next point in the array
                if (sortedFront[j] <= sortedBack[m]) {
                    x[k]=sortedFront[j];
                    j++;
                    k++;
                } else {
                    //if it is not we do the same thing but with the back
                    x[k]=sortedBack[m];
                    m++;
                    k++;
                }
            }
            //here we put in whatever was larger than elements in the oppsite array at the end
            while(j<sortedFront.length) {
                x[k]=sortedFront[j];
                j++;
                k++;
            }
            while(m<sortedBack.length) {
                x[k]=sortedBack[m];
                m++;
                k++;
            }

        }
        //we return the sorted array
        return x;

    }

    public static void main(String args[]){
       //gathers data from user on size of arrays
        Scanner kb=new Scanner(System.in);
        int[] currentplants=new int[kb.nextInt()];
        int[] spareplants=new int[kb.nextInt()];
        //gathers info to put in arrays
        for(int i=0;i<currentplants.length;i++){
            currentplants[i]=kb.nextInt();

        }
        for(int i=0;i<spareplants.length;i++){
            spareplants[i]=kb.nextInt();
        }
        //sorts arrays
        int[] sortedCurrentPlants=mergeSort(currentplants);
        int[] sortedSparePlants=mergeSort(spareplants);
        //creates object that can test our sorted arrays
        allPots mypots=new allPots(sortedCurrentPlants,sortedSparePlants);
        //uses our object to test our arrays and outputs accordingly
        if(mypots.canTranspher()==true){
            System.out.println("YES");
        }else{
            System.out.println("NO");
        }



    }

}
