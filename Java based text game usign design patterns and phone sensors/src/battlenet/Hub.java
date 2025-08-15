package battlenet;

public class Hub implements State, Location {
    private static Hub instance;
    private Hub(){}
    public static synchronized Hub getInstance(){ if(instance==null) instance=new Hub(); return instance; }
    @Override public void next(User u, boolean won){}
    @Override public void lookAround(){
        UI.getInstance().UIWrite("[Hub] Talk to Hikari (buy), Dr. Gauss (tips). Type: 'buy wooden'/'buy enchanted'/'buy shield', 'brew gold'/'brew silver'.");
        UI.getInstance().UIWrite("Type 'go ogre' to fight Shrek.");
    }
}
