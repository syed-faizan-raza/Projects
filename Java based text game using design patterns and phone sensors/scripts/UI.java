package battlenet;

import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;

public class UI implements Runnable, Subject {
    private static UI instance;
    private final List<Observer> observers = new CopyOnWriteArrayList<>();
    private UI(){}
    public static synchronized UI getInstance(){
        if(instance==null) instance = new UI();
        return instance;
    }
    public void UIWrite(String s){ System.out.println(s); }

    @Override public void run() {
        Scanner in = new Scanner(System.in);
        while (true) {
            String s = in.nextLine();
            publishMessage(new Message(this, "UI", s));
        }
    }
    @Override public void publishMessage(Message m) {
        for(Observer o: observers) o.update(m);
    }
    @Override public void addObserver(Observer o){ observers.add(o); }
    @Override public void removeObserver(Observer o){ observers.remove(o); }
}
