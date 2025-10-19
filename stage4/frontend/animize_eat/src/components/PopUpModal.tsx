import React from 'react';
import '../styles/PopUpModal.css';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}


const PopUpModal: React.FC<ModalProps> = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close" onClick={onClose}>
          x
        </button>
        {children}
      </div>
    </div>
  );
};

export default PopUpModal;
