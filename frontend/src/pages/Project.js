import React from 'react'

export default function Project() {
  return (
    <>
    <div className="page-wrapper">
        <div className="page-header d-print-none mb-3">
          <div className="container-xl">
            <div className='card'>
                <div className='card-header'>
                    <h3 className='card-title'>Project Details</h3>
                </div>
                <div className='card-body'>
                <table className='table card-table table-vcenter text-nowrap datatable'>
                    <thead>
                        <tr>
                            <th>Service</th>
                            <th>Docker Port</th>
                            <th>Real-Life Port</th>
                            <th>Docker Container Name</th>
                            <th>Docker Image</th>
                            <th>Link</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td data-label="Service">FastAPI</td>
                            <td>8000</td>
                            <td>8000</td>
                            <td>backend</td>
                            <td>Dev dockerfile</td>
                            <td><a href="http://139.59.87.2:8000/docs" target="_blank" rel="noreferrer">http://139.59.87.2:8000/docs</a></td>
                        </tr>
                        <tr>
                            <td data-label="Service">React</td>
                            <td>3000</td>
                            <td>3000</td>
                            <td>frontend</td>
                            <td>Dev dockerfile</td>
                            <td><a href="http://139.59.87.2:3000" target="_blank" rel="noreferrer">http://139.59.87.2:3000</a></td>
                        </tr>
                        <tr>
                            <td data-label="Service">Kafdrop - Apache Kafka UI</td>
                            <td>9000</td>
                            <td>9000</td>
                            <td>kafdrop</td>
                            <td>obsidiandynamics/kafdrop</td>
                            <td><a href="http://139.59.87.2:9000" target="_blank" rel="noreferrer">http://139.59.87.2:9000</a></td>
                        </tr>
                        <tr>
                            <td data-label="Service">Kafa</td>
                            <td>9092</td>
                            <td>9092</td>
                            <td>kafka</td>
                            <td>confluentinc/cp-kafka:latest</td>
                            <td><a href="http://139.59.87.2:9000" target="_blank" rel="noreferrer">http://139.59.87.2:9092</a></td>
                        </tr>  
                        <tr>
                            <td data-label="Service">zookeeper</td>
                            <td>2181</td>
                            <td>2181</td>
                            <td>zookeeper</td>
                            <td>confluentinc/cp-zookeeper:latest</td>
                            <td><a href="http://139.59.87.2:8081" target="_blank" rel="noreferrer">http://139.59.87.2:2181</a></td>
                        </tr>                       
                        <tr>
                            <td data-label="Service">jobmanager - Apache Flink UI</td>
                            <td>8081</td>
                            <td>8081</td>
                            <td>jobmanager</td>
                            <td>dockerfile.flink</td>
                            <td><a href="http://139.59.87.2:8081" target="_blank" rel="noreferrer">http://139.59.87.2:8081</a></td>
                        </tr>
                        <tr>
                            <td data-label="Service">taskmanager - Apache Flink</td>
                            <td>6121</td>
                            <td>6122</td>
                            <td>taskmanager</td>
                            <td>flink:1.16.0</td>
                            <td><a href="http://139.59.87.2:8081" target="_blank" rel="noreferrer">http://139.59.87.2:6121</a></td>
                        </tr>                                                
                        <tr>
                            <td data-label="Service">pgadmin - Postgres UI</td>
                            <td>5050</td>
                            <td>5050</td>
                            <td>pgadmin</td>
                            <td>dpage/pgadmin4</td>
                            <td><a href="http://139.59.87.2:5050" target="_blank" rel="noreferrer">http://139.59.87.2:5050</a></td>
                        </tr>
                        <tr>
                            <td data-label="Service">postgres</td>
                            <td>5432</td>
                            <td>5432</td>
                            <td>postgres</td>
                            <td>postgres:14</td>
                            <td><a href="http://139.59.87.2:5050" target="_blank" rel="noreferrer">http://139.59.87.2:5050</a></td>
                        </tr>                        
                    </tbody>
                </table>
                </div>
            </div>
          </div>
        </div>
    </div>
    </>
  );
}