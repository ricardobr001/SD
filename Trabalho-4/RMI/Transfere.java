import java.rmi.Remote;
import java.rmi.RemoteException;

public interface Transfere extends Remote {

    boolean envia(String nome, byte[] dados, int tamanho) throws RemoteException; 
}
