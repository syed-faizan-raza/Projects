package battlenet;

public class FireBreath implements AttackBehaviour{
    @Override public void attack(){ UI.getInstance().UIWrite("Breathes fire!"); }
}
