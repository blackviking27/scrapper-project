import React, { useState } from 'react';
import './App.css';

function App() {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);
    const [error, setError] = useState(null);

    const handleSearch = async (e) => {
        e.preventDefault();
        setError(null); // Reset error state

        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/data/find`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ term: searchTerm }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            if (data?.data?.data) {
                setResults(data.data.data);
            } else {
                setError(data.message);
            }
        } catch (err) {
            setError(err.message);
        }
    };

    const handleCrawl = async (e) => {
      e.preventDefault();
      setError(null); // Reset error state

      try {
          const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/data/crawl`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ term: searchTerm }),
          });

          if (!response.ok) {
              throw new Error('Network response was not ok');
          }

          const data = await response.json();
          if (data?.data?.data) {
              setResults(data.data.data);
          } else {
              setError(data.message);
          }
      } catch (err) {
          setError(err.message);
      }
  };

    return (
        <div className="App min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
            <h1 className="text-2xl font-bold mb-4">Company Search</h1>
                <input
                    type="text"
                    placeholder="Enter company name"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-[50%] p-2 border border-gray-300 rounded mb-2"
                />
                <div className="flex space-x-2">
                  <button
                      type="submit"
                      className="w-full bg-green-500 text-white p-2 rounded hover:bg-blue-600 transition"
                      onClick={handleCrawl}
                  >
                      Crawl
                  </button>
                  <button
                      onClick={handleSearch}
                      type="submit"
                      className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition"
                  >
                      Search
                  </button>
                </div>
            
            {error && <p className="text-red-500 mt-2">{error}</p>}
            <ul className="mt-4 w-full max-w-md">
                {results.map((company, index) => (
                    <li key={index} className="bg-white shadow-md rounded p-4 mb-2">
                        <strong>Name:</strong> {company.name} <br />
                        <strong>Document Number:</strong> {company.documentNumber} <br />
                        <strong>Status:</strong> {company.status} <br />
                        <strong>Details URL:</strong> <a href={company.detailsUrl} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">View Details</a>
                        <div className="mt-2">
                            <strong className='text-green-500'>Filing Information:</strong>
                            <ul>
                                <li><strong>Document Number:</strong> {company.details.filingInformation["Document Number"]}</li>
                                <li><strong>FEI/EIN Number:</strong> {company.details.filingInformation["FEI/EIN Number"]}</li>
                                <li><strong>Date Filed:</strong> {company.details.filingInformation["Date Filed"]}</li>
                                <li><strong>State:</strong> {company.details.filingInformation["State"]}</li>
                                <li><strong>Status:</strong> {company.details.filingInformation["Status"]}</li>
                                <li><strong>Last Event:</strong> {company.details.filingInformation["Last Event"]}</li>
                                <li><strong>Event Date Filed:</strong> {company.details.filingInformation["Event Date Filed"]}</li>
                                <li><strong>Event Effective Date:</strong> {company.details.filingInformation["Event Effective Date"]}</li>
                            </ul>
                        </div>
                        <div className="mt-2">
                            <strong className='text-green-500'>Registered Agent:</strong>
                            <ul>
                                <li><strong>Name:</strong> {company.details.registeredAgent.name}</li>
                                <li><strong>Address:</strong> {company.details.registeredAgent.address}</li>
                            </ul>
                        </div>
                        <div>
                            <strong className='text-green-500'>Principal Address:</strong>
                            <div>{company.details.principalAddress}</div>
                        </div>
                        <div>
                            <strong className='text-green-500'>Mailing Address:</strong>
                            <div>{company.details.mailingAddress}</div>
                        </div>
                        <div>
                            <strong className='text-green-500'>Officers:</strong>
                            <ul>
                                {company.details.officers.map((officer, idx) => (
                                    <li key={idx}>
                                        {officer.title}: {officer.name} - {officer.address}
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div>
                            <strong className='text-green-500'>Annual Reports:</strong>
                            <ul>
                                {company.details.annualReports.map((report, idx) => (
                                    <li key={idx}>
                                        Year: {report.year}, Filed Date: {report.filed_date}
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div>
                            <strong className='text-green-500'>Document Images:</strong>
                            <ul>
                                {company.details.documentImages.map((image, idx) => (
                                    <li key={idx}>
                                        <a href={image.url} target="_blank" rel="noopener noreferrer">{image.name}</a>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;