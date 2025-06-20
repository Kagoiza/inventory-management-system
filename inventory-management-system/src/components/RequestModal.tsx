
import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useToast } from '@/hooks/use-toast';

interface RequestModalProps {
  onSubmit: (request: any) => void;
  children: React.ReactNode;
}

const RequestModal = ({ onSubmit, children }: RequestModalProps) => {
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({
    type: '',
    category: '',
    description: '',
    justification: '',
    urgency: 'medium'
  });
  const { toast } = useToast();

  const itemTypes = [
    'Laptop', 'Desktop', 'Monitor', 'Keyboard', 'Mouse', 'Printer', 
    'Office Chair', 'Office Desk', 'Router', 'Switch', 'Phone', 'Tablet'
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.type || !formData.description) {
      toast({
        title: "Error",
        description: "Please fill in all required fields",
        variant: "destructive"
      });
      return;
    }

    const newRequest = {
      id: Date.now(),
      type: formData.type,
      category: formData.category,
      description: formData.description,
      justification: formData.justification,
      urgency: formData.urgency,
      status: 'Pending',
      date: new Date().toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      }),
      statusColor: 'bg-yellow-100 text-yellow-800'
    };

    onSubmit(newRequest);
    setFormData({
      type: '',
      category: '',
      description: '',
      justification: '',
      urgency: 'medium'
    });
    setOpen(false);
    
    toast({
      title: "Request Submitted",
      description: "Your request has been submitted successfully",
    });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {children}
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Request New Item</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="type">Item Type *</Label>
            <Select value={formData.type} onValueChange={(value) => setFormData({...formData, type: value})}>
              <SelectTrigger>
                <SelectValue placeholder="Select item type" />
              </SelectTrigger>
              <SelectContent>
                {itemTypes.map((type) => (
                  <SelectItem key={type} value={type}>{type}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label htmlFor="category">Category</Label>
            <Input
              id="category"
              value={formData.category}
              onChange={(e) => setFormData({...formData, category: e.target.value})}
              placeholder="e.g., Hardware, Furniture, etc."
            />
          </div>

          <div>
            <Label htmlFor="description">Description *</Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              placeholder="Describe the item you need..."
              rows={3}
            />
          </div>

          <div>
            <Label htmlFor="justification">Business Justification</Label>
            <Textarea
              id="justification"
              value={formData.justification}
              onChange={(e) => setFormData({...formData, justification: e.target.value})}
              placeholder="Why do you need this item?"
              rows={2}
            />
          </div>

          <div>
            <Label htmlFor="urgency">Urgency</Label>
            <Select value={formData.urgency} onValueChange={(value) => setFormData({...formData, urgency: value})}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="low">Low</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="high">High</SelectItem>
                <SelectItem value="urgent">Urgent</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="flex justify-end space-x-2 pt-4">
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit">Submit Request</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default RequestModal;
