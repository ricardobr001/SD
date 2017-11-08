import java.rmi.Remote;
import java.rmi.RemoteException;

public interface Transfere extends Remote {

    void envia(String nome, byte[] dados, int tamanho) throws RemoteException; 
}
