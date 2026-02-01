let ORDER_ID = null;

async function previewOrder() {
  const res = await fetch("/api/order/preview", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      ticker: document.getElementById("ticker").value,
      seed: Number(document.getElementById("seed").value),
      avg_price: Number(document.getElementById("avg").value),
      current_price: Number(document.getElementById("current").value)
    })
  });

  const data = await res.json();
  ORDER_ID = data.order_id;

  document.getElementById("orderInfo").innerText =
    `${data.ticker} | ${data.qty}주 | ${data.price}원`;

  document.getElementById("confirmBox").style.display = "block";
}

async function confirmOrder() {
  const res = await fetch(`/api/order/confirm/${ORDER_ID}`, {
    method: "POST"
  });

  const data = await res.json();
  alert(JSON.stringify(data));
}
