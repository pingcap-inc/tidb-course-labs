import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

/**
 * ```output
 * id INT AUTO_INCREMENT PRIMARY KEY, tidb_server_instance VARCHAR(30)
 * ```
 */

public class InsertJobNoTry {

    static String MAIN_TASK = "INSERT INTO test.tiproxy_test (tidb_server_instance) VALUES (SELECT instance FROM information_schema.cluster_processlist WHERE host=(SELECT host FROM information_schema.processlist WHERE id=CONNECTION_ID()));";

    public static void newRecord(Connection conn, PreparedStatement ps, int round)
            throws SQLException, InterruptedException {
        System.out.println("Inserting " + round);
        ps.executeUpdate();
        Thread.sleep(1000);
        conn.commit();
    }

    public static void main(String[] args) throws InterruptedException, SQLException {

        String tidbHost = args[0];
        String port = args[1];
        String dbUsername = args[2];
        String dbPassword = "";
        Connection connection = null;

        connection = DriverManager.getConnection(
                "jdbc:mysql://" + tidbHost + ":" + port + "/test?useServerPrepStmts=true&cachePrepStmts=true",
                dbUsername,
                dbPassword);
        connection.setAutoCommit(false);

        PreparedStatement ps = connection.prepareStatement(MAIN_TASK);
        int i = 0;
        while (true) {
            newRecord(connection, ps, i);
            i++;
        }

    }
}