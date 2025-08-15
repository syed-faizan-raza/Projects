package battlenet;

public class HighKick implements AttackBehaviour{
    @Override public void attack(){ UI.getInstance().UIWrite("Uses high kick attack"); }
}
