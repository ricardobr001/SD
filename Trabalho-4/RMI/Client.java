import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.io.*;

public class Client {
    public static void main(String[] args) {

        if (args.length != 1) {
            System.out.println("MODO DE USAR: java Client <nome do arquivo>");
        }
        
        try {
            Registry registry = LocateRegistry.getRegistry("200.9.84.233");
            Transfere stub = (Transfere) registry.lookup("Transfere");
            // File arquivo = new File(args[0]);
            byte[] dados = new byte[1048576];
            FileInputStream entrada = new FileInputStream(args[0]);
            int qtddLida = entrada.read(dados);

            while (qtddLida > 0) {
                boolean response = stub.envia(args[0], dados, qtddLida);
                System.out.println("Transferido " + qtddLida + " bytes do arquivo " + args[0]);
                qtddLida = entrada.read(dados);
            }

        } catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
