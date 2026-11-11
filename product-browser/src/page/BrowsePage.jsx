import {useEffect, useState} from "react";

function BrowsePage(){
    const [products, setProducts] = useState([]);
    const [page, setPage] = useState(1);

    useEffect(() => {
        async function loadProduct(){
            const skip = (page - 1) * 10;
            const res = await fetch(`https://dummyjson.com/products?limit=10&skip=${skip}`)
            const data = await res.json();
            setProducts(data.products);
        }
        loadProduct();
    }, [page]);
return(
        <>
        <p>loaded {products.length} products</p>
        <button disabled={page === 1} onClick={() => setPage(page - 1)}>Previous</button>
        <p>Page : {page}</p>
        <button onClick={() => setPage(page + 1)}>Next</button>
        <ul>
            {products.map(product => (
                <li key={product.id}>
                    <img src={product.thumbnail} />
                    <h3>{product.title}</h3>
                    <p>$ {product.price}</p>
                </li>
            ))}
        </ul>
        </>
        
    )
}

export default BrowsePage;