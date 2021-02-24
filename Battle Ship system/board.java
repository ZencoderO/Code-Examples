import java.util.Scanner;
/**
 * Battleship board shows ships and shots taken by opponent
 * Homework 12.
 *
 *     @author Luke Batchelder
 *     @author Jessica Diehl
 */
public class board extends grid {
    /**
     *constucts the board and the hud we will be using
     */
    board(HUD ourReadout) {
        readOut=ourReadout;
    }
    /**
     * record the effect of a shot launched by the oppent and if it conected
     * @param: x x coordinate
     * @param: y y coordinate
     * @return result 0 for a miss 1 for a hit
     *
     */
    public int recordShot(int x, int y){
        //0 means a miss 1 means a hit 2 means you have already fired there
        if (gridValues[y][x] == 0) {
            gridValues[y][x]=3;
            readOut.setMapMiss(x,y);
            return 0;
        } else {
            if(gridValues[y][x]==1){
                gridValues[y][x]=2;
                readOut.setMapHit(x,y);
                return 1;
            }
        }
        return 0;
    }
    /**
     * prints the current board
     */
    public void printboard(){
        for(int i=0; i<boardSize; i++){
            for(int m=0; m<boardSize; m++) {
                if (gridValues[i][m] == 0) {
                    System.out.print("#");
                } else {
                    if (gridValues[i][m] == 1) {
                        System.out.print("$");
                    } else {
                        if (gridValues[i][m] == 2) {
                            System.out.print("X");
                        }else{
                            if(gridValues[i][m]==3){
                                System.out.print("O");
                            }
                        }
                    }
                }
            }
            System.out.println("");
        }
    }
    /**
     *record the effect of a shot launched by the player and if it conected
     * @param: spaces the number of spaces in ships you will have
     */
    protected void placeShips(int spaces){
        int fullships=(int) (spaces/4);
        Scanner kb=new Scanner(System.in);
        int x=0;
        int y=0;
        String direction="";
        for(int i=0; i<=fullships; i++) {
            boolean locationclear = false;
            int ShipSize = 4;
            if (i == fullships) {
                ShipSize = spaces - fullships * 4;
            }
            while (!locationclear) {
                locationclear=true;
                System.out.println("What is the x corodinate for your "+ShipSize+" length ship:");
                x = kb.nextInt();
                System.out.println("What is the y corodinate for your "+ShipSize+" length ship:");
                y = kb.nextInt();
                System.out.println("What direction do you want the ship to be faceing? North South East or West");
                direction = kb.next().toLowerCase().substring(0, 1);
                for (int m = 0; m < ShipSize; m++) {
                    if(locationclear) {
                        switch (direction) {
                            case "n":
                                if (y - m >= 0) {
                                    if (gridValues[y - m][x] == 0)
                                        break;
                                }
                                System.out.println("your ship did not fit in the grid try again");
                                locationclear = false;
                                break;
                            case "s":
                                if (y + m < 10) {
                                    if (gridValues[y + m][x] == 0)
                                        break;
                                }
                                System.out.println("your ship did not fit in the grid try again");
                                locationclear = false;
                                break;
                            case "e":
                                if (x + m < 10) {
                                    if (gridValues[y][x + m] == 0)
                                        break;
                                }
                                System.out.println("your ship did not fit in the grid try again");
                                locationclear = false;
                                break;
                            case "w":
                                if (x - m >=0) {
                                    if (gridValues[y][x - m] == 0)
                                        break;
                                }
                                System.out.println("your ship did not fit in the grid try again");
                                locationclear = false;
                                break;
                            default:
                                System.out.println("your ship did not fit in the grid try again");
                                locationclear = false;
                        }
                    }
                }

            }
            for (int m = 0; m < ShipSize; m++) {
                switch (direction) {
                    case "n":
                        gridValues[y - m][x] = 1;
                        readOut.setBattleship(x,y-m);
                    break;
                    case "s":
                        gridValues[y + m][x] = 1;
                        readOut.setBattleship(x,y+m);
                    break;

                    case "e":
                       gridValues[y][x + m] = 1;
                        readOut.setBattleship(x+m,y);
                    break;
                    case "w":
                       gridValues[y][x - m] = 1;
                        readOut.setBattleship(x-m,y);
                    break;
                    }
                }
            }
        }
    }




