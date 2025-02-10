// Header 포함 높이 계산
const windowHeightWithHeader = window.innerHeight + document.querySelector("#header").offsetHeight;

// 스크롤 이벤트 핸들러
function scrollAction() {
  const scrollElements = document.querySelectorAll(".scroll");

  if (!scrollElements) {
    return;
  }

  scrollElements.forEach((scrollElement) => {
    const scrollHeight = scrollElement.getBoundingClientRect().top + 200;
    scrollElement.classList.toggle("scrollAction", windowHeightWithHeader > scrollHeight);
  });
}

// 애니메이션 이벤트 핸들러
function scaleEvent(selector) {
  const imgWrap = document.querySelector(selector);
  const imgWrapHeight = imgWrap && imgWrap.getBoundingClientRect().top;
  if (imgWrap && imgWrapHeight) {
    imgWrap.classList.toggle("on", windowHeightWithHeader > imgWrapHeight);
  }
}

// 애니메이션 delay 설정
function aniDelay(elements, delay) {
  elements.forEach((element, index) => {
    element.style.animationDelay = delay * index + "s";
  });
}

// 실행
const delayList = document.querySelectorAll('.delayList');

document.addEventListener("scroll", function () {
  scrollAction();
  scaleEvent('.delayScale ul');
});

document.addEventListener("DOMContentLoaded", function() {
  aniDelay(delayList, 0.3);
});