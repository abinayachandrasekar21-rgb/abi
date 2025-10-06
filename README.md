<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dynamic 3D Image Slider (5 Slides)</title>
<style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    background: linear-gradient(135deg, #f9a8d4, #f0abfc);
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    font-family: "Poppins", sans-serif;
    overflow: hidden;
  }

  .slider {
    position: relative;
    width: 80%;
    max-width: 900px;
    height: 420px;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 1000px;
  }

  .slide {
    position: absolute;
    width: 300px;
    height: 400px;
    border-radius: 20px;
    overflow: hidden;
    transition: all 0.8s ease;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    opacity: 0;
    transform: scale(0.8);
  }

  .slide img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /* Center image */
  .slide.active {
    transform: translateX(0) scale(1.1);
    z-index: 5;
    opacity: 1;
  }

  /* Left side */
  .slide.prev {
    transform: translateX(-220px) rotateY(30deg) scale(0.9);
    z-index: 4;
    opacity: 0.9;
  }

  /* Right side */
  .slide.next {
    transform: translateX(220px) rotateY(-30deg) scale(0.9);
    z-index: 4;
    opacity: 0.9;
  }

  /* Far left */
  .slide.prev2 {
    transform: translateX(-420px) rotateY(45deg) scale(0.8);
    z-index: 3;
    opacity: 0.6;
  }

  /* Far right */
  .slide.next2 {
    transform: translateX(420px) rotateY(-45deg) scale(0.8);
    z-index: 3;
    opacity: 0.6;
  }

  .controls {
    position: absolute;
    bottom: -60px;
    display: flex;
    justify-content: center;
    width: 100%;
    gap: 40px;
  }

  button {
    background: #fff;
    border: none;
    padding: 12px;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    transition: 0.3s;
  }

  button:hover {
    background: #e879f9;
  }

  .arrow {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-top: 3px solid #000;
    border-right: 3px solid #000;
  }

  .arrow.left {
    transform: rotate(-135deg);
  }

  .arrow.right {
    transform: rotate(45deg);
  }
</style>
</head>
<body>

  <div class="slider">
    <div class="slide"><img src="https://picsum.photos/id/1018/600/400" alt="Image 1"></div>
    <div class="slide"><img src="https://picsum.photos/id/1024/600/400" alt="Image 2"></div>
    <div class="slide"><img src="https://picsum.photos/id/1015/600/400" alt="Image 3"></div>
    <div class="slide"><img src="https://picsum.photos/id/1035/600/400" alt="Image 4"></div>
    <div class="slide"><img src="https://picsum.photos/id/1041/600/400" alt="Image 5"></div>

    <div class="controls">
      <button id="prev"><i class="arrow left"></i></button>
      <button id="next"><i class="arrow right"></i></button>
    </div>
  </div>

<script>
  const slides = document.querySelectorAll('.slide');
  let index = 0;

  function updateSlides() {
    slides.forEach(slide => {
      slide.classList.remove('active', 'prev', 'next', 'prev2', 'next2');
    });

    slides[index].classList.add('active');
    slides[(index - 1 + slides.length) % slides.length].classList.add('prev');
    slides[(index + 1) % slides.length].classList.add('next');
    slides[(index - 2 + slides.length) % slides.length].classList.add('prev2');
    slides[(index + 2) % slides.length].classList.add('next2');
  }

  document.getElementById('next').addEventListener('click', () => {
    index = (index + 1) % slides.length;
    updateSlides();
  });

  document.getElementById('prev').addEventListener('click', () => {
    index = (index - 1 + slides.length) % slides.length;
    updateSlides();
  });

  // Auto-slide every 4 seconds
  setInterval(() => {
    index = (index + 1) % slides.length;
    updateSlides();
  }, 4000);

  updateSlides();
</script>

</body>
</html>
