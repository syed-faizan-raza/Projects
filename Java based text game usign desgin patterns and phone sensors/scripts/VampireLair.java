package battlenet;

public class VampireLair implements State, Location {
    private final User u;
    public VampireLair(User u){ this.u=u; }
    @Override public void next(User u, boolean won){
        if(won){ UI.getInstance().UIWrite("Dracula defeated! Onward to Dragon's Den..."); u.startDragon(); }
        else { UI.getInstance().UIWrite("Defeated by Dracula. Back to Hub."); u.setState(Hub.getInstance()); }
    }
    @Override public void lookAround(){
        UI.getInstance().UIWrite("[Vampire Lair] Requires Enchanted Sword. Shake to attack, beat Dracula.");
    }
}
