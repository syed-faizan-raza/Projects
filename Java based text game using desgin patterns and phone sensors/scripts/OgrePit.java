package battlenet;

public class OgrePit implements State, Location {
    private static OgrePit instance;
    private OgrePit(){}
    public static synchronized OgrePit getInstance(){ if(instance==null) instance=new OgrePit(); return instance; }
    @Override public void next(User u, boolean won){
        if(won){ u.gold += 10; UI.getInstance().UIWrite("Shrek defeated! Earned 10 gold."); u.startVampire(); }
        else { UI.getInstance().UIWrite("Defeated by Shrek. Back to Hub."); u.setState(Hub.getInstance()); }
    }
    @Override public void lookAround(){
        UI.getInstance().UIWrite("[Ogre's Pit] Shake phone to attack (AccelZ). Defeat Shrek!");
    }
}
