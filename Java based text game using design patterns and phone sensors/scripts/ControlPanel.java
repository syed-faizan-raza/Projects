package battlenet;

public class ControlPanel {
    private static ControlPanel instance;
    private Command[] commands = new Command[1];
    private Command undoCommand;

    private ControlPanel(){
        commands[0] = new Play(Paused.getInstance()); // index 0 = resume from pause
    }
    public static synchronized ControlPanel getInstance(){
        if(instance==null) instance = new ControlPanel();
        return instance;
    }
    public void in(int index){
        commands[index].execute();
        undoCommand = commands[index];
    }
    public void undo(){ if(undoCommand!=null) undoCommand.undo(); }
}
