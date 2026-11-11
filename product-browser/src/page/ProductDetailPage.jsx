import { useEffect, useState } from "react";
import { useParams } from "react-router";

function ProductDetailPage(){
    const {id} = useParams();
    const [product, setProduct] = useState(null);

    useEffect(() => {
        async function loadProduct(){
            const res = await fetch(`https://dummyjson.com/products/${id}`)
            const data = await res.json();
            setProduct(data);
        }
        loadProduct();
    }, [id]);

        if (!product) {
        return <p>Loading product details...</p>;
    }

    return (
        <>  
            <h3>{product.title}</h3>
            <img src={product.thumbnail} />
            <p>$ {product.price}</p>
            <p>{product.description}</p>
            <p>Rating: {product.rating}</p>
            <p>Category: {product.category}</p>
            <p>Reviews: {product.reviews.length}</p>
            <h3>Reviews</h3>
            <ul>
                {product.reviews.map((review, index) => (
                    <li key={index}>
                        <p>Rating: {review.rating}</p>
                        <p>Reviewer: {review.reviewerName}</p>
                        <p>Comment: {review.comment}</p>
                    </li>
                ))}
            </ul>
        </>
    );

}

export default ProductDetailPage;