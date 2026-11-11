import { useState } from 'react'
import ProductPage from "./page/ProductPage.jsx";
import { Routes, Route, Link } from "react-router";
import BrowsePage from './page/BrowsePage.jsx';
import ProductDetailPage from './page/ProductDetailPage.jsx';

function App() {
  return (
    <>
      <nav>
        <Link to="/products">All Products</Link> | <Link to="/browse">Browse</Link>
      </nav>
      <Routes>
        <Route path="/" element={<ProductPage />} />
        <Route path="/products" element={<ProductPage />} />
        <Route path="/browse" element={<BrowsePage />} />
        <Route path="/products/:id" element={<ProductDetailPage />} />
        <Route path="*" element={<h1>404 Not Found</h1>} />
      </Routes>
    </>
  )
}

export default App
