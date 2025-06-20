
import React from 'react';
import { Card } from '@/components/ui/card';

interface StatsCardsProps {
  requests: any[];
}

const StatsCards = ({ requests }: StatsCardsProps) => {
  const totalRequests = requests.length;
  const approvedRequests = requests.filter(r => r.status === 'Approved').length;
  const pendingRequests = requests.filter(r => r.status === 'Pending').length;
  const deniedRequests = requests.filter(r => r.status === 'Denied').length;

  const stats = [
    {
      title: 'Total Items Requested',
      value: totalRequests.toString(),
      color: 'bg-green-500',
      textColor: 'text-white'
    },
    {
      title: 'Approved',
      value: approvedRequests.toString(),
      color: 'bg-gray-100',
      textColor: 'text-gray-700'
    },
    {
      title: 'Pending',
      value: pendingRequests.toString(),
      color: 'bg-gray-100',
      textColor: 'text-gray-700'
    },
    {
      title: 'Denied',
      value: deniedRequests.toString(),
      color: 'bg-gray-100',
      textColor: 'text-gray-700'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      {stats.map((stat, index) => (
        <Card key={index} className={`p-6 ${stat.color}`}>
          <div className={`${stat.textColor}`}>
            <p className="text-sm font-medium opacity-90">{stat.title}</p>
            <p className="text-3xl font-bold mt-2">{stat.value}</p>
          </div>
        </Card>
      ))}
    </div>
  );
};

export default StatsCards;
