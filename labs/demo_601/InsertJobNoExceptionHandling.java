import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

/**
 * ```output
 * id INT AUTO_INCREMENT PRIMARY KEY, tidb_server_instance VARCHAR(30)
 * ```
 */

class Worker implements Runnable {

    static String MAIN_TASK = "INSERT INTO test.tiproxy_test (tidb_server_instance) VALUES (SELECT instance FROM information_schema.cluster_processlist WHERE host=(SELECT host FROM information_schema.processlist WHERE id=CONNECTION_ID()));";

    String tidbHost;
    String port;
    String dbUsername;
    String dbPassword;
    int workerId;

    public Worker(String tidbHost, String port, String dbUsername, String dbPassword, int workerId) {
        this.tidbHost = tidbHost;
        this.port = port;
        this.dbUsername = dbUsername;
        this.dbPassword = dbPassword;
        this.workerId = workerId;
    }

    public void newRecord(Connection conn, PreparedStatement ps, int round)
            throws SQLException, InterruptedException {
        System.out.println("Inserting " + round + " by worker " + this.workerId);
        ps.executeUpdate();
        Thread.sleep(1000);
        conn.commit();
    }

    @Override
    public void run() {
        try {
            Connection connection = DriverManager.getConnection(
                    "jdbc:mysql://" + this.tidbHost + ":" + this.port
                            + "/test?useServerPrepStmts=true&cachePrepStmts=true",
                    this.dbUsername,
                    this.dbPassword);
            connection.setAutoCommit(false);

            PreparedStatement ps = connection.prepareStatement(MAIN_TASK);
            int i = 0;
            while (true) {
                newRecord(connection, ps, i);
                i++;
            }
        } catch (Exception e) {
            System.out.println("Exception encountered.");
            System.exit(1);
        }
    }
}

public class InsertJobNoExceptionHandling {
    public static void main(String[] args) throws InterruptedException, SQLException {
        String tidbHost = args[0];
        String port = args[1];
        String dbUsername = args[2];
        String dbPassword = "";
        for (int i = 0; i < 4; i++) {
            new Thread(new Worker(tidbHost, port, dbUsername, dbPassword, (i + 1))).start();
        }
    }
}