import java.util.Scanner;
//pasword some tables
// need to download an external driver
//project moduels, dependences gives you access to the jar
// Select to_parse From sites
import static java.lang.Integer.parseInt;
/**
 * player creates player needed objects and runs functions needed to progress the game
 * Homework 12.
 *
 *     @author Luke Batchelder
 *     @author Jessica Diehl
 */
public class player {
    HUD readOut= new HUD();
    board battleSpace= new board(readOut);
    grid battleMap= new grid(readOut);
    int crew=6;
    /**
     *creates a player with a board grid and a GUI to make there actions visable
     */
    player(){
        readOut.setupWindow();
        battleSpace.placeShips(crew);
    }
    /**
     *gets a string of proper type from the user
     */
    public String fire() {
        Scanner kb = new Scanner(System.in);
        String fireComand = "";
        boolean ordersCorect = false;
        while (!ordersCorect){
            System.out.println("In the following format what are the x,y corodinates for your shot?");
            fireComand = kb.next();
            try{
                if(fireComand.substring(1,2).equals(",") && Integer.parseInt(fireComand.substring(0,1))<=9 &&
                        Integer.parseInt(fireComand.substring(2))<=9){
                    ordersCorect=true;
                }else{
                    System.out.println("orders unparsable, remember you use numbers lower than 10");
                }

            }catch (Exception e){
                System.out.println("orders unparsable, remember you use numbers lower than 10 and greater than -1");}
        }
        return fireComand;
    }


    /**
     * record the effect of a shot launched by the player and if it conected
     * @param: x x coordinate
     * @param: y y coordinate
     * @param: result 0 for a miss 1 for a hit
     *
     */
    public void fireResults(int x,int y, int results){
        battleMap.recordShotResults(x,y,results);
    }
    /**
     * record the effect of a shot launched by the oppent and if it conected
     * @param: x x coordinate
     * @param: y y coordinate
     * @return result 0 for a miss 1 for a hit
     *
     */
    public int reciveFire(int x, int y){
        int result= battleSpace.recordShot(x,y);
        if(result==1) {
            crew--;
            System.out.println("you've been hit! at "+x+","+y);
        }else{
            if(result==0){
                System.out.println("Enemy missed at "+x+","+y);
            }
        }
        return result;
    }
}
