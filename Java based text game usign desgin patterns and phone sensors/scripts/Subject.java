package battlenet;

public interface Subject {
    void publishMessage(Message m);
    void addObserver(Observer o);
    void removeObserver(Observer o);
}
