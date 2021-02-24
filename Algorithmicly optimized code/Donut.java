import java.util.Scanner;
import java.util.Random;


public class Donut {
    //data set used for evaluating distance more easily
    public static class intersection {
        int x;
        int y;
        intersection(int xvalue, int yvalue){
            x=xvalue;
            y=yvalue;
        }

    }
    //uses manhatan distance to ditermine how far one point is from another
    public static int calclualteDistance(intersection point1, intersection point2){
        int yDistance=0;
        int xDistance=0;
        if(point1.x>point2.x){
            xDistance=point1.x-point2.x;
        }else{
            xDistance=point2.x-point1.x;
        }
        if(point1.y>point2.y){
            yDistance=point1.y-point2.y;
        }else{
            yDistance=point2.y-point1.y;
        }
        return xDistance+yDistance;
    }
    public static int findMedianQuickSelect(int[] numbarray){
        if (numbarray.length%2==1){
            return quickSelectPivot(numbarray,numbarray.length/2);
        }else{
            return (quickSelectPivot(numbarray,numbarray.length/2-1)
                    +quickSelectPivot(numbarray,numbarray.length/2))/2;
        }
    }

    public static int quickSelectPivot(int[]numbarray,int index){
        //if we get passed an array one element long
        if (numbarray.length==1){
            return numbarray[0];
        }
        Random rand=new Random();
        //pick a random number from our index
        int pivot=rand.nextInt(numbarray.length-1);
        int lowNumber=0;
        int highNumber=0;
        int pivots=0;
        //sort though the array to find how close we were
        for(int x=0;x<numbarray.length;x++){
            if(numbarray[pivot]<numbarray[x])
                lowNumber++;
            else {
                if (numbarray[x] < numbarray[pivot])
                    highNumber++;
                else
                    pivots++;
            }
        }
        int []lowerThanPivot=new int[lowNumber];
        int []higherThanPivot=new int[highNumber];
        int []pivotPoints=new int[pivots];
        lowNumber=0;
        highNumber=0;
        pivots=0;
        //alocate the new arrays we need (note if you want to improve speed futher, this part can be opimized)
        for(int x=0;x<numbarray.length;x++) {
            if (numbarray[pivot] < numbarray[x]) {
                lowerThanPivot[lowNumber] = numbarray[x];
                lowNumber++;
            } else {
                if (numbarray[x] < numbarray[pivot]) {
                    higherThanPivot[highNumber] = numbarray[x];
                    highNumber++;
                } else {
                    pivotPoints[pivots] = numbarray[x];
                    pivots++;
                }
            }
        }
            if(index<lowerThanPivot.length){
                //median lower, try again
                return quickSelectPivot(lowerThanPivot,index);
            }else{
                if(index<lowerThanPivot.length+pivotPoints.length){
                    //this point is the median, return it
                    return pivotPoints[0];
                }else{
                    //median is higher, try again
                    return quickSelectPivot(higherThanPivot,index-lowerThanPivot.length-pivotPoints.length);
                }
            }

        }

    public static void main(String args[]){
        //gathers data from user
        Scanner kb=new Scanner(System.in);
        int n=kb.nextInt();
        int []ypoints=new int [n];
        int []xpoints=new int [n];
        int x=0;
        int y=0;
        //data set used for storing all points for latter when we evaluate distance
        intersection[] cityPlan=new intersection[n];
        for(int m=0;m<n;m++){
            //gathers
            xpoints[m]=kb.nextInt();
            ypoints[m]=kb.nextInt();
            cityPlan[m]=new intersection(xpoints[m],ypoints[m]);
        }
        //the median of x and y will be the point closest to all of the points we are given
        int bestX=findMedianQuickSelect(xpoints);
        int bestY=findMedianQuickSelect(ypoints);
        intersection finalpoint=new intersection(bestX,bestY);
        int totaldistance=0;
        for(int m=0;m<n;m++){
            //evaluates the distance of all of our points
            totaldistance+=calclualteDistance(finalpoint,new intersection(xpoints[m],ypoints[m]));
        }
        System.out.println(totaldistance);
    }
}
