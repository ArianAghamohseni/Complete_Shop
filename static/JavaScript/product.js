"use strict";

const deleteProduct = async (product_id) => {
  await fetch(`/product/${product_id}`, {
    method: "DELETE",
    redirect: "follow",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (response.redirected) {
      window.location.href = response.url;
    }
  });
};

const addItemToCart = async (product_id) => {
  const quantity = document.getElementsByClassName(
    `item-quantity${product_id}`
  )[0].value;
  console.log(quantity);
  await fetch(`/cart_item/${product_id}`, {
    method: "POST",
    redirect: "follow",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ quantity }),
  }).then((response) => {
    if (response.redirected) {
      window.location.href = response.url;
    }
  });
};
