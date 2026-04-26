import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Header from './components/Header';
import Home from './screens/Home';
import Login from './screens/Login';
import Register from './screens/Register';
import MyCollection from './screens/MyCollection';
import AddItem from './screens/AddItem';
import ItemDetail from './screens/ItemDetail';
import Public from './screens/Public';
import './index.css';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <div className="app">
          <Header />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/public" element={<Public />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/my-collection" element={<MyCollection />} />
              <Route path="/add-item" element={<AddItem />} />
              <Route path="/edit-item/:id" element={<AddItem />} />
              <Route path="/item/:id" element={<ItemDetail />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
