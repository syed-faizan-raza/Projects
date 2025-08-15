package battlenet;

public class Play implements Command{
    private final Paused paused;
    public Play(Paused p){ this.paused = p; }
    @Override public void execute(){ paused.play(); }
    @Override public void undo(){}
}
