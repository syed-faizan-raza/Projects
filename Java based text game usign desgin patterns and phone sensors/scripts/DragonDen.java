package battlenet;

public class DragonDen implements State, Location {
    private final User u;
    public DragonDen(User u){ this.u=u; }
    @Override public void next(User u, boolean won){
        if(won){ UI.getInstance().UIWrite("Dragon defeated! Final Stage unlocked."); u.startFinal(); }
        else { UI.getInstance().UIWrite("Burned by Dragon. Back to Hub."); u.setState(Hub.getInstance()); }
    }
    @Override public void lookAround(){
        UI.getInstance().UIWrite("[Dragon's Den] Hold still (gyro) to raise shield. Shake to attack.");
    }
}
