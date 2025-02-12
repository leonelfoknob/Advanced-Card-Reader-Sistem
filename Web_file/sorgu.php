<?php
// Enable error reporting for debugging
ini_set('display_errors', 1);
error_reporting(E_ALL);

// Database connection details
$servername = "localhost";
$username = "*****";  // Use the username you created (or root)
$password = "*****";  // Use the password for the MySQL user
$dbname = "*****";  // Name of the database

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get search parameters
$searchBranch = isset($_POST['searchBranch']) ? $_POST['searchBranch'] : '';
$searchDate = isset($_POST['searchDate']) ? $_POST['searchDate'] : '';

// Get the updated credit if it's submitted
if (isset($_POST['updateCredit'])) {
    $userId = $_POST['user_id'];
    $newCredit = $_POST['newCredit'];
    
    // Update the user's credit in the database
    $stmt = $conn->prepare("UPDATE kayit SET credit = ? WHERE id = ?");
    $stmt->bind_param("ii", $newCredit, $userId);

    if ($stmt->execute()) {
        echo "Credit updated successfully.<br>";
    } else {
        echo "Error updating credit: " . $stmt->error . "<br>";
    }

    // Close the statement
    $stmt->close();
}

// Build the query to search users
$query = "SELECT * FROM kayit WHERE 1"; // Default condition (fetch all users)

// Add conditions to the query if fields are set
if (!empty($searchBranch)) {
    $query .= " AND branch LIKE '%" . $conn->real_escape_string($searchBranch) . "%'";
}
if (!empty($searchDate)) {
    $query .= " AND DATE(registration_date) = '" . $conn->real_escape_string($searchDate) . "'";
}

// Execute the query
$result = $conn->query($query);

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Search and Credit Update</title>
</head>
<body>

<h1>Search Users and Update Credit</h1>

<!-- Search Form -->
<form method="POST">
    <div>
        <label for="searchBranch">Search by Branch:</label>
        <input type="text" id="searchBranch" name="searchBranch" value="<?php echo htmlspecialchars($searchBranch); ?>">
    </div>
    <div>
        <label for="searchDate">Search by Registration Date:</label>
        <input type="date" id="searchDate" name="searchDate" value="<?php echo htmlspecialchars($searchDate); ?>">
    </div>
    <div>
        <button type="submit">Search</button>
    </div>
</form>

<hr>

<?php
// If users are found, display them with a form to update credit
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        echo "<div style='border: 1px solid #ddd; margin-bottom: 15px; padding: 10px;'>";
        echo "<p><strong>Name:</strong> " . $row['name'] . "</p>";
        echo "<p><strong>Surname:</strong> " . $row['surname'] . "</p>";
        echo "<p><strong>Branch:</strong> " . $row['branch'] . "</p>";
        echo "<p><strong>Credit:</strong> " . $row['credit'] . "</p>";

        // Display a form to update the user's credit
        echo "<form method='POST' action=''>
                <input type='hidden' name='user_id' value='" . $row['id'] . "'>
                <label for='newCredit'>New Credit Amount:</label>
                <input type='number' name='newCredit' value='" . $row['credit'] . "' required>
                <button type='submit' name='updateCredit'>Update Credit</button>
              </form>";

        echo "</div>";
    }
} else {
    echo "<p>No users found based on the search criteria.</p>";
}

// Close the connection
$conn->close();
?>

</body>
</html>
