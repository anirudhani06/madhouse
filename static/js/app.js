const signPage = document.getElementById('signin-page');
const createRoomPage = document.getElementById('create-room-page');
const settingsPage = document.getElementById('settings-page');
const chatRoomPage = document.getElementById('room-page');
const changePwdPage = document.getElementById('change-password-page');
const newPwdPage = document.getElementById('new-password-page');
const loginPage = document.getElementById('login-page');
const registerPage = document.getElementById('register-page');
const sidebarLinks = document.querySelector('.sidebar__links');

if (signPage) {
  const passwordEye = signPage.querySelector('.password_eye');
  const input = passwordEye.parentElement.querySelector('input');
  passwordEye.addEventListener('click', () => {
    if (passwordEye.classList.contains('on')) {
      input.setAttribute('type', 'text');
      passwordEye.classList.remove('on');
    } else {
      input.setAttribute('type', 'password');
      passwordEye.classList.add('on');
    }
  });
}

if (createRoomPage) {
  const previewImage = createRoomPage.querySelector('#image_input');

  previewImage.addEventListener('change', (event) => {
    if (event.target.files.length > 0) {
      const src = URL.createObjectURL(event.target.files[0]);
      createRoomPage.querySelector('.preview_image').src = src;
    }
  });
}

if (settingsPage) {
  const previewImage = settingsPage.querySelector('#image_input');

  previewImage.addEventListener('change', (event) => {
    if (event.target.files.length > 0) {
      const src = URL.createObjectURL(event.target.files[0]);
      settingsPage.querySelector('.preview_image').src = src;
    }
  });
}

if (chatRoomPage) {
  const chatRoom = chatRoomPage.querySelector('#room_chat_box');
  chatRoom.scrollTop = chatRoom.scrollHeight;
}

if (changePwdPage) {
  const eyes = changePwdPage.querySelectorAll('.eye');

  for (let i = 0; i < eyes.length; i++) {
    eyes[i].addEventListener('click', () => {
      const currentEye = eyes[i];
      const inputElem = currentEye.parentElement.querySelector('input');
      if (currentEye.classList.contains('showpwd')) {
        currentEye.classList.remove('showpwd');
        inputElem.setAttribute('type', 'password');
      } else {
        currentEye.classList.add('showpwd');
        inputElem.setAttribute('type', 'text');
      }
    });
  }
}
if (newPwdPage) {
  const eyes = newPwdPage.querySelectorAll('.eye');

  for (let i = 0; i < eyes.length; i++) {
    eyes[i].addEventListener('click', () => {
      const currentEye = eyes[i];
      const inputElem = currentEye.parentElement.querySelector('input');
      if (currentEye.classList.contains('showpwd')) {
        currentEye.classList.remove('showpwd');
        inputElem.setAttribute('type', 'password');
      } else {
        currentEye.classList.add('showpwd');
        inputElem.setAttribute('type', 'text');
      }
    });
  }
}
if (registerPage) {
  const eyes = registerPage.querySelectorAll('.eye');
  for (let i = 0; i < eyes.length; i++) {
    eyes[i].addEventListener('click', () => {
      const currentEye = eyes[i];
      const inputElem = currentEye.parentElement.querySelector('input');
      if (currentEye.classList.contains('showpwd')) {
        currentEye.classList.remove('showpwd');
        inputElem.setAttribute('type', 'password');
      } else {
        currentEye.classList.add('showpwd');
        inputElem.setAttribute('type', 'text');
      }
    });
  }
}
if (loginPage) {
  const eyes = loginPage.querySelector('.eye');
  eyes.addEventListener('click', () => {
    const currentEye = eyes;
    const inputElem = currentEye.parentElement.querySelector('input');
    if (currentEye.classList.contains('showpwd')) {
      currentEye.classList.remove('showpwd');
      inputElem.setAttribute('type', 'password');
    } else {
      currentEye.classList.add('showpwd');
      inputElem.setAttribute('type', 'text');
    }
  });
}

if (sidebarLinks) {
  let li = sidebarLinks.querySelectorAll('.link');
  const url = window.location.href;
  for (let i = 0; i < li.length; i++) {
    if (url === li[i].querySelector('a').href) {
      li[i].classList.add('active');
    } else {
      li[i].classList.remove('active');
    }
  }
}
