const btn = document.getElementById("btn");

let responce;
let infoList;

function getParams() {
  let data = [];
  let mass = [];
  let orderParams = [];
  let W = [];
  const form = document.getElementById("form");
  const formData = new FormData(form);
  
  for (let [key, value] of formData) {
    if (key == "W") {
      W.push(Number(value));
    } else {
      mass.push([key, value]);
    }
  }
  let num = 0;
  for (let i = 0; i < mass.length / 3; i++) {
    let item = [];
    item.push(Number(mass[num + 0][1]));
    item.push(Number(mass[num + 2][1]));
    orderParams.push(item);
    num += 3;
  }
  
  data[0] = W;
  data[1] = orderParams;
  console.log(data);
  return data;
}

async function fetchToDB(data) {
  // Блок try выполнится полностью, если не будет ошибок:
  try {
    // Выполняем запрос:
    responce = await fetch("test.php", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    infoList = await responce.json();
    return infoList; // Возвращаем результат запроса
  } catch (err) {
    // Блок catch сработает только если будут какие-то ошибки в блоке try:
    // Выведем в консоли информацию об ошибке:
    console.log("При запросе произошла ошибка, детали ниже:");
    console.error(err);
    // Вернем исключение с текстом поясняющим детали ошибки:
    // alert("Произошла ошибка при запросе!");
    throw new Error("Запрос завершился неудачно.");
  }
}

btn.addEventListener("click", async function (e) {
  e.preventDefault();
  const data = getParams();
  await fetchToDB(data);
  
  console.log(infoList[0]);
  console.log(infoList[1]);
  let div1 = document.createElement("div");
  let div2 = document.createElement("div");
  div1.textContent = infoList[0];
  for (let i = 0; i < infoList[1].length; i++) {
    let div = document.createElement("div");
    div.textContent = infoList[1][i];
    div2.append(div);
  }
    
  document.body.append(div1);
  document.body.append(div2);
});
