const input = document.getElementById('promptInput');
const button = document.querySelector('#sendButton');

input.addEventListener('input', () => {
  if (input.value.trim() === "") {
    button.disabled = true;
  } else {
    button.disabled = false;
  }
});

button.addEventListener('click', () => {
  input.value = "";
  button.disabled = true;
});
