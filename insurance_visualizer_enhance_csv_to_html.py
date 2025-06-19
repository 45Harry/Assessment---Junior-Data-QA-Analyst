import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import os

def create_visualization(csv_file_path, output_html_path):
    # Read CSV file
    df = pd.read_csv(csv_file_path)
    
    # Basic statistics
    total_rows = len(df)
    columns = df.columns.tolist()
    
    # Calculate missing values
    missing_data = df.isnull().sum().reset_index()
    missing_data.columns = ['Field', 'Missing Count']
    missing_data['Available Count'] = total_rows - missing_data['Missing Count']
    missing_data['Available Percentage'] = (missing_data['Available Count'] / total_rows * 100).round(2)
    missing_data['Missing Percentage'] = (missing_data['Missing Count'] / total_rows * 100).round(2)
    
    # Calculate distributions for charts
    # 1. Gender distribution
    gender_dist = df['gender'].value_counts().reset_index()
    gender_dist.columns = ['Gender', 'Count']
    
    # 2. Provider distribution (top 15)
    provider_dist = df['name'].value_counts().reset_index().head(15)
    provider_dist.columns = ['Provider', 'Count']
    
    # 3. Postal code distribution (top 10)
    postal_dist = df['post_code'].value_counts().reset_index().head(10)
    postal_dist.columns = ['Postal Code', 'Count']
    
    # 4. Age distribution (grouped into bins)
    age_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    age_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91+']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)
    age_dist = df['age_group'].value_counts().sort_index().reset_index()
    age_dist.columns = ['Age Group', 'Count']
    
    # 5. Hospital insurance type distribution
    hosp_ins_dist = df['Spitalzusatzversicherung'].value_counts().reset_index().head(10)
    hosp_ins_dist.columns = ['Insurance Type', 'Count']
    
    # 6. Franchise amount distribution
    franchise_dist = df['Franchise'].value_counts().reset_index().head(10)
    franchise_dist.columns = ['Franchise Amount', 'Count']
    
    # 7. Product name 1 distribution (top 10)
    product1_dist = df['Product name 1'].value_counts().reset_index().head(10)
    product1_dist.columns = ['Product Name', 'Count']
    
    # 8. Accident insurance distribution
    accident_dist = df['Unfallzusatz in den Zusatzversicherungen'].value_counts().reset_index()
    accident_dist.columns = ['Accident Insurance', 'Count']
    
    # Create HTML with all charts
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Insurance Data Visualization</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        .card {{
            margin-bottom: 20px;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        }}
        .progress {{
            height: 20px;
            margin-bottom: 10px;
        }}
        .progress-bar {{
            font-size: 12px;
            line-height: 20px;
        }}
        .chart-container {{
            width: 100%;
            height: 400px;
            margin-bottom: 30px;
        }}
        .tab-content {{
            padding: 15px;
            border-left: 1px solid #ddd;
            border-right: 1px solid #ddd;
            border-bottom: 1px solid #ddd;
        }}
        .chart-title {{
            text-align: center;
            margin-bottom: 10px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container-fluid mt-3">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h2>Insurance Data Visualization</h2>
            </div>
            <div class="card-body">
                <h4 class="text-success">Total Records: {total_rows:,}</h4>
                <hr>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="chart-title">Gender Distribution</div>
                        <div class="chart-container" id="genderChart"></div>
                    </div>
                    <div class="col-md-6">
                        <div class="chart-title">Top Insurance Providers</div>
                        <div class="chart-container" id="providerChart"></div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="chart-title">Top Postal Codes</div>
                        <div class="chart-container" id="postalChart"></div>
                    </div>
                    <div class="col-md-6">
                        <div class="chart-title">Age Distribution</div>
                        <div class="chart-container" id="ageChart"></div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="chart-title">Hospital Insurance Types</div>
                        <div class="chart-container" id="hospInsChart"></div>
                    </div>
                    <div class="col-md-6">
                        <div class="chart-title">Franchise Amounts</div>
                        <div class="chart-container" id="franchiseChart"></div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="chart-title">Top Product Names</div>
                        <div class="chart-container" id="product1Chart"></div>
                    </div>
                    <div class="col-md-6">
                        <div class="chart-title">Accident Insurance Coverage</div>
                        <div class="chart-container" id="accidentChart"></div>
                    </div>
                </div>
                
                <hr>
                
                <ul class="nav nav-tabs" id="myTab" role="tablist">
                    <li class="nav-item">
                        <a class="nav-link active" id="summary-tab" data-toggle="tab" href="#summary" role="tab">Data Summary</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" id="details-tab" data-toggle="tab" href="#details" role="tab">Detailed View</a>
                    </li>
                </ul>
                
                <div class="tab-content" id="myTabContent">
                    <div class="tab-pane fade show active" id="summary" role="tabpanel">
                        <h4 class="mt-3">Data Completeness</h4>
                        <table class="table table-striped table-bordered">
                            <thead class="thead-dark">
                                <tr>
                                    <th>Field</th>
                                    <th>Available Count</th>
                                    <th>Missing Count</th>
                                    <th>Distribution</th>
                                </tr>
                            </thead>
                            <tbody>
    """
    
    # Add rows for each field's completeness
    for _, row in missing_data.iterrows():
        html_content += f"""
                                <tr>
                                    <td><b>{row['Field']}</b></td>
                                    <td>{row['Available Count']:,}</td>
                                    <td>{row['Missing Count']:,}</td>
                                    <td>
                                        <div class="progress">
                                            <div class="progress-bar bg-success" style="width:{row['Available Percentage']}%">{row['Available Percentage']}%</div>
                                            <div class="progress-bar bg-danger" style="width:{row['Missing Percentage']}%">{row['Missing Percentage']}%</div>
                                        </div>
                                    </td>
                                </tr>
        """
    
    html_content += """
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="tab-pane fade" id="details" role="tabpanel">
                        <div class="table-responsive">
                            <table class="table table-striped table-bordered" id="dataTable">
                                <thead class="thead-dark">
                                    <tr>
    """
    
    # Add table headers
    for col in columns:
        html_content += f"<th>{col}</th>"
    
    html_content += """
                                    </tr>
                                </thead>
                                <tbody>
    """
    
    # Add table rows (limited to 100 for performance)
    for _, row in df.head(100).iterrows():
        html_content += "<tr>"
        for col in columns:
            # Handle NaN values
            cell_value = row[col]
            if pd.isna(cell_value):
                cell_value = "nan"
            html_content += f"<td>{cell_value}</td>"
        html_content += "</tr>"
    
    # JavaScript section with all chart data
    html_content += f"""
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js"></script>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css">
    
    <script>
        $(document).ready(function() {{
            $('#dataTable').DataTable();
        }});
        
        // 1. Gender distribution chart
        var genderData = {{
            values: {gender_dist['Count'].tolist()},
            labels: {gender_dist['Gender'].tolist()},
            type: 'pie',
            marker: {{
                colors: ['#3498db', '#e74c3c', '#2ecc71']
            }}
        }};
        
        Plotly.newPlot('genderChart', [genderData], {{height: 400, width: '100%'}});
        
        // 2. Provider distribution chart
        var providerData = {{
            x: {provider_dist['Provider'].tolist()},
            y: {provider_dist['Count'].tolist()},
            type: 'bar',
            marker: {{
                color: '#9b59b6'
            }}
        }};
        
        Plotly.newPlot('providerChart', [providerData], {{height: 400, width: '100%'}});
        
        // 3. Postal code distribution chart
        var postalData = {{
            x: {postal_dist['Postal Code'].astype(str).tolist()},
            y: {postal_dist['Count'].tolist()},
            type: 'bar',
            marker: {{
                color: '#f1c40f'
            }}
        }};
        
        Plotly.newPlot('postalChart', [postalData], {{height: 400, width: '100%'}});
        
        // 4. Age distribution chart
        var ageData = {{
            x: {age_dist['Age Group'].tolist()},
            y: {age_dist['Count'].tolist()},
            type: 'bar',
            marker: {{
                color: '#e67e22'
            }}
        }};
        
        Plotly.newPlot('ageChart', [ageData], {{height: 400, width: '100%'}});
        
        // 5. Hospital insurance type distribution
        var hospInsData = {{
            x: {hosp_ins_dist['Insurance Type'].tolist()},
            y: {hosp_ins_dist['Count'].tolist()},
            type: 'bar',
            marker: {{
                color: '#1abc9c'
            }}
        }};
        
        Plotly.newPlot('hospInsChart', [hospInsData], {{height: 400, width: '100%'}});
        
        // 6. Franchise amount distribution
        var franchiseData = {{
            x: {franchise_dist['Franchise Amount'].astype(str).tolist()},
            y: {franchise_dist['Count'].tolist()},
            type: 'bar',
            marker: {{
                color: '#e74c3c'
            }}
        }};
        
        Plotly.newPlot('franchiseChart', [franchiseData], {{height: 400, width: '100%'}});
        
        // 7. Product name 1 distribution
        var product1Data = {{
            x: {product1_dist['Product Name'].tolist()},
            y: {product1_dist['Count'].tolist()},
            type: 'bar',
            marker: {{
                color: '#3498db'
            }}
        }};
        
        Plotly.newPlot('product1Chart', [product1Data], {{height: 400, width: '100%'}});
        
        // 8. Accident insurance distribution
        var accidentData = {{
            values: {accident_dist['Count'].tolist()},
            labels: {accident_dist['Accident Insurance'].astype(str).tolist()},
            type: 'pie',
            marker: {{
                colors: ['#2ecc71', '#e74c3c']
            }}
        }};
        
        Plotly.newPlot('accidentChart', [accidentData], {{height: 400, width: '100%'}});
    </script>
</body>
</html>
    """
    
    # Save HTML file
    with open(output_html_path, 'w') as f:
        f.write(html_content)
    
    print(f"HTML visualization created at: {output_html_path}")

# Example usage
if __name__ == "__main__":
    input_csv = "data_with_out_duplicates.csv"  # Replace with your CSV file path
    output_html = "insurance_visualization.html"
    
    if os.path.exists(input_csv):
        create_visualization(input_csv, output_html)
    else:
        print(f"Error: Input CSV file '{input_csv}' not found.")