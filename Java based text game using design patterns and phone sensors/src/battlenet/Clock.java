package battlenet;

public class Clock implements Runnable, Subject {
    private final int time;
    public Clock(int time){ this.time=time; }
    @Override public void run() {
        try {
            for(int i=0;i<time;i++){ Thread.sleep(1000); UI.getInstance().UIWrite("1 second has passed"); }
        } catch (InterruptedException ignored){}
        publishMessage(new Message(this,"time", time + " has passed"));
    }
    @Override public void publishMessage(Message m){ UI.getInstance().publishMessage(m); }
    @Override public void addObserver(Observer o){} // using UI fanout
    @Override public void removeObserver(Observer o){} // using UI fanout
}
