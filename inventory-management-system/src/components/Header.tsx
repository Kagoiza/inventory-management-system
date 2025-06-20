
import React from 'react';
import { Search } from 'lucide-react';
import { Input } from '@/components/ui/input';
import AdminToggle from './AdminToggle';

interface HeaderProps {
  isAdmin: boolean;
  onAdminToggle: (isAdmin: boolean) => void;
}

const Header = ({ isAdmin, onAdminToggle }: HeaderProps) => {
  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">
          Hello Sarah!!
        </h1>
        
        <div className="flex items-center space-x-4">
          <div className="relative w-96">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input 
              placeholder="Search for items..." 
              className="pl-10 bg-gray-50 border-gray-200"
            />
          </div>
          
          <AdminToggle isAdmin={isAdmin} onToggle={onAdminToggle} />
        </div>
      </div>
    </div>
  );
};

export default Header;
