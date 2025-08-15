package battlenet;

import java.util.Scanner;

public class Paused {
    private static Paused instance;
    private Paused(){}
    public static synchronized Paused getInstance(){ if(instance==null) instance=new Paused(); return instance; }

    public void paused(){
        UI.getInstance().UIWrite("Game Paused, Type 'resume' to resume...");
        Scanner sc = new Scanner(System.in);
        while(true){
            String line = sc.nextLine();
            if("resume".equalsIgnoreCase(line)){ play(); break; }
        }
    }
    public void play(){ UI.getInstance().UIWrite("Resuming game...."); }
}
