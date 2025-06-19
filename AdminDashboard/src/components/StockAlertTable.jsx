import React from 'react';

const StockAlertTable = () => (
  <div className="bg-white p-6 rounded-xl shadow-md mb-6">
    <h2 className="text-xl font-semibold mb-4">Stock Alerts</h2>
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm text-left">
        <thead className="bg-gray-100 text-gray-600 uppercase">
          <tr>
            <th className="px-4 py-2">Item ID</th>
            <th className="px-4 py-2">Name</th>
            <th className="px-4 py-2">Quantity</th>
            <th className="px-4 py-2">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr className="border-b">
            <td className="px-4 py-2">ITM001</td>
            <td className="px-4 py-2">Router</td>
            <td className="px-4 py-2">2</td>
            <td className="px-4 py-2 text-yellow-500 font-semibold">Low</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
);

export default StockAlertTable;
