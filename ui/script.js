const input = document.getElementById('promptInput');
const button = document.querySelector('#sendButton');
const container = document.querySelector('.container');

input.addEventListener('input', () => {
  if (input.value.trim() === "") {
    button.disabled = true;
  } else {
    button.disabled = false;
  }
});

button.addEventListener('click', () => {
  const element = document.createElement("div");
  element.textContent = input.value;
  element.classList.add("userMessage");
  container.appendChild(element);
  input.value = "";
  button.disabled = true;
  setTimeout(() => {
    const AIelement = document.createElement("div");
    AIelement.textContent = "Hello world!";
    AIelement.classList.add("AIMessage");
    container.appendChild(AIelement);
  }, 2000);
});
