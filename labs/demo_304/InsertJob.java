import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

/**
 * ```output
 * +-------+-----------+------+------+---------+----------------+
 * | Field | Type | Null | Key | Default | Extra |
 * +-------+-----------+------+------+---------+----------------+
 * | id | int | NO | PRI | NULL | auto_increment |
 * | k | int | NO | MUL | 0 | |
 * | c | char(120) | NO | | | |
 * | pad | char(60) | NO | | | |
 * +-------+-----------+------+------+---------+----------------+
 * 4 rows in set (0.00 sec)
 * ```
 */

public class InsertJob {

    static String MAIN_TASK = "INSERT INTO sbtest1000.sbtest9 (k, c, pad) VALUES (?, 'A', 'B');";

    public static void newRecord(Connection conn, PreparedStatement ps, int round) {
        System.out.println("Inserting " + round);
        try {
            ps.setInt(1, round);
            ps.executeUpdate();
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            conn.commit();
        } catch (SQLException e) {
            if (e.getErrorCode() == 8028) {
                System.out.println("Schema mutation encountered, retry ...");
                try {
                    try {
                        Thread.sleep(1000);
                        ps.executeUpdate();
                    } catch (InterruptedException e2) {
                        e.printStackTrace();
                    }
                    conn.commit();
                } catch (SQLException e1) {
                    System.out.println("Unhandled situation.");
                }
            } else {
                e.printStackTrace();
                System.exit(1);
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {

        String tidbHost = args[0];
        String port = args[1];
        String dbUsername = args[2];
        String dbPassword = "tidb";
        Connection connection = null;
        try {
            connection = DriverManager.getConnection(
                    "jdbc:mysql://" + tidbHost + ":" + port + "/sbtest1000?useServerPrepStmts=true&cachePrepStmts=true",
                    dbUsername,
                    dbPassword);
            connection.setAutoCommit(false);
            try {
                PreparedStatement ps = connection.prepareStatement(MAIN_TASK);
                int i = 0;
                while (true) {
                    newRecord(connection, ps, i);
                    i++;
                }
            } catch (SQLException e) {
                System.out.println("Prepare statement failed.");
            }
        } catch (SQLException e) {
            System.out.println("Cannot connect to TiDB server instance.");
            e.printStackTrace();
        }
    }
}