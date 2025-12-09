function update_cart_count() {
  const apiUrl = "http://127.0.0.1:8000/cart-item-count/";

  fetch(apiUrl)
    .then((response) => {
      if (!response.ok) {
        document.getElementById("cart").innerHTML = 0;
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data.count);
      document.getElementById("cart").innerHTML = data.count;
    })
    .catch((error) => {
      console.error("Error:", error);
    });

  console.log("hello");
}

update_cart_count(); //call everytime when page is reloaded
