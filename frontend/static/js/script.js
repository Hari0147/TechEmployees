const EMPLOYEE_API = "http://employee-service:5001";
const DEPARTMENT_API = "http://department-service:5002";

// Load employees and departments when the page loads
window.onload = function () {
    loadEmployees();
    loadDepartments();
};

// Add Employee
document.getElementById("employeeForm").addEventListener("submit", async function (e) {

    e.preventDefault();

    const employee = {
        name: document.querySelector("input[placeholder='Employee Name']").value,
        department: document.querySelector("input[placeholder='Department']").value,
        salary: document.querySelector("input[placeholder='Salary']").value
    };

    const response = await fetch(`${EMPLOYEE_API}/employees`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(employee)
    });

    if (response.ok) {
        alert("Employee Added Successfully");

        document.getElementById("employeeForm").reset();

        loadEmployees();
    } else {
        alert("Unable to Add Employee");
    }

});

// Load Employees
async function loadEmployees() {

    const response = await fetch(`${EMPLOYEE_API}/employees`);

    const employees = await response.json();

    let html = "";

    employees.forEach(emp => {

        html += `
        <tr>
            <td>${emp.id}</td>
            <td>${emp.name}</td>
            <td>${emp.department}</td>
            <td>${emp.salary}</td>
        </tr>
        `;

    });

    document.querySelector("tbody").innerHTML = html;

}

// Load Departments
async function loadDepartments() {

    const response = await fetch(`${DEPARTMENT_API}/departments`);

    const departments = await response.json();

    console.log("Departments:", departments);

}
