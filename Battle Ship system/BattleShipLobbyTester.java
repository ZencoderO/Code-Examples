

import java.io.*;
import java.net.*;
import java.util.*;


/**
 * class that can let the user host or join any number of games useing the battleship protocols same as lobby
 * but will be used to test localy
 * Homework 12.
 *
 *     @author Luke Batchelder
 *     @author Jessica Diehl
 */
public class BattleShipLobbyTester {

    /**
     * host a game and accept concetions from other players, run the game, other player shots frist
     * @param: Port: used by the host
     * @param: hostPlayer object that will repersent the host
     * @return Victory! if won Defeat if lost
     *
     */
    static String hostGame( int Port, player HostPlayer ) {
        String battleResults = "Victory!";
        ServerSocket Server;
        Socket client;
        try {
            Server = new ServerSocket(Port);
            System.out.println("Your name is " + Server.getInetAddress().getHostName());
            System.out.println("Your port number is " + Server.getLocalPort());
            client = Server.accept();
        } catch (IOException e) {
            e.printStackTrace();
            return "Socket was not open try again";
        }
        try (PrintWriter fireComand =
                     new PrintWriter(client.getOutputStream(), true);
             BufferedReader fireRecived = new BufferedReader(
                     new InputStreamReader(client.getInputStream()));) {
            String lastShot="";
            int x;
            int y;
            while (HostPlayer.crew > 0 && !lastShot.equals("-1,-1")) {
                System.out.println("Opponents turn");
                lastShot= fireRecived.readLine();
                if(lastShot.equals("-1,-1")){
                    break;
                }
                x = Integer.parseInt(lastShot.substring(0, 1));
                y = Integer.parseInt(lastShot.substring(2));
                int damageResults=HostPlayer.reciveFire(x, y);
                fireComand.println(damageResults);
                if (HostPlayer.crew == 0) {
                    battleResults = "Defeat";
                    fireComand.println("-1,-1");
                } else {
                    String output = HostPlayer.fire();
                    x = Integer.parseInt(output.substring(0, 1));
                    y = Integer.parseInt(output.substring(2));
                    fireComand.println(output);
                    int results = Integer.parseInt(fireRecived.readLine());
                    HostPlayer.fireResults(x, y, results);
                }
            }
            client.close();
            Server.close();
        }catch(IOException e){
            e.printStackTrace();
            return "bad input try again.";
        }
        return battleResults;
    }

    /**
     * join a game created that uses the battleship
     * protocols, run the game, player shoots first
     * @param: address name of the Server
     * @param: port: port of the Server
     * @return Victory! if won Defeat if lost
     *
     */
    public static String runInHostedGame(String address, int port, player ClientPlayer) throws UnknownHostException{
        String battleResults="Victory!";
        try(
                // BufferedReader MyComand = new BufferedReader( new InputStreamReader(System.in));
                Socket Client= new Socket(address, port);
                BufferedReader fireRecived = new BufferedReader (
                        new InputStreamReader (Client.getInputStream()));
                PrintWriter fireComand =new PrintWriter( Client.getOutputStream(),true);
        ) {
            System.out.println("conected to "+ address);
            String lastShot="";
            while (ClientPlayer.crew > 0 && !lastShot.equals("-1,-1")){
                String output=ClientPlayer.fire();
                fireComand.println(output);
                int x=Integer.parseInt(output.substring(0,1));
                int y=Integer.parseInt(output.substring(2));
                int results = Integer.parseInt(fireRecived.readLine());
                ClientPlayer.fireResults(x,y,results);
                System.out.println("Opponent turn");

                lastShot=fireRecived.readLine();
                if(!lastShot.equals("-1,-1")) {
                    x = Integer.parseInt(output.substring(0, 1));
                    y = Integer.parseInt(output.substring(2));
                    results=ClientPlayer.reciveFire(x, y);
                    fireComand.println(results);
                }
                if(ClientPlayer.crew==0){
                    battleResults="Defeat";
                    fireComand.println("-1.-1");
                }
            }

        }catch(IOException e){
            e.printStackTrace();
            return "bad input try again.";
        }
        return battleResults;
    }

    /**
     * alows the user to join or host any number of battleship games
     */
    public static void main(String[] args) {
        String hostingStatus="";
        String Results="";
        Scanner kb=new Scanner(System.in);
        while(!hostingStatus.equals("q")){
            System.out.println("do you wish to host (h) port into another game (c) or quit (q)?");
            hostingStatus=kb.next().toLowerCase().substring(0,1);
            if(hostingStatus.equals("h")){
                player Player1=new player();
                System.out.println("what is the portNumber you will use?");
                int portnumber=kb.nextInt();
                Results=hostGame(portnumber, Player1);
            }
            if(hostingStatus.equals("c")){
                String gameAddress;
                player Player1=new player();
                try{
                    System.out.println("enter the name of the game you want to conect to");
                    gameAddress=kb.next();
                    System.out.println("enter the port of the game you want to conect to");
                    Results=runInHostedGame(gameAddress,kb.nextInt(),Player1);
                }catch(UnknownHostException e){
                    System.out.println("wrong name, try again.");
                }

            }
            System.out.println(Results);
        }

    }

}
