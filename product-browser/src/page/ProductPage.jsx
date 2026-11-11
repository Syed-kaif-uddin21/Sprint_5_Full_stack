import {useEffect, useState} from "react";
import {Link} from "react-router";

function ProductPage(){
    const [products, setProducts] = useState([]);

    useEffect(() => {
        async function loadProduct(){
            const res = await fetch("https://dummyjson.com/products")
            const data = await res.json();
            setProducts(data.products);
        }
        loadProduct();
    }, []);

    return(
        <>
        <p>loaded {products.length} products</p>

        <ul>
            {products.map(product => (
                <li key={product.id}>
                    <img src={product.thumbnail} />
                    <h3>{product.title}</h3>
                    <p>$ {product.price}</p>
                    <p>Rating : {product.rating}</p>
                    <p>Category : {product.category}</p>
                    <p>Reviews : {product.reviews.length}</p>
                    <Link to={`/products/${product.id}`}>View Details</Link>
                </li>
            ))}
        </ul>
        </>
        
    )
}

export default ProductPage;