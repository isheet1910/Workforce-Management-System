import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['EmployeeDB']

# Example: Fetch data from the Employee collection
cursor = db.Employee.find({})
data = list(cursor)

# Convert data to a Pandas DataFrame
df = pd.DataFrame(data)
# Display the first few rows of the DataFrame
print(df.head())
dep = df['department']
emp = df['emp_id']
department_counts = df['department'].value_counts()
df.info()


# Generate summary statistics
print(df.describe())

# Convert a column to numeric
df['emp_id'] = pd.to_numeric(df['emp_id'])

# Now, you can plot
plt.plot(df['emp_id'], df['department'])
plt.show()
department_counts.plot(kind='bar', xlabel='Department', ylabel='Number of Employees', title='Number of Employees in Each Department')
# Plot data (requires additional libraries, e.g., matplotlib or seaborn)
df.plot(kind='bar', x=dep, y=emp, title='Projects per Employee')
