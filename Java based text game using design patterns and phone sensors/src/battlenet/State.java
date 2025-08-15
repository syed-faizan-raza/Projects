package battlenet;

public interface State {
    void next(User u, boolean won);
    void lookAround();
}
