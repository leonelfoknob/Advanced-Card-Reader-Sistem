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

// Capture POST data from the form
$name = $_POST['name'];
$surname = $_POST['surname'];
$age = $_POST['age'];
$branch = $_POST['branch'];
$motherName = $_POST['motherName'];
$fatherName = $_POST['fatherName'];
$phoneNumber = $_POST['phoneNumber'];
$nationalId = $_POST['nationalId'];
$uid = $_POST['uid'];
$credit = $_POST['credit']; // Capture the credit input

// Prepare an SQL statement with placeholders
$stmt = $conn->prepare("INSERT INTO kayit (name, surname, age, branch, mother_name, father_name, phone_number, national_id, uid, credit) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");

// Bind the form data to the prepared statement
$stmt->bind_param("ssissssssi", $name, $surname, $age, $branch, $motherName, $fatherName, $phoneNumber, $nationalId, $uid, $credit);

// Execute the prepared statement
if ($stmt->execute()) {
    echo "New record created successfully";
} else {
    echo "Error: " . $stmt->error;
}

// Close the prepared statement and the connection
$stmt->close();
$conn->close();
?>
