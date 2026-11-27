<template>
  <footer class="site-footer">
    <div class="container-xl py-5">
      <div class="row g-4 align-items-start">
        <div class="col-lg-5">
          <RouterLink class="brand-mark footer-brand" to="/">
            <span class="brand-icon">R</span><span class="brand-copy">R<span>FITNESS</span></span>
          </RouterLink>
          <p class="footer-tagline mt-3">Show up. Put in the work. Get stronger.</p>
        </div>
        <div class="col-6 col-lg-3">
          <div class="footer-heading">EXPLORE</div>
          <a href="/#about">About us</a>
          <a href="/#training">Training</a>
          <a href="/#membership">Membership</a>
        </div>
        <div class="col-6 col-lg-4">
          <div class="footer-heading">FIND YOUR WAY</div>
          <a href="/#location">Uppal, Hyderabad</a>
          <a href="https://www.instagram.com/rfitness_gym/" target="_blank" rel="noreferrer">Instagram <i class="bi bi-arrow-up-right"></i></a>
          <RouterLink to="/admin">Admin</RouterLink>
        </div>
      </div>
      <div class="footer-bottom mt-5 pt-3 d-flex flex-wrap justify-content-between gap-2">
        <span>© {{ new Date().getFullYear() }} R Fitness. All rights reserved.</span>
        <span>Made for the work.</span>
      </div>
    </div>
  </footer>
</template>
