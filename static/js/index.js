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
      console.log(`Cart count = ${data.count}`);
      document.getElementById("cart").innerHTML = data.count;
    })
    .catch((error) => {
      console.error("Error:", error);
    });

}

update_cart_count(); //calls everytime when page is reloaded
