import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const data = [
  { name: 'Mon', Issued: 40, Returned: 20 },
  { name: 'Tue', Issued: 30, Returned: 22 },
  { name: 'Wed', Issued: 20, Returned: 15 },
  { name: 'Thu', Issued: 27, Returned: 25 },
  { name: 'Fri', Issued: 18, Returned: 12 },
];

const ChartSection = () => (
  <div className="bg-white p-6 rounded-xl shadow-md mb-6">
    <h2 className="text-xl font-semibold mb-4">Stock Movement (This Week)</h2>
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="Issued" fill="#006644" radius={[6, 6, 0, 0]} />
          <Bar dataKey="Returned" fill="#b21e27" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  </div>
);

export default ChartSection;
