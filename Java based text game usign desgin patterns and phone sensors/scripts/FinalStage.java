package battlenet;

public class FinalStage implements State, Location {
    private final User u;
    public FinalStage(User u){ this.u = u; }
    @Override public void next(User u, boolean won){
        if(won){
            UI.getInstance().UIWrite("WOOOW, You finished the game! Sister rescued.");
            System.exit(0);
        } else {
            UI.getInstance().UIWrite("Noise detected! Back to Hub.");
            u.setState(Hub.getInstance());
        }
    }
    @Override public void lookAround(){
        UI.getInstance().UIWrite("[Final Stage] Sneak: keep mic level low to succeed.");
    }
}
