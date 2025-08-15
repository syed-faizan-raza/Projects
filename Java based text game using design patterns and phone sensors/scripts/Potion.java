package battlenet;

public abstract class Potion {
    public final void preparePotion(){
        addIngredients();
        stir();
        heat();
        UI.getInstance().UIWrite("You may now collect your potion – enjoy!");
    }
    protected abstract void addIngredients();
    protected void stir(){ UI.getInstance().UIWrite("Stirring the mixture..."); }
    protected void heat(){ UI.getInstance().UIWrite("Heating to perfect temperature..."); }
}
